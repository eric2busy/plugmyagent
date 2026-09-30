#!/usr/bin/env python3
"""Generate build/stack/index.html, the My Stack cart page.

Reads the master catalog, embeds the API data as JSON (same pattern as the
catalog page), and renders a cart-style page: line items with reorder/remove,
a summary panel, and the Copy combined setup checkout action.

Usage: python3 build/tools/generate-stack-page.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
MASTER = os.path.expanduser("~/workspace/api-catalog/master-list.json")
OUT_DIR = os.path.join(BUILD, "stack")
OUT = os.path.join(OUT_DIR, "index.html")

CART_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="9" cy="20" r="1.6"/><circle cx="17" cy="20" r="1.6"/>'
    '<path d="M2.5 3.5h2.6l2.5 12.2a1.5 1.5 0 0 0 1.5 1.2h7.9a1.5 1.5 0 0 0 1.5-1.2L20.5 7H6"/></svg>'
)

CART_CSS = """
.cart-link{position:relative;display:inline-flex;align-items:center;color:var(--ink);text-decoration:none;padding:8px;margin-left:6px;border-radius:10px}
.cart-link:hover{color:var(--yellow)}
.cart-link svg{width:22px;height:22px;display:block}
.cart-count{position:absolute;top:1px;right:-2px;min-width:18px;height:18px;border-radius:999px;background:var(--yellow);color:#14100a;font:700 11px/18px "Azeret Mono",ui-monospace,monospace;text-align:center;padding:0 4px}
.cart-link[aria-current="page"]{color:var(--yellow)}
"""

CART_JS = """
(function(){
  var KEY = "plugmyagent_stack_v1";
  function read(){ try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v : []; } catch (_) { return []; } }
  function write(a){ try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (_) {} document.dispatchEvent(new CustomEvent("pma:stack")); }
  function paint(){ var n = read().length;
    document.querySelectorAll("[data-cart-count]").forEach(function(b){ b.textContent = n; b.style.display = n > 0 ? "" : "none"; }); }
  window.PMA = window.PMA || {};
  PMA.stackKey = KEY; PMA.stackRead = read; PMA.stackWrite = write; PMA.paintCart = paint;
  document.addEventListener("pma:stack", paint);
  window.addEventListener("storage", function(e){ if (e.key === KEY) paint(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", paint); else paint();
})();
"""

GOALS_JS = """    const GOALS = [
      { label: "Everything", categories: [] },
      { label: "Send messages & alerts", categories: ["Messaging & Chat", "Push Notifications", "Email", "Voice & Video"] },
      { label: "Organize my life", categories: ["Calendars & Scheduling", "Task & Project Tools", "Forms", "Automation", "Business Operations", "Smart Home"] },
      { label: "Weather", categories: ["Weather", "Environment & Climate"] },
      { label: "Maps, travel & getting around", categories: ["Maps & Geocoding", "Routing", "Transit", "Flights", "Travel", "Time & Location"] },
      { label: "News & web search", categories: ["News", "Web Search", "Social & Community", "Scraping & Extraction", "Marketing & SEO"] },
      { label: "Movies, music & fun", categories: ["Movies & TV", "Anime", "Music", "Podcasts", "Games", "Sports", "Fun & Random", "Avatars & Images"] },
      { label: "Money & markets", categories: ["Stocks", "Crypto", "FX & Currency", "Economic Data", "Blockchain", "Payments Dev", "Banking & Budgeting"] },
      { label: "Health, food & science", categories: ["Nutrition & Food", "Fitness", "Medical & Drug Info", "Science Data", "Scholarly", "Books & Learning"] },
      { label: "Government, jobs & civic", categories: ["US Government Data", "Civic & Legal", "Jobs & Careers"] },
      { label: "Safety & networks", categories: ["Threat Intel", "Network & IP Intel", "Auth & Identity"] },
      { label: "Build & code", categories: ["Code & Repos", "Dev Utilities", "Databases", "Hosting & Cloud", "AI & ML", "Audio & Speech", "Images & Media", "Link Tools", "Ecommerce Dev", "Utilities"] }
    ];
    const GOAL_TESTS = {
      "Send messages & alerts": "have it send you the message \\u201cplugmyagent test\\u201d",
      "Organize my life": "have it create an item called \\u201cplugmyagent test\\u201d, then delete it",
      "Weather": "ask it: \\u201cwhat's the weather in Covina, California right now?\\u201d",
      "Maps, travel & getting around": "ask it to look up an address you know well",
      "News & web search": "ask it for today's top headlines",
      "Movies, music & fun": "ask it to look something up for you",
      "Money & markets": "ask it: \\u201cwhat's the price of Bitcoin in USD?\\u201d",
      "Health, food & science": "ask it to look up one item you know",
      "Government, jobs & civic": "ask it to find one real record for you",
      "Safety & networks": "ask it to check a domain or IP address you know",
      "Build & code": "ask it to fetch one small thing, like a repo or a fresh UUID"
    };
    const AUTH_HOW = {
      "Telegram Bot API": "Your bot token goes right in the URL where the example shows it.",
      "Discord Webhooks": "No separate key. Your webhook URL (Discord channel settings \\u2192 Integrations \\u2192 Webhooks) is the secret. Swap your full URL in for the example.",
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
      "Google Calendar API": "Uses Google OAuth 2.0 (not a simple key). Follow the setup steps above; your agent will need the OAuth credentials."
    };
    function normalizeExample(example) {
      return String(example || "")
        .replace(/<YOUR_API_KEY>/gi, "PASTE_KEY_HERE")
        .replace(/<API_KEY>/gi, "PASTE_KEY_HERE")
        .replace(/\\{api_key\\}/gi, "PASTE_KEY_HERE")
        .replace(/<TOKEN>/g, "PASTE_KEY_HERE")
        .replace(/<token>/g, "PASTE_KEY_HERE")
        .replace(/\\bYOUR_API_KEY\\b/g, "PASTE_KEY_HERE")
        .replace(/\\bYOUR_KEY\\b/g, "PASTE_KEY_HERE")
        .replace(/YOUR_KEYSTRING/g, "PASTE_KEY_HERE")
        .replace(/sk_test_YOUR_KEY/g, "sk_test_PASTE_KEY_HERE")
        .replace(/_YOUR_KEY/g, "_PASTE_KEY_HERE")
        .replace(/YOUR_APP_TOKEN/g, "PASTE_KEY_HERE");
    }
    function testFor(api) {
      const goal = GOALS.find(g => g.categories.includes(api.category));
      const t = goal && GOAL_TESTS[goal.label];
      return t || "try one small real request to confirm it works";
    }
    function agentPrompt(api) {
      const noKey = api.auth === "No key";
      const lines = [];
      lines.push(`Set up ${api.name} for me so you can use it.`);
      lines.push("");
      lines.push("HOW TO CALL IT");
      lines.push(normalizeExample(api.example));
      lines.push("");
      if (noKey) {
        lines.push("AUTH: none needed. No signup, no key.");
      } else {
        lines.push("AUTH: free API key. Mine: PASTE_KEY_HERE.");
        lines.push(AUTH_HOW[api.name] || "Put it where the example above shows (usually an Authorization header or a key in the URL).");
        if (api.auth === "Free tier (card may be required)") lines.push("Heads up: signup may ask for a card.");
        if (api.auth === "Free trial") lines.push("Heads up: this is a free trial. Check how long it lasts.");
      }
      lines.push("");
      lines.push(`FREE LIMIT: ${api.rate_limit}`);
      lines.push("");
      lines.push(`TEST: once it's set up, ${testFor(api)}.`);
      lines.push(`If you can't make web requests yourself, give me the exact curl command with my key filled in so I can run it.`);
      lines.push("");
      lines.push(`Docs if you get stuck: ${api.docs_url}`);
      return lines.join("\\n");
    }
"""


def api_count_copy():
    """Public count copy per the standing threshold rule: floor(n/50)*50 with '+'.
    485 -> '450+', 500 -> '500+', 550 -> '550+'. Never an exact number."""
    with open(os.path.join(BUILD, "api-catalog.json"), encoding="utf-8") as f:
        n = len(json.load(f))
    return f"{(n // 50) * 50}+"


def esc_js(s):
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")


def main():
    with open(MASTER, encoding="utf-8") as f:
        apis = json.load(f)
    apis_json = json.dumps(apis, ensure_ascii=False).replace("</script", "<\\/script")

    head = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="color-scheme" content="dark" />
  <meta name="theme-color" content="#0b0d0d" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='4' y='29' width='18' height='6' rx='3' fill='%23ff6b1a'/%3E%3Cpolygon points='20,27 32,21 32,43 20,37' fill='%23ff6b1a'/%3E%3Crect x='30' y='19' width='14' height='26' rx='4' fill='%23ff6b1a'/%3E%3Crect x='44' y='22' width='16' height='20' rx='2' fill='%23ff6b1a'/%3E%3C/svg%3E" />
  <title>My Stack | PlugMyAgent</title>
  <meta name="description" content="Your saved stack of free APIs on PlugMyAgent. Review what you picked, then copy one combined setup prompt and hand it to your AI agent." />
  <link rel="canonical" href="https://www.plugmyagent.com/stack/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="PlugMyAgent" />
  <meta property="og:title" content="My Stack | PlugMyAgent" />
  <meta property="og:description" content="Your saved stack of free APIs. Copy one combined setup prompt and hand it to your AI agent." />
  <meta property="og:url" content="https://www.plugmyagent.com/stack/" />
  <meta property="og:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="PlugMyAgent: 400+ free APIs to supercharge your AI agent" />
  <meta name="twitter:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="My Stack | PlugMyAgent" />
  <meta name="twitter:description" content="Your saved stack of free APIs. Copy one combined setup prompt and hand it to your AI agent." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #f5f7f5;
      --muted: #9aa39e;
      --paper: #0b0d0d;
      --white: #101314;
      --line: rgba(255,255,255,.09);
      --yellow: #ff6b1a;
      --yellow-soft: rgba(255,107,26,.14);
      --coral: #ff8a70;
      --coral-soft: rgba(255,138,112,.14);
      --green: #4ade80;
      --green-soft: rgba(74,222,128,.12);
      --blue: #7fb5ec;
      --blue-soft: rgba(127,181,236,.12);
      --shadow: 0 22px 60px rgba(0,0,0,.55);
      --radius-lg: 28px;
      --radius-md: 18px;
      --radius-sm: 12px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; background: #0b0d0d; color-scheme: dark; overflow-x: clip; }
    body {
      margin: 0; overflow-x: clip; background: #0b0d0d; color: var(--ink);
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 16px; line-height: 1.5; -webkit-font-smoothing: antialiased;
    }
    button, input { font: inherit; }
    button, a { -webkit-tap-highlight-color: transparent; }
    button { color: inherit; }
    a { color: inherit; }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
    h1, h2, h3 { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }

    .site-header { position: sticky; top: 0; z-index: 40; background: rgba(11,13,13,.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
    .site-header-inner { width: min(1120px, 100%); margin: 0 auto; padding: 11px clamp(16px, 4vw, 32px); display: flex; align-items: center; justify-content: space-between; min-height: 56px; position: relative; }
    .brandmark { display: inline-flex; align-items: center; }
    .brandmark img { display: block; height: 26px; width: auto; }
    .header-right { display: flex; align-items: center; }
    .cnav { display: flex; gap: 26px; align-items: center; }
    .cnav a { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color .18s; }
    .cnav a:hover { color: var(--yellow); }
    .burger { display: none; background: none; border: 0; cursor: pointer; padding: 12px 2px 12px 14px; }
    .burger span { display: block; width: 22px; height: 2px; border-radius: 2px; background: var(--ink); margin: 5px 0; transition: transform .2s, opacity .2s, background .2s; }
    .burger:hover span { background: var(--yellow); }
    .burger[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); background: var(--yellow); }
    .burger[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
    .burger[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); background: var(--yellow); }
    .mnav { display: none; }
    @media (max-width: 760px) {
      .cnav { display: none; }
      .burger { display: block; }
      .mnav { display: block; position: absolute; top: calc(100% + 8px); right: 16px; min-width: 230px; z-index: 60;
        background: var(--white); border: 1px solid var(--line); border-radius: 12px; padding: 8px; box-shadow: var(--shadow);
        opacity: 0; transform: translateY(-6px); pointer-events: none; transition: opacity .18s, transform .18s; }
      .mnav.open { opacity: 1; transform: none; pointer-events: auto; }
      .mnav a { display: block; padding: 12px 14px; border-radius: 8px;
        font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
        color: var(--muted); text-decoration: none; }
      .mnav a:hover { background: var(--yellow-soft); color: var(--yellow); }
    }
""" + CART_CSS + """
    .page { min-height: 100vh; overflow: clip; background: var(--paper); position: relative; z-index: 1; }
    body::before { content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
      background-size: 56px 56px;
      mask-image: radial-gradient(ellipse 90% 70% at 50% 0%, black 30%, transparent 100%);
      -webkit-mask-image: radial-gradient(ellipse 90% 70% at 50% 0%, black 30%, transparent 100%); }
    .wrap { width: min(1120px, 100%); margin: 0 auto; padding: 0 clamp(16px, 4vw, 32px); position: relative; }
    .page-head { padding: 52px 0 8px; }
    .kicker { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px; letter-spacing: .18em; text-transform: uppercase; color: var(--yellow); margin: 0 0 10px; }
    .page-head h1 { font-size: clamp(30px, 4.4vw, 44px); letter-spacing: -.03em; margin: 0 0 8px; font-weight: 800; }
    .page-head p { color: var(--muted); margin: 0; max-width: 560px; font-size: 16px; }

    .stack-layout { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 28px; padding: 32px 0 80px; align-items: start; }
    @media (max-width: 900px) { .stack-layout { grid-template-columns: 1fr; } .summary { position: static; } }

    .stack-items { display: flex; flex-direction: column; gap: 14px; margin: 0; padding: 0; list-style: none; }
    .stack-item { display: flex; gap: 16px; align-items: center; background: var(--white); border: 1px solid var(--line);
      border-radius: var(--radius-md); padding: 14px 16px; }
    .stack-thumb { flex: 0 0 72px; width: 72px; height: 72px; border-radius: 12px; overflow: hidden; background: linear-gradient(135deg, #ff6b1a, #b33c00);
      display: grid; place-items: center; }
    .stack-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .stack-thumb svg { width: 30px; height: 30px; color: rgba(20,16,10,.75); }
    .stack-info { flex: 1; min-width: 0; }
    .stack-info h3 { margin: 0 0 2px; font-size: 17px; letter-spacing: -.01em; }
    .stack-info h3 a { text-decoration: none; }
    .stack-info h3 a:hover { color: var(--yellow); }
    .stack-info .tag { color: var(--muted); font-size: 14px; margin: 0 0 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .chips { display: flex; flex-wrap: wrap; gap: 6px; }
    .chip { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
      border: 1px solid var(--line); border-radius: 999px; padding: 3px 10px; color: var(--muted); }
    .chip.key { color: var(--green); border-color: rgba(74,222,128,.35); }
    .chip.nokey { color: var(--blue); border-color: rgba(127,181,236,.35); }
    .stack-actions { display: flex; flex-direction: column; gap: 4px; align-items: center; }
    .icon-btn { background: none; border: 1px solid transparent; border-radius: 8px; color: var(--muted); cursor: pointer;
      width: 30px; height: 26px; display: grid; place-items: center; font-size: 14px; line-height: 1; }
    .icon-btn:hover { color: var(--ink); border-color: var(--line); background: rgba(255,255,255,.04); }
    .icon-btn.remove:hover { color: var(--coral); border-color: rgba(255,138,112,.4); }
    .icon-btn:disabled { opacity: .25; cursor: default; }
    .icon-btn:disabled:hover { color: var(--muted); border-color: transparent; background: none; }
    .stack-links { display: flex; gap: 8px; margin-top: 10px; }
    .mini-link { font-size: 13px; color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--line); padding-bottom: 1px; }
    .mini-link:hover { color: var(--yellow); border-color: var(--yellow); }

    .summary { position: sticky; top: 84px; background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 22px; }
    .summary h2 { margin: 0 0 14px; font-size: 19px; letter-spacing: -.01em; }
    .sum-row { display: flex; justify-content: space-between; align-items: baseline; padding: 8px 0; border-bottom: 1px dashed var(--line); font-size: 14.5px; }
    .sum-row:last-of-type { border-bottom: 0; }
    .sum-row b { font-family: "Azeret Mono", ui-monospace, monospace; font-weight: 600; }
    .sum-row .dim { color: var(--muted); }
    .btn-checkout { display: block; width: 100%; margin-top: 16px; padding: 14px 18px; border-radius: 12px; border: 0; cursor: pointer;
      background: var(--yellow); color: #14100a; font-weight: 800; font-size: 15.5px; text-align: center; }
    .btn-checkout:hover { filter: brightness(1.08); }
    .btn-ghost { display: block; width: 100%; margin-top: 10px; padding: 12px 18px; border-radius: 12px; cursor: pointer;
      background: transparent; border: 1px solid var(--line); color: var(--muted); font-weight: 600; font-size: 14px; }
    .btn-ghost:hover { color: var(--coral); border-color: rgba(255,138,112,.4); }
    .browse-link { display: block; text-align: center; margin-top: 14px; font-size: 14px; color: var(--muted); }
    .browse-link:hover { color: var(--yellow); }
    .fine { margin-top: 14px; font-size: 12.5px; color: var(--muted); }

    .empty { text-align: center; padding: 70px 20px 90px; }
    .empty svg { width: 64px; height: 64px; color: var(--muted); opacity: .6; margin-bottom: 18px; }
    .empty h2 { font-size: 26px; margin: 0 0 8px; letter-spacing: -.02em; }
    .empty p { color: var(--muted); max-width: 440px; margin: 0 auto 24px; }
    .btn-primary { display: inline-block; padding: 14px 26px; border-radius: 12px; background: var(--yellow); color: #14100a;
      font-weight: 800; font-size: 15.5px; text-decoration: none; }
    .btn-primary:hover { filter: brightness(1.08); }

    footer { border-top: 1px solid var(--line); }
    .footer-inner { width: min(1120px, 100%); margin: 0 auto; padding: 34px clamp(16px, 4vw, 32px) 46px; color: var(--muted); font-size: 14px; }
    .footer-inner strong { color: var(--ink); display: block; margin-bottom: 6px; }
    .footer-trust { margin: 10px 0 0; }
    .footer-credit { display: flex; align-items: center; gap: 10px; margin-top: 18px; font-size: 13px; }
    .footer-sep { opacity: .5; }
    .footer-credit svg { width: 15px; height: 15px; fill: currentColor; display: block; }
    .footer-credit a:hover { color: var(--yellow); }
  </style>
</head>
<body>
<div class="page">
  <div class="site-header"><div class="site-header-inner">
    <a class="brandmark" href="/" aria-label="PlugMyAgent home"><img src="/plug-lockup-v2.png" alt="PlugMyAgent"></a>
    <div class="header-right">
      <nav class="cnav" aria-label="Primary">
        <a href="/catalog/">Catalog</a><a href="/mcp/">MCP</a><a href="/components/">Components</a><a href="/guides/">Guides</a><a href="/#pillars">Tools</a>
      </nav>
      <a class="cart-link" href="/stack/" aria-label="My stack" aria-current="page">""" + CART_SVG + """<span class="cart-count" data-cart-count style="display:none">0</span></a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
      <nav class="mnav" id="mnav" aria-label="Mobile">
        <a href="/catalog/">API Catalog</a><a href="/mcp/">MCP</a><a href="/components/">Components</a><a href="/guides/">Guides</a><a href="/#pillars">Tools</a><a href="/stack/">My Stack</a>
      </nav>
    </div>
  </div></div>

  <main class="wrap">
    <div class="page-head">
      <p class="kicker">Saved for later</p>
      <h1>My Stack</h1>
      <p id="pageSub">Your hand-picked APIs, ready to plug into your agent.</p>
    </div>
    <div id="stackWrap"></div>
  </main>

  <footer>
    <div class="footer-inner"><strong>450+ listings, checked against official documentation on September 19, 2026.</strong> Free plans can change, so double-check the official docs before building something you rely on.
      <p class="footer-trust">Your API keys never touch our servers. They go straight from you to your agent.</p>
      <div class="footer-credit"><span>&copy; 2026 hiddeninwest</span><span class="footer-sep" aria-hidden="true">&middot;</span><a href="mailto:contact@plugmyagent.com">contact@plugmyagent.com</a><span class="footer-sep" aria-hidden="true">&middot;</span><a href="https://x.com/hiddeninwest" target="_blank" rel="noopener" aria-label="hiddeninwest on X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.451-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg></a></div>
    </div>
  </footer>
</div>

<script>
""" + CART_JS + """
(function(){
  const APIS = %%APIS_JSON%%;

  function slugify(name) {
    return ((name || "api").toLowerCase().normalize("NFKD").replace(/[\\u0300-\\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "")) || "api";
  }
  const slugToApi = {};
  const apiToSlug = new Map();
  APIS.forEach(api => {
    const base = slugify(api.name);
    let slug = base, n = 2;
    while (slugToApi[slug]) slug = base + "-" + (n++);
    slugToApi[slug] = api;
    apiToSlug.set(api, slug);
  });
  const byName = new Map(APIS.map(a => [a.name, a]));

  function esc(s){ return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

""" + GOALS_JS + """
  function stackPrompt(apis) {
    const parts = apis.map(a => {
      const body = agentPrompt(a).split("\\n").slice(2).join("\\n");
      return `--- ${a.name} ---\\n${body}`;
    });
    return `Set up each of these ${apis.length} APIs for me so you can use them. One section per API:\\n\\n${parts.join("\\n\\n")}`;
  }
  async function copyText(text, btn) {
    try { await navigator.clipboard.writeText(text); }
    catch (_) {
      const area = document.createElement("textarea");
      area.value = text; document.body.append(area); area.select();
      document.execCommand("copy"); area.remove();
    }
    const original = btn.textContent;
    btn.textContent = "Copied";
    setTimeout(() => { btn.textContent = original; }, 1800);
  }

  const wrap = document.getElementById("stackWrap");
  const pageSub = document.getElementById("pageSub");

  function getStack(){ return PMA.stackRead(); }
  function setStack(a){ PMA.stackWrite(a); render(); }

  function move(name, dir){
    const s = getStack();
    const i = s.indexOf(name);
    const j = i + dir;
    if (i < 0 || j < 0 || j >= s.length) return;
    const t = s[i]; s[i] = s[j]; s[j] = t;
    setStack(s);
  }
  function removeItem(name){ setStack(getStack().filter(n => n !== name)); }
  function clearStack(){ if (confirm("Remove everything from your stack?")) setStack([]); }

  function thumbHtml(api){
    if (api.hero_img) return `<span class="stack-thumb"><img src="/${esc(api.hero_img)}" alt="" loading="lazy"></span>`;
    return `<span class="stack-thumb">` + %%CART_SVG_JS%% + `</span>`;
  }

  function render(){
    const names = getStack();
    const apis = names.map(n => byName.get(n)).filter(Boolean);
    const missing = names.length - apis.length;
    if (missing > 0) {
      setStack(apis.map(a => a.name));
      return;
    }
    if (!apis.length) { renderEmpty(); PMA.paintCart(); return; }

    pageSub.textContent = apis.length === 1
      ? "One API in your stack, ready to plug into your agent."
      : `${apis.length} APIs in your stack, ready to plug into your agent.`;

    const noKey = apis.filter(a => a.auth === "No key").length;
    const needKey = apis.length - noKey;

    const items = apis.map((api, i) => {
      const slug = apiToSlug.get(api);
      const keyChip = api.auth === "No key"
        ? `<span class="chip nokey">No signup</span>`
        : `<span class="chip key">Free key</span>`;
      return `<li class="stack-item" data-name="${esc(api.name)}">
        ${thumbHtml(api)}
        <div class="stack-info">
          <h3><a href="/api/${slug}/">${esc(api.name)}</a></h3>
          <p class="tag">${esc(api.tagline)}</p>
          <div class="chips"><span class="chip">${esc(api.category)}</span>${keyChip}</div>
          <div class="stack-links">
            <a class="mini-link" href="/api/${slug}/">Details</a>
            ${api.docs_url ? `<a class="mini-link" href="${esc(api.docs_url)}" rel="noopener">Docs</a>` : ""}
          </div>
        </div>
        <div class="stack-actions">
          <button class="icon-btn" data-act="up" aria-label="Move ${esc(api.name)} up" ${i === 0 ? "disabled" : ""}>&#9650;</button>
          <button class="icon-btn" data-act="down" aria-label="Move ${esc(api.name)} down" ${i === apis.length - 1 ? "disabled" : ""}>&#9660;</button>
          <button class="icon-btn remove" data-act="remove" aria-label="Remove ${esc(api.name)} from stack">&times;</button>
        </div>
      </li>`;
    }).join("");

    wrap.innerHTML = `
      <div class="stack-layout">
        <ul class="stack-items">${items}</ul>
        <aside class="summary" aria-label="Stack summary">
          <h2>Stack summary</h2>
          <div class="sum-row"><span class="dim">APIs in stack</span><b>${apis.length}</b></div>
          <div class="sum-row"><span class="dim">No signup needed</span><b>${noKey}</b></div>
          <div class="sum-row"><span class="dim">Need a free key</span><b>${needKey}</b></div>
          <button class="btn-checkout" id="checkoutBtn" type="button">Copy combined setup</button>
          <button class="btn-ghost" id="clearBtn" type="button">Clear stack</button>
          <a class="browse-link" href="/catalog/">Keep browsing the catalog</a>
          <p class="fine">One prompt covers every API in your stack. Paste it into your agent and it walks through each setup in order.</p>
        </aside>
      </div>`;

    wrap.querySelectorAll(".stack-item").forEach(li => {
      const name = li.getAttribute("data-name");
      li.querySelector('[data-act="up"]').addEventListener("click", () => move(name, -1));
      li.querySelector('[data-act="down"]').addEventListener("click", () => move(name, 1));
      li.querySelector('[data-act="remove"]').addEventListener("click", () => removeItem(name));
    });
    document.getElementById("checkoutBtn").addEventListener("click", function(){
      copyText(stackPrompt(apis), this);
    });
    document.getElementById("clearBtn").addEventListener("click", clearStack);
    PMA.paintCart();
  }

  function renderEmpty(){
    pageSub.textContent = "Your hand-picked APIs, ready to plug into your agent.";
    wrap.innerHTML = `
      <div class="empty">
        ` + %%CART_SVG_JS%% + `
        <h2>Your stack is empty</h2>
        <p>Add APIs from the catalog and they will show up here. When the stack looks right, copy one combined setup and hand it to your agent.</p>
        <a class="btn-primary" href="/catalog/">Browse the catalog</a>
      </div>`;
  }

  document.getElementById("burger").addEventListener("click", function(){
    const mnav = document.getElementById("mnav");
    const open = mnav.classList.toggle("open");
    this.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("pma:stack", render);
  window.addEventListener("storage", function(e){ if (e.key === PMA.stackKey) render(); });
  render();
})();
</script>
</body>
</html>
"""

    cart_svg_js = json.dumps(CART_SVG)
    page = head.replace("%%APIS_JSON%%", apis_json).replace("%%CART_SVG_JS%%", cart_svg_js).replace("400+ free APIs", api_count_copy() + " free APIs")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)

    # sanity checks
    assert "\u2014" not in page, "em dash found"
    assert page.count("</script>") == 1, "unexpected script tag count"
    print(f"wrote {OUT} ({len(page)//1024} KB, {len(apis)} APIs)")


if __name__ == "__main__":
    main()
