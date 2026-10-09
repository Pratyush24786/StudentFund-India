const FIELDS = ["title", "category", "label", "icon", "iconTone", "description", "amount", "deadline", "level", "location", "tag", "eligibility", "details", "provider", "url"];
const LABELS = { funding: "FUNDING & GRANTS", startup: "BUILD A STARTUP", innovation: "INNOVATION PROGRAM", student: "STUDENT SCHEME" };
const ICONS = { funding: ["♢", "green"], startup: ["↗", "peach"], innovation: ["✳", "blue"], student: ["✦", "lilac"] };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });

export async function onRequestGet({ env }) {
  const { results } = await env.LAUNCHPAD_DB.prepare(`SELECT id, ${FIELDS.join(", ")} FROM opportunities ORDER BY id DESC`).all();
  return json(results);
}

export async function onRequestPost({ request, env }) {
  if (!env.ADMIN_PASSWORD || request.headers.get("X-Admin-Password") !== env.ADMIN_PASSWORD) return json({ error: "Incorrect admin password." }, 401);
  let input;
  try { input = await request.json(); } catch { return json({ error: "Request body must be JSON." }, 400); }
  const data = Object.fromEntries(FIELDS.map((field) => [field, String(input[field] ?? "").trim()]));
  const required = ["title", "category", "description", "amount", "deadline", "eligibility", "details", "provider"];
  if (required.some((field) => !data[field])) return json({ error: "Please fill in all required fields." }, 400);
  if (!Object.hasOwn(LABELS, data.category)) return json({ error: "Choose a valid category." }, 400);
  if (!["undergraduate", "postgraduate", "any"].includes(data.level) || !["india", "global"].includes(data.location)) return json({ error: "Choose a valid study level and location." }, 400);
  if (data.url && !/^https?:\/\//i.test(data.url)) return json({ error: "Official link must start with http:// or https://." }, 400);
  data.label = LABELS[data.category];
  [data.icon, data.iconTone] = ICONS[data.category];
  const placeholders = FIELDS.map(() => "?").join(", ");
  const result = await env.LAUNCHPAD_DB.prepare(`INSERT INTO opportunities (${FIELDS.join(", ")}) VALUES (${placeholders})`).bind(...FIELDS.map((field) => data[field])).run();
  const saved = await env.LAUNCHPAD_DB.prepare(`SELECT id, ${FIELDS.join(", ")} FROM opportunities WHERE id = ?`).bind(result.meta.last_row_id).first();
  return json(saved, 201);
}
