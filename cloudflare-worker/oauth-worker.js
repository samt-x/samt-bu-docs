/**
 * Cloudflare Worker – GitHub OAuth-proxy + CF Pages build-status proxy
 *
 * Miljøvariabler som må settes i Cloudflare-dashboardet:
 *   CLIENT_ID     – GitHub App Client ID
 *   CLIENT_SECRET – GitHub App Client Secret (kryptert)
 *   WORKER_PAT    – Fine-grained PAT (samt-x org, Contents+Issues+PRs R/W)
 *
 * Endepunkter:
 *   GET  /auth?provider=github&site_id=...  → redirect til GitHub OAuth
 *   GET  /callback?code=...                 → bytt kode mot token, lukk popup
 *   GET  /build-status?url=<side-url>       → hent samtu-build-tag uten CDN-cache
 *   POST /suggest                           → opprett branch+commit+PR på vegne av ekstern bruker
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/auth") {
      return handleAuth(url, env);
    }

    if (url.pathname === "/callback") {
      return handleCallback(url, env);
    }

    if (url.pathname === "/build-status") {
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: buildStatusCors() });
      }
      return handleBuildStatus(url);
    }

    if (url.pathname === "/suggest") {
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: suggestCors() });
      }
      return handleSuggest(request, env);
    }

    return new Response("Not found", { status: 404 });
  },
};

// --- Build-status proxy (omgår CF CDN-cache ved hjelp av cf.bypassCache) ---

async function handleBuildStatus(url) {
  const cors = buildStatusCors();
  const pageUrl = url.searchParams.get("url");

  if (!pageUrl || !pageUrl.startsWith("https://docs.samt-bu.no/")) {
    return new Response(JSON.stringify({ error: "ugyldig url" }), {
      status: 400,
      headers: { "Content-Type": "application/json", ...cors },
    });
  }

  try {
    const resp = await fetch(pageUrl, {
      cf: { bypassCache: true },
      headers: { Accept: "text/html" },
    });
    const html = await resp.text();
    const m = html.match(/<meta name="samtu-build" content="([^"]+)"/);
    const buildTag = m ? m[1] : null;
    return new Response(JSON.stringify({ buildTag }), {
      headers: { "Content-Type": "application/json", ...cors },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: { "Content-Type": "application/json", ...cors },
    });
  }
}

function buildStatusCors() {
  return {
    "Access-Control-Allow-Origin": "https://docs.samt-bu.no",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Max-Age": "86400",
    "Cache-Control": "no-store",
  };
}

// --- GitHub OAuth ---

function handleAuth(url, env) {
  const provider = url.searchParams.get("provider");
  if (provider !== "github") {
    return new Response("Kun GitHub-autentisering er støttet.", { status: 400 });
  }

  const githubUrl = new URL("https://github.com/login/oauth/authorize");
  githubUrl.searchParams.set("client_id", env.CLIENT_ID);
  githubUrl.searchParams.set("state", url.searchParams.get("site_id") ?? "");

  // login=<brukernavn>: tvinger GitHub til å vise innloggingsskjema for den angitte brukeren
  const loginHint = url.searchParams.get("login");
  if (loginHint) githubUrl.searchParams.set("login", loginHint);

  // force=true (uten login-hint): rut via github.com/login for å vise innloggingsskjemaet
  if (!loginHint && url.searchParams.get("force") === "true") {
    const loginUrl = new URL("https://github.com/login");
    loginUrl.searchParams.set("return_to", githubUrl.toString());
    return Response.redirect(loginUrl.toString(), 302);
  }

  return Response.redirect(githubUrl.toString(), 302);
}

async function handleCallback(url, env) {
  // Bruker klikket «Cancel» i GitHub-autorisasjonsdialogen
  if (url.searchParams.get("error")) {
    return new Response(
      `<!DOCTYPE html><html lang="nb"><head><meta charset="utf-8"><title>Avbrutt</title></head>
<body><p>Innlogging avbrutt.</p>
<script>(function(){if(window.opener)window.opener.postMessage('authorization:github:cancelled','*');window.close();}());</script>
</body></html>`,
      { headers: { "Content-Type": "text/html;charset=UTF-8" } }
    );
  }

  const code = url.searchParams.get("code");
  if (!code) {
    return errorPage("Manglende 'code'-parameter fra GitHub.");
  }

  const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify({
      client_id: env.CLIENT_ID,
      client_secret: env.CLIENT_SECRET,
      code,
    }),
  });

  const tokenData = await tokenRes.json();

  if (tokenData.error) {
    return errorPage(
      `GitHub OAuth-feil: ${tokenData.error_description ?? tokenData.error}`
    );
  }

  const token = tokenData.access_token;
  const content = JSON.stringify({ token, provider: "github" });
  const message = `authorization:github:success:${content}`;

  const html = `<!DOCTYPE html>
<html lang="nb">
<head>
  <meta charset="utf-8">
  <title>Autentisering fullført</title>
</head>
<body>
<p>Autentisering fullført. Vinduet lukkes automatisk.</p>
<script>
(function () {
  const message = ${JSON.stringify(message)};

  function onMessage(e) {
    window.opener.postMessage(message, e.origin);
    window.removeEventListener("message", onMessage);
  }

  window.addEventListener("message", onMessage);
  window.opener.postMessage("authorizing:github", "*");
}());
</script>
</body>
</html>`;

  return new Response(html, {
    headers: { "Content-Type": "text/html;charset=UTF-8" },
  });
}

// --- /suggest – Worker-proxy for eksterne bidragsytere (branch + commit + PR) ---

async function handleSuggest(request, env) {
  if (request.method !== "POST") {
    return suggestError(405, "Method not allowed");
  }
  if (!env.WORKER_PAT) {
    return suggestError(500, "Server ikke konfigurert (mangler WORKER_PAT)");
  }

  let body;
  try { body = await request.json(); } catch { return suggestError(400, "Ugyldig JSON"); }

  const { repo, branch, treeItems, deletePrefix, commitMessage, prTitle, prBody, userToken } = body;

  if (!repo || typeof repo !== "string" || !/^[a-zA-Z0-9_.-]+$/.test(repo) || repo.length > 100) {
    return suggestError(400, "Ugyldig repo-navn");
  }
  if (!branch || typeof branch !== "string" || !/^[a-zA-Z0-9_./-]+$/.test(branch) || branch.length > 200) {
    return suggestError(400, "Ugyldig branch-navn");
  }
  if (!commitMessage || !prTitle) {
    return suggestError(400, "Mangler commitMessage eller prTitle");
  }
  if (!treeItems && !deletePrefix) {
    return suggestError(400, "Mangler treeItems eller deletePrefix");
  }

  // Verifiser at kallet har et token fra vår OAuth-flyt.
  // GitHub App user-tokens starter med ghu_, klassiske med ghp_.
  if (!userToken || typeof userToken !== "string" ||
      !(/^(ghu_|ghp_|github_pat_)[A-Za-z0-9_]{20,}$/.test(userToken))) {
    return suggestError(401, "Mangler gyldig brukertoken – logg inn først");
  }

  const gh = (path, opts = {}) => fetch(
    `https://api.github.com/repos/SAMT-X/${repo}${path}`,
    {
      ...opts,
      headers: {
        "Authorization": `Bearer ${env.WORKER_PAT}`,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "samt-bu-docs-worker/1.0",
      },
      cache: "no-store",
    }
  );

  const userInfo = await fetchGitHubUser(userToken);

  try {
    // 1. Hent HEAD commit SHA
    const refRes = await gh("/git/ref/heads/main");
    if (!refRes.ok) {
      const refErr = await refRes.json().catch(() => ({}));
      return suggestError(502, `Kunne ikke hente HEAD (${refRes.status}): ${refErr.message || refRes.statusText}`);
    }
    const { object: { sha: headSha } } = await refRes.json();

    // 2. Hent commit for å få tree SHA
    const commitRes = await gh(`/git/commits/${headSha}`);
    if (!commitRes.ok) return suggestError(502, "Kunne ikke hente commit");
    const { tree: { sha: baseTreeSha } } = await commitRes.json();

    // 3. Bygg tree-items (vanlig upsert eller rekursiv sletting via prefix)
    let items = treeItems || [];
    if (deletePrefix) {
      const treeRes = await gh(`/git/trees/${baseTreeSha}?recursive=1`);
      if (!treeRes.ok) return suggestError(502, "Kunne ikke hente repo-tre");
      const { tree } = await treeRes.json();
      const prefix = deletePrefix.replace(/\/$/, "") + "/";
      items = tree
        .filter(i => i.type === "blob" && i.path.startsWith(prefix))
        .map(i => ({ path: i.path, mode: i.mode, type: "blob", sha: null }));
      if (items.length === 0) return suggestError(400, "Ingen filer funnet under angitt sti");
    }

    // 4. Opprett nytt tre
    const newTreeRes = await gh("/git/trees", {
      method: "POST",
      body: JSON.stringify({ base_tree: baseTreeSha, tree: items }),
    });
    if (!newTreeRes.ok) {
      const e = await newTreeRes.json();
      return suggestError(502, `Tre-oppretting feilet: ${e.message}`);
    }
    const { sha: newTreeSha } = await newTreeRes.json();

    // 5. Opprett commit
    const commitPayload = { message: commitMessage, tree: newTreeSha, parents: [headSha] };
    if (userInfo) commitPayload.author = { ...userInfo, date: new Date().toISOString() };
    const newCommitRes = await gh("/git/commits", {
      method: "POST",
      body: JSON.stringify(commitPayload),
    });
    if (!newCommitRes.ok) {
      const e = await newCommitRes.json();
      return suggestError(502, `Commit-oppretting feilet: ${e.message}`);
    }
    const { sha: newCommitSha } = await newCommitRes.json();

    // 6. Opprett branch pekende på ny commit
    const branchRes = await gh("/git/refs", {
      method: "POST",
      body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: newCommitSha }),
    });
    if (!branchRes.ok) {
      const e = await branchRes.json();
      return suggestError(502, `Branch-oppretting feilet: ${e.message}`);
    }

    // 7. Opprett pull request
    const prRes = await gh("/pulls", {
      method: "POST",
      body: JSON.stringify({ title: prTitle, body: prBody || "", head: branch, base: "main" }),
    });
    if (!prRes.ok) {
      const e = await prRes.json();
      return suggestError(502, `PR-oppretting feilet: ${e.message}`);
    }
    const { number, html_url } = await prRes.json();

    return new Response(JSON.stringify({ pr_number: number, pr_url: html_url }), {
      headers: { "Content-Type": "application/json", ...suggestCors() },
    });

  } catch (e) {
    return suggestError(500, e.message);
  }
}

async function fetchGitHubUser(token) {
  try {
    const res = await fetch("https://api.github.com/user", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "samt-bu-docs-worker/1.0",
      },
      cache: "no-store",
    });
    if (!res.ok) return null;
    const u = await res.json();
    return {
      name: u.name || u.login,
      email: u.email || `${u.id}+${u.login}@users.noreply.github.com`,
    };
  } catch {
    return null;
  }
}

function suggestCors() {
  return {
    "Access-Control-Allow-Origin": "https://docs.samt-bu.no",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Cache-Control": "no-store",
  };
}

function suggestError(status, message) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { "Content-Type": "application/json", ...suggestCors() },
  });
}

function errorPage(message) {
  return new Response(
    `<!DOCTYPE html><html lang="nb"><body><p>Feil: ${message}</p></body></html>`,
    {
      status: 400,
      headers: { "Content-Type": "text/html;charset=UTF-8" },
    }
  );
}
