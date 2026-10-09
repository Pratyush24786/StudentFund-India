# Launchpad — Student Opportunity Finder

A responsive website for student benefits, startup support, grants and innovation programs. It supports local development (Flask + SQLite) and Cloudflare Pages (Pages Functions + D1).

## Deploy to Cloudflare Pages + D1

Cloudflare runs the website and API; D1 stores opportunities. You do not repeatedly run `requirements.txt` on Cloudflare. That file is only for the local Flask version. The website requests current records from `/api/opportunities` whenever it loads.

1. Install Node.js, then in this folder run `npm install -D wrangler` (or use `npx wrangler` if you do not want to add a project dependency).
2. Sign in to Cloudflare: `npx wrangler login`.
3. Create the D1 database: `npx wrangler d1 create launchpad-opportunities`. Copy the returned database ID into `database_id` in `wrangler.toml`, replacing `REPLACE_WITH_YOUR_D1_DATABASE_ID`.
4. Create the database table: `npx wrangler d1 migrations apply launchpad-opportunities --remote`.
5. Create a Pages project named `launchpad-student-opportunities` in the Cloudflare dashboard (Workers & Pages → Create application → Pages).
6. Create the admin password secret: `npx wrangler pages secret put ADMIN_PASSWORD --project-name launchpad-student-opportunities`. Enter a strong password when prompted.
7. Deploy this folder: `npx wrangler pages deploy . --project-name launchpad-student-opportunities`.
8. Open the deployed site and visit `/admin` to add opportunities. Saved listings are stored in D1 and served by the API to the homepage. The first migration adds eight sample listings.

If you connect a Git repository through the Cloudflare dashboard instead, set the D1 binding name to `LAUNCHPAD_DB` and add the `ADMIN_PASSWORD` secret in the Pages project settings, then redeploy. Keep `functions/` at the project root so Pages detects the API routes.

### Local Cloudflare preview

After creating the D1 database and editing its ID in `wrangler.toml`, run `npx wrangler pages dev . --d1 LAUNCHPAD_DB=YOUR_D1_DATABASE_ID`. Wrangler uses local development storage by default, so preview data is separate from production data.

## Run the local Python version

For local Flask development only:

```powershell
py -m pip install -r requirements.txt
$env:LAUNCHPAD_ADMIN_PASSWORD = "choose-a-password"
py server.py
```

Open `http://127.0.0.1:8000`; the admin form is at `/admin`. The first run creates `launchpad.db` and inserts eight illustrative starter listings. Cloudflare Pages uses D1 instead of this SQLite file.

## Files

- `index.html`, `styles.css` — public page and responsive design
- `app.js` — fetches listings from the API and provides search, filters, saved items and details
- `admin.html`, `admin.js` — listing entry form
- `functions/api/opportunities.js` — Cloudflare Pages API backed by D1
- `migrations/0001_create_opportunities.sql` — creates the D1 table
- `wrangler.toml` — Cloudflare Pages and D1 configuration; add the database ID after creating D1
- `server.py`, `requirements.txt` — optional local Flask + SQLite development version
- `launchpad.db` — created automatically on first local Python run; do not commit real user data

The included opportunities are sample data, not verified live offers. Confirm eligibility, deadlines and application URLs with each official provider.
