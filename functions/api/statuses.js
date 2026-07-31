/**
 * Cloudflare Pages Function — shared post statuses.
 *
 * GET  /api/statuses           -> { "<postId>": "approved", ... }
 * POST /api/statuses  { id, status }  -> persists one status for everyone
 *
 * Requires a KV namespace bound as `STATUSES` in the Pages project
 * (Settings > Functions > KV namespace bindings). Until that binding exists the
 * endpoints return 501 and the dashboard silently falls back to localStorage.
 */
const KEY = 'statuses';
const VALID = ['in-review', 'approved', 'declined'];

export async function onRequestGet({ env }) {
  if (!env.STATUSES) return json({ error: 'kv-not-configured' }, 501);
  const raw = await env.STATUSES.get(KEY);
  return json(raw ? JSON.parse(raw) : {});
}

export async function onRequestPost({ request, env }) {
  if (!env.STATUSES) return json({ error: 'kv-not-configured' }, 501);

  let body;
  try { body = await request.json(); } catch (_) { return json({ error: 'bad-json' }, 400); }

  const id = body && body.id;
  const status = body && body.status;
  if (!id || VALID.indexOf(status) === -1) return json({ error: 'invalid' }, 400);

  const current = JSON.parse((await env.STATUSES.get(KEY)) || '{}');
  current[id] = status;
  await env.STATUSES.put(KEY, JSON.stringify(current));
  return json({ ok: true, id, status });
}

function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}
