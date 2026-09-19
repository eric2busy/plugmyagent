#!/usr/bin/env python3
"""Generate per-API static pages, sitemap.xml, and robots.txt for plugmyagent.com.

Each API in api-catalog.json gets its own page at /api/<slug>/ with full
SEO meta tags and Open Graph tags, so shared links unfurl with that API's
name and description and search engines can index every entry.

Slug logic replicates the site's JS exactly (slugify(name), then -2, -3...
on collision), so page URLs always match what the app's Share button copies.

Usage: python3 tools/generate-api-pages.py   (run from the repo root)
Re-run whenever api-catalog.json changes, then commit the output.
"""

import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.plugmyagent.com"
OG_IMAGE = BASE + "/og-card.png"
TODAY = date.today().isoformat()


def slugify(name):
    s = (name or "api").lower()
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "api"


def slugs_for(apis):
    """Mirror the site's slugToApi construction, collisions included."""
    seen = {}
    out = []
    for api in apis:
        base = slugify(api.get("name"))
        slug, n = base, 2
        while slug in seen:
            slug = f"{base}-{n}"
            n += 1
        seen[slug] = api
        out.append(slug)
    return out


def esc(text):
    return html.escape(str(text or ""), quote=True)


def clean_url(url):
    url = (url or "").strip()
    return url if url.startswith(("http://", "https://")) else ""


def meta_desc(api):
    d = (api.get("tagline") or api.get("description") or "").strip()
    d = re.sub(r"\s+", " ", d)
    return d if len(d) <= 160 else d[:157].rsplit(" ", 1)[0] + "..."


CSS = """
:root{
  color-scheme:dark;
  --ink:#f5f7f5; --muted:#9aa39e; --paper:#0b0d0d; --white:#101314; --card:#101314;
  --line:rgba(255,255,255,.09); --teal:#ff6b1a; --teal-ink:#201000; --teal-soft:rgba(255,107,26,.14);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
  background-size:48px 48px;
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:16px;line-height:1.55}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
.site-header{position:sticky;top:0;z-index:40;background:var(--white);border-bottom:1px solid var(--line)}
.site-header-inner{width:min(1120px,100%);margin:0 auto;padding:11px clamp(16px,4vw,32px);
  display:flex;align-items:center;min-height:56px}
.brandmark{display:inline-flex;align-items:center}
.brandmark img{display:block;height:30px;width:auto}
@media (max-width:560px){.brandmark img{height:24px}}
.crumb{font-size:13px;color:var(--muted);margin:26px 0 6px}
.crumb a{color:var(--muted)}
h1{font-size:clamp(34px,6vw,52px);line-height:1.02;letter-spacing:-.04em;margin:6px 0 10px;font-weight:800}
.pill{display:inline-block;font:600 12px "Azeret Mono",ui-monospace,monospace;
  background:var(--teal);color:var(--teal-ink);border-radius:999px;padding:5px 12px;margin-bottom:14px}
.tagline{font-size:19px;color:var(--muted);max-width:620px;margin:0 0 26px}
.cta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 34px}
.btn{display:inline-block;padding:13px 20px;border-radius:12px;font-weight:700;font-size:15px;
  text-decoration:none;border:1px solid var(--line);color:var(--ink);background:var(--card)}
button.btn{font:inherit;cursor:pointer}
.btn.primary{background:var(--teal);border-color:var(--teal);color:var(--teal-ink)}
h2{font-size:22px;letter-spacing:-.02em;margin:34px 0 12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:0 0 14px}
.card p{margin:0}
ul.tight{margin:0;padding-left:20px}
ul.tight li{margin:7px 0}
ol.steps{margin:0;padding:0;list-style:none;counter-reset:st}
ol.steps li{counter-increment:st;position:relative;padding:14px 14px 14px 58px;
  background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 10px}
ol.steps li::before{content:counter(st);position:absolute;left:14px;top:14px;width:30px;height:30px;
  border-radius:50%;background:var(--teal);color:var(--teal-ink);
  font:700 13px "Azeret Mono",ui-monospace,monospace;display:grid;place-items:center}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 14px}
.fact{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:14px}
.fact b{display:block;font:600 11px "Azeret Mono",ui-monospace,monospace;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
pre{margin:0;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;padding:16px;border-radius:12px;
  background:#050707;color:#f5f7f5;font:500 12.5px/1.55 "Azeret Mono",ui-monospace,monospace}
.verified{font-size:13px;color:var(--muted);margin:26px 0 0}
footer{border-top:1px solid var(--line);margin-top:44px;padding:22px 0 40px;font-size:13px;color:var(--muted)}
footer a{color:var(--muted)}
@media (max-width:620px){ .facts{grid-template-columns:1fr} }
"""


