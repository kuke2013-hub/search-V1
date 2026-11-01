// Foundation only. This Worker performs NO external crawling and NO outreach.
// Data endpoints must remain disabled until authenticated access is deployed.
export default {
  async fetch(request) {
    const path = new URL(request.url).pathname;
    if (path === "/health" && request.method === "GET") {
      return Response.json({
        service: "search-v1",
        status: "foundation_only",
        liveSourceChecks: false,
        outboundMessaging: false,
        privateDataApi: false
      }, { headers: { "cache-control": "no-store" } });
    }
    return new Response("Not found", { status: 404 });
  },

  async scheduled(controller, env) {
    // Observability probe only: even a successful cron invocation does not
    // mean source monitoring has run successfully.
    if (!env.DB) {
      console.error("Scheduler not configured: D1 binding missing");
      return;
    }
    const now = new Date().toISOString();
    await env.DB.prepare(
      "INSERT INTO scheduler_runs (id, started_at, status, source_count, completed_at) VALUES (?, ?, ?, ?, ?)"
    ).bind(crypto.randomUUID(), new Date(controller.scheduledTime).toISOString(),
      "not_configured", 0, now).run();
  }
};
