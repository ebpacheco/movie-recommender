export default {
  async fetch(request, env) {
    try {
      return await env.ASSETS.fetch(request);
    } catch (err) {
      // Fallback SPA: serve index.html mantendo query string para o Vue Router
      const url = new URL(request.url);
      const indexRequest = new Request(`${url.origin}/index.html`, { headers: request.headers });
      return await env.ASSETS.fetch(indexRequest);
    }
  }
};
