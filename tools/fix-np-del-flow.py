"""Erstatter NP- og Del-flyten i custom-footer.html med Worker-basert suggest-flyt."""
import sys

path = "S:/app-data/github/samt-x-repos/samt-bu-docs/themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ── NP-flyt: finn og erstatt ──────────────────────────────────────────────────
# Søker etter nøkkeldelen som identifiserer blokken
NP_MARKER = "        : ensureForkReady(token, npRepo).then(function() { return tryNpCommit(2, branchName, npLogin); });\n"
if NP_MARKER not in content:
    print("NP marker IKKE FUNNET")
    sys.exit(1)

# Finn start og slutt av blokken
np_start = content.find("    checkCollaboratorPermission(npRepo, function(canWrite) {")
np_end = content.find("\n        .catch(function(err) {\n          showMsg('error'", np_start)
if np_start == -1 or np_end == -1:
    print(f"NP start/slutt IKKE FUNNET: start={np_start}, end={np_end}")
    sys.exit(1)

old_np = content[np_start:np_end]
print(f"NP-blokk funnet: linje ~{content[:np_start].count(chr(10))+1}")

new_np = (
    "    checkCollaboratorPermission(npRepo, function(canWrite) {\n"
    "      var branchName = canWrite ? null : makePrBranch();\n"
    "      var npLogin = localStorage.getItem('samt-bu-gh-user') || 'unknown';\n"
    "      var commitPromise = canWrite\n"
    "        ? tryNpCommit(2)\n"
    "        : Promise.all([\n"
    "            weightInt ? fetchSiblingWeightUpdates(token, npRepo, npParentPath, weightInt, slug) : Promise.resolve([]),\n"
    "            Promise.resolve([])\n"
    "          ]).then(function(results) {\n"
    "            var items = newFiles.concat(results[0]).map(function(f) {\n"
    "              return {path: f.path, mode: '100644', type: 'blob', content: f.content};\n"
    "            });\n"
    "            var prTitle = (npLang === 'en' ? 'Suggest new page: ' : 'Foreslår ny side: ') + titleNb;\n"
    "            var prBody = npLang === 'en'\n"
    "              ? 'New page suggested by @' + npLogin + ' via SAMT-BU Docs editor.'\n"
    "              : 'Ny side foreslått av @' + npLogin + ' via SAMT-BU Docs redigeringsgrensesnitt.';\n"
    "            return suggestViaWorker(npRepo, branchName, items, null, commitMsg, prTitle, prBody);\n"
    "          });\n"
    "      commitPromise\n"
    "        .then(function(result) {\n"
    "          if (canWrite) {\n"
    "            npTitle = titleNb;\n"
    "            if (npMode === 'child') {\n"
    "              npNewPageUrl = npCurrentPermalink.replace(/\\/?$/, '/') + slug + '/';\n"
    "            } else {\n"
    "              var parentUrl = npCurrentPermalink.replace(/\\/[^\\/]+\\/?$/, '/');\n"
    "              npNewPageUrl = parentUrl + slug + '/';\n"
    "            }\n"
    "            showNpBuildPanel();\n"
    "            samtuIncrementPending();\n"
    "            npPollBuild(startTime);\n"
    "          } else {\n"
    "            setNpStatus(npLang === 'en' ? '\\u2713 Pull request sent' : '\\u2713 Pull request sendt');\n"
    "            submitBtn.textContent = npLang === 'en' ? 'Sent' : 'Sendt';\n"
    "            submitBtn.style.background = '#2d7a3a';\n"
    "            submitBtn.style.cursor = 'default';\n"
    "            var cancelBtn = document.getElementById('np-cancel');\n"
    "            if (cancelBtn) cancelBtn.textContent = npLang === 'en' ? 'Close' : 'Lukk';\n"
    "            if (result && result.html_url) {\n"
    "              var statusEl = document.getElementById('np-status-text');\n"
    "              if (statusEl) statusEl.innerHTML = (npLang === 'en' ? '\\u2713 PR: ' : '\\u2713 PR: ') +\n"
    "                '<a href=\"' + result.html_url + '\" target=\"_blank\" style=\"color:#fff; text-decoration:underline;\">#' + result.number + '</a>';\n"
    "            }\n"
    "          }\n"
    "        })"
)

content = content[:np_start] + new_np + content[np_end:]
print("NP: erstattet OK")

# ── Del-flyt: finn og erstatt ─────────────────────────────────────────────────
DEL_MARKER = "        : ensureForkReady(token, delRepo).then(function() { return tryDelCommit(2, delLogin); });\n"
if DEL_MARKER not in content:
    print("Del marker IKKE FUNNET")
    sys.exit(1)

del_start = content.find("      var delPromise = canWrite\n        ? tryDelCommit(2)\n        : ensureForkReady(token, delRepo)")
if del_start == -1:
    print("Del start IKKE FUNNET")
    sys.exit(1)

del_block_end = content.find("        .catch(function(err) {\n          document.getElementById('del-confirm-section-2')", del_start)
if del_block_end == -1:
    print("Del slutt IKKE FUNNET")
    sys.exit(1)

old_del = content[del_start:del_block_end]
print(f"Del-blokk funnet, lengde={len(old_del)}")

new_del = (
    "      var delSuggestItems = delChildCount > 0 ? null : [\n"
    "        {path: nbPath, mode: '100644', type: 'blob', sha: null},\n"
    "        {path: enPath, mode: '100644', type: 'blob', sha: null}\n"
    "      ];\n"
    "      var delSuggestPrefix = delChildCount > 0 ? delDirPath : null;\n"
    "      var delPrTitle = (delLang === 'en' ? 'Suggest deletion: ' : 'Foreslår sletting: ') + delTitle;\n"
    "      var delPrBody = delLang === 'en'\n"
    "        ? 'Deletion suggested by @' + delLogin + ' via SAMT-BU Docs.'\n"
    "        : 'Sletting foreslått av @' + delLogin + ' via SAMT-BU Docs.';\n"
    "      var delPromise = canWrite\n"
    "        ? tryDelCommit(2)\n"
    "        : suggestViaWorker(delRepo, branchName, delSuggestItems, delSuggestPrefix, commitMsg, delPrTitle, delPrBody);\n"
    "      delPromise\n"
    "        .then(function(result) {\n"
    "          if (canWrite) {\n"
    "            showBuildPanel();\n"
    "            samtuIncrementPending();\n"
    "            pollBuild(startTime);\n"
    "          } else {\n"
    "            showBuildPanel();\n"
    "            document.getElementById('del-heading').textContent =\n"
    "              delLang === 'en' ? 'Suggestion sent!' : 'Forslag sendt!';\n"
    "            var buildText = document.getElementById('del-build-status-text');\n"
    "            if (buildText) buildText.innerHTML = (delLang === 'en' ? 'Pull request created: ' : 'Pull request opprettet: ') +\n"
    "              (result && result.html_url ? '<a href=\"' + result.html_url + '\" target=\"_blank\">#' + result.number + '</a>' : '');\n"
    "            var doneBtn = document.getElementById('del-panel-done');\n"
    "            if (doneBtn) { doneBtn.style.display = 'inline-block'; doneBtn.onclick = closeDialog; }\n"
    "            var closeBtn = document.getElementById('del-panel-close');\n"
    "            if (closeBtn) closeBtn.style.display = 'none';\n"
    "          }\n"
    "        })"
)

content = content[:del_start] + new_del + content[del_block_end:]
print("Del: erstattet OK")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Ferdig – fil lagret.")
