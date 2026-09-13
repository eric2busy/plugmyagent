# plugmyagent.com

Free API catalog for AI-agent rookies — 421 free APIs with plain-English setup guides.

## What's here
- `index.html` — the entire website (single file, no build step). This is what Vercel deploys.
- `api-catalog.json` — the source of truth. Every API, every field, in one JSON array.

## How updates work
1. Edit `api-catalog.json` (or ask Slime for a fresh copy).
2. Rebuild `index.html` from it.
3. Commit + push — Vercel auto-deploys.

## Data fields per API
name, category, tagline, description, auth, best_for, docs_url, signup_url, rate_limit, setup_steps, example, use_cases, verified
