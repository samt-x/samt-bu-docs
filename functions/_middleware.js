export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === "samt-bu-docs.pages.dev") {
    return Response.redirect("https://docs.samt-bu.no" + url.pathname + url.search, 301);
  }
  return context.next();
}
