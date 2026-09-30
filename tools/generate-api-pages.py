#!/usr/bin/env python3
"""Generate per-API static pages, sitemap.xml, and robots.txt for plugmyagent.com.

Each API in api-catalog.json gets its own page at /api/<slug>/ with full
SEO meta tags and Open Graph tags, so shared links unfurl with that API's
name and description and search engines can index every entry.

Design: the orange catalog-drawer aesthetic (hero + badge + quick actions,
composed 3-step setup, fine-print cards), rendered fully server-side so the
page an AI or crawler fetches carries the complete content.

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

# Categories that are tools, not APIs: page copy says "free tool" instead of "free API".
NON_API_CATS = {"MCP Servers", "Agent Templates", "Eval & Testing", "Guardrails",
                "Agent Skills", "Memory", "Frameworks", "Agent Frameworks"}


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
    d = (api.get("description") or api.get("tagline") or "").strip()
    d = re.sub(r"\s+", " ", d)
    return d if len(d) <= 160 else d[:157].rsplit(" ", 1)[0] + "..."


# ---------------------------------------------------------------------------
# Drawer composition logic, ported from build/catalog/index.html (openDetail).
# Mirrors the catalog SPA's detail view exactly so both surfaces agree.
# ---------------------------------------------------------------------------

GOALS = [
    ("Send messages & alerts", ["Messaging & Chat", "Push Notifications", "Email", "Voice & Video"]),
    ("Organize my life", ["Calendars & Scheduling", "Task & Project Tools", "Forms", "Automation", "Business Operations", "Smart Home"]),
    ("Weather", ["Weather", "Environment & Climate"]),
    ("Maps, travel & getting around", ["Maps & Geocoding", "Routing", "Transit", "Flights", "Travel", "Time & Location"]),
    ("News & web search", ["News", "Web Search", "Social & Community", "Scraping & Extraction", "Marketing & SEO"]),
    ("Movies, music & fun", ["Movies & TV", "Anime", "Music", "Podcasts", "Games", "Sports", "Fun & Random", "Avatars & Images"]),
    ("Money & markets", ["Stocks", "Crypto", "FX & Currency", "Economic Data", "Blockchain", "Payments Dev", "Banking & Budgeting"]),
    ("Health, food & science", ["Nutrition & Food", "Fitness", "Medical & Drug Info", "Science Data", "Scholarly", "Books & Learning"]),
    ("Government, jobs & civic", ["US Government Data", "Civic & Legal", "Jobs & Careers"]),
    ("Safety & networks", ["Threat Intel", "Network & IP Intel", "Auth & Identity"]),
    ("Build & code", ["Code & Repos", "Dev Utilities", "Databases", "Hosting & Cloud", "AI & ML", "Audio & Speech", "Images & Media", "Link Tools", "Ecommerce Dev", "Utilities"]),
]
GOAL_TESTS = {
    "Send messages & alerts": "have it send you the message \u201cplugmyagent test\u201d",
    "Organize my life": "have it create an item called \u201cplugmyagent test\u201d, then delete it",
    "Weather": "ask it: \u201cwhat's the weather in Los Angeles right now?\u201d",
    "Maps, travel & getting around": "ask it to look up an address you know well",
    "News & web search": "ask it for today's top headlines",
    "Movies, music & fun": "ask it to look something up for you",
    "Money & markets": "ask it: \u201cwhat's the price of Bitcoin in USD?\u201d",
    "Health, food & science": "ask it to look up one item you know",
    "Government, jobs & civic": "ask it to find one real record for you",
    "Safety & networks": "ask it to check a domain or IP address you know",
    "Build & code": "ask it to fetch one small thing, like a repo or a fresh UUID",
}
AUTH_HOW = {
    "Telegram Bot API": "Your bot token goes right in the URL where the example shows it.",
    "Discord Webhooks": "No separate key. Your webhook URL (Discord channel settings \u2192 Integrations \u2192 Webhooks) is the secret. Swap your full URL in for the example.",
    "Slack Incoming Webhooks": "No separate key. Your webhook URL from the Slack app setup is the secret. Swap your full URL in for the example.",
    "ntfy": "No key. Just pick a topic name and put it in the URL.",
    "Gotify": "Your app token goes in the URL as ?token=PASTE_KEY_HERE (it runs on a server).",
    "OpenWeather": "Your key goes in the URL as ?appid=PASTE_KEY_HERE.",
    "CoinGecko Demo API": "Your demo key goes in the x-cg-demo-api-key header.",
    "ExchangeRate-API v6": "Your key goes right in the URL where the example shows it.",
    "Todoist API": "Your token goes in the Authorization header as: Bearer <redacted>",
    "Notion API": "Your token goes in the Authorization header as: Bearer <redacted> (plus a Notion-Version header).",
    "Twilio Programmable Messaging/Voice": "Uses your Account SID and Auth Token with HTTP Basic Auth; the SID also goes in the URL.",
    "Twilio Verify": "Uses your Account SID and Auth Token with HTTP Basic Auth; the SID also goes in the URL.",
    "Stripe API Test Mode": "Your test secret key goes as the Basic Auth username: -u sk_test_PASTE_KEY_HERE: (blank password).",
    "Gmail API": "Uses Google OAuth 2.0 (not a simple key). Follow the setup steps above; your agent will need the OAuth credentials.",
    "Google Calendar API": "Uses Google OAuth 2.0 (not a simple key). Follow the setup steps above; your agent will need the OAuth credentials.",
}


def effort_label(auth):
    if auth == "No key":
        return "No signup"
    if auth == "Free key (no card)":
        return "Free account"
    if auth == "Free tier (card may be required)":
        return "Card may be required"
    return "Free trial"


def effort_class(label):
    if label == "No signup":
        return "no-signup"
    if label == "Free account":
        return "free-account"
    return "caution"


def normalize_example(example):
    s = str(example or "")
    s = re.sub(r"<YOUR_API_KEY>", "PASTE_KEY_HERE", s, flags=re.I)
    s = re.sub(r"<API_KEY>", "PASTE_KEY_HERE", s, flags=re.I)
    s = re.sub(r"\{api_key\}", "PASTE_KEY_HERE", s, flags=re.I)
    s = re.sub(r"<token>", "PASTE_KEY_HERE", s, flags=re.I)
    s = re.sub(r"\bYOUR_API_KEY\b", "PASTE_KEY_HERE", s)
    s = re.sub(r"\bYOUR_KEY\b", "PASTE_KEY_HERE", s)
    s = re.sub(r"YOUR_KEYSTRING", "PASTE_KEY_HERE", s)
    s = re.sub(r"sk_test_YOUR_KEY", "sk_test_PASTE_KEY_HERE", s)
    s = re.sub(r"_YOUR_KEY", "_PASTE_KEY_HERE", s)
    s = re.sub(r"YOUR_APP_TOKEN", "PASTE_KEY_HERE", s)
    return s


def test_for(api):
    category = api.get("category") or ""
    for label, categories in GOALS:
        if category in categories:
            return GOAL_TESTS[label]
    return "try one small real request to confirm it works"


def agent_prompt(api):
    no_key = api.get("auth") == "No key"
    lines = []
    lines.append(f"Set up {api.get('name')} for me so you can use it.")
    lines.append("")
    lines.append("HOW TO CALL IT")
    lines.append(normalize_example(api.get("example")))
    lines.append("")
    if no_key:
        lines.append("AUTH: none needed. No signup, no key.")
    else:
        lines.append("AUTH: free API key. Mine: PASTE_KEY_HERE.")
        lines.append(AUTH_HOW.get(api.get("name"),
            "Put it where the example above shows (usually an Authorization header or a key in the URL)."))
        if api.get("auth") == "Free tier (card may be required)":
            lines.append("Heads up: signup may ask for a card.")
        if api.get("auth") == "Free trial":
            lines.append("Heads up: this is a free trial. Check how long it lasts.")
    lines.append("")
    lines.append(f"FREE LIMIT: {api.get('rate_limit') or ''}")
    lines.append("")
    lines.append(f"TEST: once it's set up, {test_for(api)}.")
    lines.append("If you can't make web requests yourself, give me the exact curl command with my key filled in so I can run it.")
    lines.append("")
    lines.append(f"Docs if you get stuck: {api.get('docs_url') or ''}")
    return "\n".join(lines)


CSS = """
:root{
  color-scheme:dark;
  --ink:#f5f7f5; --muted:#9aa39e; --paper:#0b0d0d; --white:#101314;
  --line:rgba(255,255,255,.09); --teal:#ff6b1a; --teal-ink:#201000; --teal-soft:rgba(255,107,26,.14);
  --green:#4ade80; --green-soft:rgba(74,222,128,.12);
  --blue:#7fb5ec; --blue-soft:rgba(127,181,236,.12);
  --amber:#f0be4f; --amber-soft:rgba(240,190,79,.12);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:16px;line-height:1.55}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
.site-header{position:sticky;top:0;z-index:40;background:var(--white);border-bottom:1px solid var(--line)}
.site-header-inner{width:min(1120px,100%);margin:0 auto;padding:11px clamp(16px,4vw,32px);
  display:flex;align-items:center;min-height:56px}
.brandmark{display:inline-flex;align-items:center}
.brandmark img{display:block;height:26px;width:auto}
.cart-link{position:relative;display:inline-flex;align-items:center;color:var(--ink);text-decoration:none;padding:8px;border-radius:10px;margin-left:auto}
.cnav{display:flex;gap:22px;margin-left:26px}
.cnav a{font-family:"Azeret Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);text-decoration:none}
.cnav a:hover{color:var(--ink)}
.cart-link:hover{color:var(--teal)}
.cart-link svg{width:22px;height:22px;display:block}
.cart-count{position:absolute;top:1px;right:-2px;min-width:18px;height:18px;border-radius:999px;background:var(--teal);color:var(--teal-ink);font:700 11px/18px "Azeret Mono",ui-monospace,monospace;text-align:center;padding:0 4px}
/* ---- orange hero, ported from the catalog drawer detail view ---- */
.d-hero{padding:54px 0 38px;background:var(--teal);color:var(--teal-ink)}
.d-hero.has-img{background-size:cover;background-position:center;color:#f5f7f5}
.d-hero.has-img .d-category{color:#f5f7f5}
.d-hero.has-img .d-tagline{color:rgba(245,247,245,.88)}
.d-hero.has-img .crumb,.d-hero.has-img .crumb a{color:rgba(245,247,245,.75)}
.crumb{font-size:13px;color:rgba(32,16,0,.72);margin:0 0 22px}
.crumb a{color:rgba(32,16,0,.72)}
.d-meta{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:20px}
.d-category{font:600 12px "Azeret Mono",ui-monospace,monospace;color:var(--teal-ink);letter-spacing:.04em}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 9px;border-radius:999px;
  font-size:11px;font-weight:750;line-height:1;white-space:nowrap}
.badge::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.badge.no-signup{color:var(--green);background:var(--green-soft)}
.badge.free-account{color:var(--blue);background:var(--blue-soft)}
.badge.caution{color:var(--amber);background:var(--amber-soft)}
.d-hero h1{margin:0 0 10px;max-width:640px;font-size:clamp(32px,5vw,48px);line-height:.98;
  letter-spacing:-.05em;font-weight:800}
.d-tagline{margin:0;max-width:590px;color:rgba(32,16,0,.82);font-size:17px;line-height:1.45}
.d-actions{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.quick-btn{display:inline-flex;align-items:center;gap:6px;padding:10px 14px;background:var(--white);
  border:1.5px solid var(--line);border-radius:10px;cursor:pointer;font-size:13px;font-weight:700;
  color:var(--ink);text-decoration:none;font-family:inherit}
.quick-btn:hover{border-color:var(--ink)}
.quick-btn[aria-pressed="true"]{background:transparent;border-color:var(--teal);color:var(--teal)}
.quick-btn svg{flex:none}
/* ---- dark body sections ---- */
.d-body{padding:36px 20px 60px}
.d-body section{margin-bottom:38px}
.d-body h2{margin:0 0 13px;font-size:25px;letter-spacing:-.03em;font-weight:800}
.d-desc{color:var(--ink);font-size:17px;line-height:1.62;margin:0}
.use-list{display:grid;gap:9px;padding:0;margin:0;list-style:none}
.use-list li{position:relative;padding-left:27px;color:var(--ink)}
.use-list li::before{content:"\\2713";position:absolute;left:0;top:0;color:var(--green);font-weight:800}
.d-setup{display:grid;gap:0;overflow:hidden;border:1.5px solid var(--line);border-radius:20px;background:var(--white)}
.d-step{display:grid;grid-template-columns:42px 1fr;gap:14px;padding:22px;border-bottom:1px solid var(--line)}
.d-step:last-child{border-bottom:0}
.d-num{display:grid;place-items:center;align-self:start;width:36px;height:36px;border-radius:50%;
  background:var(--teal);border:0;color:var(--teal-ink);font:600 13px "Azeret Mono",ui-monospace,monospace}
.d-step h3{margin:3px 0 5px;font-size:19px;font-weight:700}
.d-step p{margin:0;color:var(--muted);font-size:14px}
.primary-link{display:inline-flex;align-items:center;gap:7px;margin-top:13px;padding:10px 14px;
  border:2px solid var(--teal);border-radius:10px;background:var(--white);box-shadow:none;
  color:var(--teal);text-decoration:none;font-weight:750}
.primary-link:active{transform:translate(1px,1px);box-shadow:2px 2px 0 var(--teal)}
.provider-steps{margin:12px 0 0;padding-left:20px;color:var(--ink);font-size:14px}
.provider-steps li{margin-bottom:7px;overflow-wrap:anywhere}
.agent-message{position:relative;margin-top:12px;padding:16px 96px 16px 15px;border-radius:11px;
  background:rgba(255,107,26,.10);color:var(--ink);font:500 12px/1.55 "Azeret Mono",ui-monospace,monospace;
  overflow-wrap:anywhere;white-space:pre-wrap}
.copy-btn{position:absolute;right:9px;top:9px;padding:8px 10px;border:0;border-radius:8px;
  background:var(--teal);color:var(--teal-ink);cursor:pointer;font:600 11px "Azeret Mono",ui-monospace,monospace}
.key-note{display:flex;gap:9px;margin-top:11px !important;color:var(--amber) !important}
.d-example pre{margin:0;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;
  padding:18px;border-radius:14px;background:#050707;border:1px solid var(--line);
  color:#f5f7f5;font:500 13px/1.6 "Azeret Mono",ui-monospace,monospace}
.d-fine{display:grid;gap:10px}
.d-fact{background:var(--white);border:1px solid var(--line);border-radius:12px;padding:13px 16px}
.d-fact b{display:block;font:600 11px "Azeret Mono",ui-monospace,monospace;color:var(--muted);
  text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px}
.d-fact span{font-size:15px;color:var(--ink)}
details{border-top:1.5px solid var(--line);padding-top:24px}
summary{cursor:pointer;font-size:19px;font-weight:700;letter-spacing:-.02em}
.d-adv{margin-top:14px;display:flex;flex-wrap:wrap;gap:10px}
.verified{font-size:13px;color:var(--muted);margin:26px 0 0}
footer{border-top:1px solid var(--line);margin-top:0;padding:22px 0 40px;font-size:13px;color:var(--muted)}
footer a{color:var(--muted)}
@media (max-width:620px){
  .cnav{display:none}
  .d-hero{padding:40px 0 28px}
  .d-hero h1{font-size:40px}
  .d-step{grid-template-columns:34px 1fr;gap:11px;padding:17px 14px}
  .d-num{width:32px;height:32px}
  .agent-message{padding:14px 14px 55px}
  .copy-btn{top:auto;bottom:9px;left:9px;right:auto}
}
"""


def render_page(api, slug):
    name = esc(api.get("name"))
    name_js = json.dumps(api.get("name"), ensure_ascii=False)
    category = esc(api.get("category"))
    tagline = esc(api.get("tagline"))
    desc = esc(api.get("description"))
    page_url = f"{BASE}/api/{slug}/"
    docs = clean_url(api.get("docs_url"))
    signup = clean_url(api.get("signup_url"))
    auth = api.get("auth") or ""
    no_key = auth == "No key"
    label = effort_label(auth)
    badge_cls = effort_class(label)
    kind = "tool" if api.get("category") in NON_API_CATS else "API"
    title = f"{api.get('name')} | Free {kind} on PlugMyAgent"
    description = meta_desc(api)

    hero_extra, hero_style = "", ""
    if api.get("hero_img"):
        hero_extra = " has-img"
        hero_style = (f' style="background-image:linear-gradient(180deg, rgba(5,7,7,.60) 0%, '
                      f'rgba(5,7,7,.88) 100%), url(/{esc(api.get("hero_img"))})"')

    use_cases = "".join(f"<li>{esc(u)}</li>" for u in (api.get("use_cases") or []))
    use_section = ""
    if use_cases:
        use_section = f"""<section>
<h2>What you can do with it</h2>
<ul class="use-list">{use_cases}</ul>
</section>"""

    # Step 1: open the guide / get free access
    guide_url = signup or docs
    if no_key:
        s1_h, s1_p = "Open the official guide", "This API works without an account or key. Open the guide to see what it offers."
        s1_link_text = f"Open {api.get('name')} docs \u2197"
    else:
        s1_h, s1_p = "Get free access", "Open the provider's signup page and make a free account."
        s1_link_text = f"Sign up for {api.get('name')} \u2197"
    s1_link = (f'<a class="primary-link" href="{esc(guide_url)}" rel="noopener">{esc(s1_link_text)}</a>'
               if guide_url else "")

    # Step 2: quick-start / copy key
    if no_key:
        s2_h = "Follow the quick-start steps"
        s2_p = "Use the provider's instructions below. There's no secret key to manage."
    else:
        s2_h = "Copy your API key"
        s2_p = "After signing up, look in the dashboard or settings for your API key, then copy it. The provider-specific steps are below."
    provider_steps = "".join(
        f"<li>{esc(re.sub(r'^\\d+\\.\\s*', '', s))}</li>"
        for s in (api.get("setup_steps") or []))
    provider_html = f'<ol class="provider-steps">{provider_steps}</ol>' if provider_steps else ""

    # Step 3: tell your agent (composed at build time)
    prompt = agent_prompt(api)
    key_note = ""
    if not no_key:
        key_note = '<p class="key-note">Keep API keys private. Only share yours with tools and people you trust.</p>'

    example = ""
    if api.get("example"):
        example = (f'<section class="d-example"><h2>Example request</h2>'
                   f'<pre>{esc(normalize_example(api.get("example")))}</pre></section>')

    best = ", ".join(esc(b) for b in (api.get("best_for") or []))
    fine_pairs = [("Access", esc(auth)), ("Rate limit", esc(api.get("rate_limit"))),
                  ("Best for", best), ("Category", category)]
    fine_facts = "".join(
        f'<div class="d-fact"><b>{k}</b><span>{v}</span></div>'
        for k, v in fine_pairs if v)

    adv_links = ""
    if docs:
        adv_links += f'<a class="primary-link" href="{esc(docs)}" rel="noopener">Official docs \u2197</a>'
    if signup and signup != docs:
        adv_links += f'<a class="primary-link" href="{esc(signup)}" rel="noopener">Signup page \u2197</a>'

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
        "@type": "SoftwareApplication" if kind == "tool" else "WebAPI",
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
<meta property="og:title" content="{name} - free {kind}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} - free {kind}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="stylesheet" href="/api-pages.css">
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<div class="site-header"><div class="site-header-inner"><a class="brandmark" href="/" aria-label="PlugMyAgent home"><img src="/plug-lockup-v2.png" alt="PlugMyAgent"></a><nav class="cnav" aria-label="Primary"><a href="/catalog/">Catalog</a><a href="/mcp/">MCP</a><a href="/components/">Components</a><a href="/guides/">Guides</a></nav><a class="cart-link" href="/stack/" aria-label="My stack"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.6"/><circle cx="17" cy="20" r="1.6"/><path d="M2.5 3.5h2.6l2.5 12.2a1.5 1.5 0 0 0 1.5 1.2h7.9a1.5 1.5 0 0 0 1.5-1.2L20.5 7H6"/></svg><span class="cart-count" data-cart-count style="display:none">0</span></a></div></div>
<div class="d-hero{hero_extra}"{hero_style}>
<div class="wrap">
<p class="crumb"><a href="/">Home</a> / <a href="/catalog/">Catalog</a> / {category} / {name}</p>
<div class="d-meta"><span class="d-category">{category}</span><span class="badge {badge_cls}">{label}</span></div>
<h1>{name}</h1>
<p class="d-tagline">{tagline}</p>
<div class="d-actions">
<button class="quick-btn" id="stackBtn" type="button" aria-pressed="false">+ Stack</button>
<button class="quick-btn" id="shareBtn" type="button" aria-label="Share {name}"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M5 12v8h14v-8"/></svg><span>Share</span></button>
</div>
</div>
</div>
<main class="wrap d-body">
<section>
<h2>What it does</h2>
<p class="d-desc">{desc}</p>
</section>
{use_section}
<section>
<h2>Set it up</h2>
<div class="d-setup">
<div class="d-step"><span class="d-num">1</span><div>
<h3>{s1_h}</h3><p>{s1_p}</p>{s1_link}
</div></div>
<div class="d-step"><span class="d-num">2</span><div>
<h3>{s2_h}</h3><p>{s2_p}</p>{provider_html}
</div></div>
<div class="d-step"><span class="d-num">3</span><div>
<h3>Tell your agent</h3><p>Copy the message, paste it into ChatGPT, Claude, Grok, or a similar agent. No code needed. Replace PASTE_KEY_HERE with your key first. Your agent will either set it up directly or hand you the exact command to run.</p>
<div class="agent-message"><span id="agentMsg">{esc(prompt)}</span><button class="copy-btn" id="copyMsg" type="button">Copy</button></div>
{key_note}
</div></div>
</div>
</section>
{example}
<section>
<h2>The fine print</h2>
<div class="d-fine">{fine_facts}</div>
</section>
<details><summary>For advanced users</summary><div class="d-adv">{adv_links}</div></details>
{verified_line}
</main>
<footer><div class="wrap">
<a href="/">PlugMyAgent</a> - every listing free to start. &copy; 2026 hiddeninwest
</div></footer>
<script>
(function(){{
var b=document.getElementById('shareBtn');if(!b)return;
function fallback(u,btn){{var t=document.createElement('textarea');t.value=u;document.body.appendChild(t);
t.select();try{{document.execCommand('copy');}}catch(e){{}}t.remove();
var o=btn.querySelector('span').textContent;btn.querySelector('span').textContent='Copied';
setTimeout(function(){{btn.querySelector('span').textContent=o;}},1600);}}
b.addEventListener('click',function(){{
var u=document.querySelector('link[rel="canonical"]').href;
if(navigator.share){{navigator.share({{title:document.title,url:u}}).then(function(){{}},function(err){{
if(err&&err.name==='AbortError')return;fallback(u,b);}});return;}}
fallback(u,b);}});}})();
(function(){{
var KEY='plugmyagent_stack_v1',NAME={name_js};
function read(){{try{{var v=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v:[];}}catch(e){{return [];}}}}
function write(a){{try{{localStorage.setItem(KEY,JSON.stringify(a));}}catch(e){{}}document.dispatchEvent(new CustomEvent('pma:stack'));}}
function paint(){{var n=read().length;var els=document.querySelectorAll('[data-cart-count]');for(var i=0;i<els.length;i++){{var b=els[i];b.textContent=n;b.style.display=n>0?'':'none';}}}}
function paintBtn(){{var b=document.getElementById('stackBtn');if(!b)return;var has=read().indexOf(NAME)>=0;b.textContent=has?'\u2713 In stack':'+ Stack';b.setAttribute('aria-pressed',String(has));}}
var sb=document.getElementById('stackBtn');
if(sb){{sb.addEventListener('click',function(){{var s=read();var i=s.indexOf(NAME);if(i>=0){{s.splice(i,1);}}else{{s.push(NAME);}}write(s);paintBtn();}});}}
document.addEventListener('pma:stack',function(){{paint();paintBtn();}});
window.addEventListener('storage',function(e){{if(e.key===KEY){{paint();paintBtn();}}}});
paint();paintBtn();}})();
(function(){{
var c=document.getElementById('copyMsg');if(!c)return;
c.addEventListener('click',function(){{
var t=document.getElementById('agentMsg').textContent;
function done(){{var o=c.textContent;c.textContent='Copied';setTimeout(function(){{c.textContent=o;}},1800);}}
function fallback(){{var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);
ta.select();try{{document.execCommand('copy');}}catch(e){{}}ta.remove();done();}}
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(done,function(){{fallback();}});}}
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

    urls = ([BASE + "/", BASE + "/catalog/", BASE + "/stack/", BASE + "/mcp/",
             BASE + "/components/"] + [f"{BASE}/api/{s}/" for s in slugs])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8"
    )
    (ROOT / "api-pages.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    print(f"Wrote {count} API pages + sitemap.xml + robots.txt + api-pages.css")


if __name__ == "__main__":
    main()