def render_page(api, slug):
    name = esc(api.get("name"))
    category = esc(api.get("category"))
    tagline = esc(api.get("tagline"))
    desc = esc(api.get("description"))
    page_url = f"{BASE}/api/{slug}/"
    app_url = f"{BASE}/catalog/?api={slug}"
    docs = clean_url(api.get("docs_url"))
    signup = clean_url(api.get("signup_url"))
    title = f"{api.get('name')} | Free API on PlugMyAgent"
    description = meta_desc(api)

    use_cases = "".join(f"<li>{esc(u)}</li>" for u in (api.get("use_cases") or []))
    steps = "".join(f"<li>{esc(s)}</li>" for s in (api.get("setup_steps") or []))
    best = ", ".join(esc(b) for b in (api.get("best_for") or []))

    example = ""
    if api.get("example"):
        example = f'<h2>Example request</h2><div class="card"><pre>{esc(api.get("example"))}</pre></div>'

    docs_btn = f'<a class="btn" href="{esc(docs)}" rel="noopener">Official docs</a>' if docs else ""
    signup_btn = ""
    if signup and signup != docs:
        signup_btn = f'<a class="btn" href="{esc(signup)}" rel="noopener">Get free access</a>'

    verified = esc(api.get("verified"))
    verified_line = f'<p class="verified">Last verified {verified} by the PlugMyAgent team.</p>' if verified else ""
    lc = api.get("link_check") or {}
    if lc.get("date"):
        if not lc.get("ok", True):
            status_word = "needs review"
        elif lc.get("unverified"):
            status_word = "couldn't verify automatically"
        else:
            status_word = "working"
        verified_line += (f'<p class="verified">Links last checked {esc(lc.get("date"))} '
                          f'({status_word}).</p>')

    ld = {
        "@context": "https://schema.org",
        "@type": "WebAPI",
        "name": api.get("name"),
        "description": description,
        "url": page_url,
        "documentationUrl": docs or None,
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }
    ld_json = json.dumps({k: v for k, v in ld.items() if v is not None}, ensure_ascii=False)
    ld_json = ld_json.replace("</script", "<\\/script")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="PlugMyAgent">
<meta property="og:title" content="{name} - free API">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} - free API">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<style>{CSS}</style>
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<div class="site-header"><div class="site-header-inner"><a class="brandmark" href="/" aria-label="PlugMyAgent home"><img src="/plug-lockup-v2.png" alt="PlugMyAgent"></a></div></div>
<main class="wrap">
<p class="crumb"><a href="/">Home</a> / <a href="/catalog/">Catalog</a> / {category} / {name}</p>
<span class="pill">{category}</span>
<h1>{name}</h1>
<p class="tagline">{tagline}</p>
<div class="cta-row">
<a class="btn primary" href="{app_url}">Open in PlugMyAgent</a><button class="btn" id="copyLink" type="button">Copy link</button>{docs_btn}{signup_btn}
</div>
<h2>What it does</h2>
<div class="card"><p>{desc}</p></div>
<h2>What you can do with it</h2>
<div class="card"><ul class="tight">{use_cases}</ul></div>
<h2>Set it up</h2>
<ol class="steps">{steps}</ol>
{example}
<h2>The fine print</h2>
<div class="facts">
<div class="fact"><b>Access</b>{esc(api.get("auth"))}</div>
<div class="fact"><b>Rate limit</b>{esc(api.get("rate_limit"))}</div>
<div class="fact"><b>Best for</b>{best}</div>
<div class="fact"><b>Category</b>{category}</div>
</div>
{verified_line}
</main>
<footer><div class="wrap">
<a href="/">PlugMyAgent</a> - every API free to start. &copy; 2026 hiddeninwest
</div></footer>
<script>
(function(){{var b=document.getElementById('copyLink');if(!b)return;
b.addEventListener('click',function(){{
var u=document.querySelector('link[rel="canonical"]').href;
function done(){{var o=b.textContent;b.textContent='Copied';setTimeout(function(){{b.textContent=o;}},1600);}}
function fallback(){{var t=document.createElement('textarea');t.value=u;document.body.appendChild(t);
t.select();try{{document.execCommand('copy');}}catch(e){{}}t.remove();done();}}
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(u).then(done,function(){{fallback();}});}}
else{{fallback();}}}});}})();
</script>
</body>
</html>
"""


def main():
    catalog = json.loads((ROOT / "api-catalog.json").read_text(encoding="utf-8"))
    slugs = slugs_for(catalog)
    api_dir = ROOT / "api"
    count = 0
    for api, slug in zip(catalog, slugs):
        page = api_dir / slug / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(render_page(api, slug), encoding="utf-8")
        count += 1

    urls = [BASE + "/", BASE + "/catalog/"] + [f"{BASE}/api/{s}/" for s in slugs]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8"
    )
    print(f"Wrote {count} API pages + sitemap.xml + robots.txt")


if __name__ == "__main__":
    main()
