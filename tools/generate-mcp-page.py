#!/usr/bin/env python3
"""Generate build/mcp/index.html, the MCP Server Directory page.

Reads build/mcp-servers.json (curated free MCP servers) and renders a
searchable directory: server cards with install command, copyable client
config JSON, key badges, and source links. Same dark asphalt + safety
orange theme as the rest of the site.

Usage: python3 build/tools/generate-mcp-page.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
DATA = os.path.join(BUILD, "mcp-servers.json")
OUT_DIR = os.path.join(BUILD, "mcp")
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
"""

CART_JS = """
(function(){
  var KEY = "plugmyagent_stack_v1";
  function read(){ try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v : []; } catch (_) { return []; } }
  function paint(){ var n = read().length;
    document.querySelectorAll("[data-cart-count]").forEach(function(b){ b.textContent = n; b.style.display = n > 0 ? "" : "none"; }); }
  document.addEventListener("pma:stack", paint);
  window.addEventListener("storage", function(e){ if (e.key === KEY) paint(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", paint); else paint();
})();
"""


def api_count_copy():
    """Public count copy per the standing threshold rule: floor(n/50)*50 with '+'.
    485 -> '450+', 500 -> '500+', 550 -> '550+'. Never an exact number."""
    with open(os.path.join(BUILD, "api-catalog.json"), encoding="utf-8") as f:
        n = len(json.load(f))
    return f"{(n // 50) * 50}+"


def main():
    with open(DATA, encoding="utf-8") as f:
        servers = json.load(f)
    servers_json = json.dumps(servers, ensure_ascii=False).replace("</script", "<\\/script")

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
  <title>MCP Server Directory | PlugMyAgent</title>
  <meta name="description" content="A curated directory of free MCP servers for AI agents. One standard plug for files, apps, and services, with install commands and copy-paste client configs." />
  <link rel="canonical" href="https://www.plugmyagent.com/mcp/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="PlugMyAgent" />
  <meta property="og:title" content="MCP Server Directory | PlugMyAgent" />
  <meta property="og:description" content="Free MCP servers for your AI agent, with install commands and copy-paste configs." />
  <meta property="og:url" content="https://www.plugmyagent.com/mcp/" />
  <meta property="og:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="PlugMyAgent: 400+ free APIs to supercharge your AI agent" />
  <meta name="twitter:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="MCP Server Directory | PlugMyAgent" />
  <meta name="twitter:description" content="Free MCP servers for your AI agent, with install commands and copy-paste configs." />
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
      --green: #4ade80;
      --blue: #7fb5ec;
      --shadow: 0 22px 60px rgba(0,0,0,.55);
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
    h1, h2, h3 { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }

    .site-header { position: sticky; top: 0; z-index: 40; background: rgba(11,13,13,.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
    .site-header-inner { width: min(1120px, 100%); margin: 0 auto; padding: 11px clamp(16px, 4vw, 32px); display: flex; align-items: center; justify-content: space-between; min-height: 56px; position: relative; }
    .brandmark { display: inline-flex; align-items: center; }
    .brandmark img { display: block; height: 26px; width: auto; }
    .header-right { display: flex; align-items: center; }
    .cnav { display: flex; gap: 26px; align-items: center; }
    .cnav a { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color .18s; }
    .cnav a:hover { color: var(--yellow); }
    .cnav a[aria-current="page"] { color: var(--ink); }
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
      .mnav a[aria-current="page"] { color: var(--ink); }
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
    .page-head p { color: var(--muted); margin: 0; max-width: 620px; font-size: 16px; }

    .how { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; padding: 28px 0 8px; }
    @media (max-width: 760px) { .how { grid-template-columns: 1fr; }
      .cfg-body pre { white-space: pre-wrap; word-break: break-all; overflow-x: visible; } }
    .how-step { background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 18px; }
    .how-step .n { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .16em; color: var(--yellow); text-transform: uppercase; }
    .how-step h3 { margin: 8px 0 6px; font-size: 16px; letter-spacing: -.01em; }
    .how-step p { margin: 0; color: var(--muted); font-size: 14px; }

    .tools { display: flex; flex-wrap: wrap; gap: 10px; padding: 22px 0 6px; align-items: center; }
    .search { flex: 1 1 240px; display: flex; }
    .search input { width: 100%; background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-sm);
      padding: 12px 16px; color: var(--ink); font-size: 15px; outline: none; }
    .search input:focus { border-color: var(--yellow); }
    .search input::placeholder { color: var(--muted); }
    .chips { display: flex; flex-wrap: wrap; gap: 8px; padding: 12px 0 4px; }
    .fchip { background: transparent; border: 1px solid var(--line); border-radius: 999px; padding: 8px 16px;
      color: var(--muted); font-size: 13.5px; cursor: pointer; }
    .fchip:hover { color: var(--ink); border-color: rgba(255,255,255,.25); }
    .fchip.on { background: var(--yellow-soft); border-color: var(--yellow); color: var(--yellow); }
    .count { color: var(--muted); font-size: 13.5px; padding: 10px 0 0; }

    .servers { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; padding: 18px 0 80px; margin: 0; list-style: none; }
    @media (max-width: 860px) { .servers { grid-template-columns: minmax(0, 1fr); } }
    .server { background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 20px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
    .server-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
    .server h3 { margin: 0; font-size: 18px; letter-spacing: -.01em; }
    .server .desc { margin: 0; color: var(--muted); font-size: 14.5px; }
    .tags { display: flex; flex-wrap: wrap; gap: 6px; }
    .tag { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
      border: 1px solid var(--line); border-radius: 999px; padding: 3px 10px; color: var(--muted); }
    .tag.key { color: var(--green); border-color: rgba(74,222,128,.35); }
    .tag.nokey { color: var(--blue); border-color: rgba(127,181,236,.35); }
    .cmd { display: flex; align-items: center; gap: 10px; background: #0b0d0d; border: 1px solid var(--line); border-radius: var(--radius-sm);
      padding: 10px 10px 10px 14px; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12.5px; color: var(--ink); }
    .cmd code { flex: 1 1 auto; min-width: 0; overflow-x: auto; white-space: nowrap; padding: 2px 0; scrollbar-width: thin; }
    .copy-btn { flex: none; background: rgba(255,255,255,.06); border: 1px solid var(--line);
      border-radius: 8px; color: var(--muted); font-size: 12px; padding: 4px 10px; cursor: pointer; }
    .copy-btn:hover { color: var(--ink); border-color: rgba(255,255,255,.25); }
    details.cfg { border: 1px solid var(--line); border-radius: var(--radius-sm); background: #0b0d0d; }
    details.cfg summary { cursor: pointer; padding: 10px 14px; font-size: 13.5px; color: var(--muted); list-style: none; }
    details.cfg summary::-webkit-details-marker { display: none; }
    details.cfg summary:hover { color: var(--ink); }
    details.cfg summary::before { content: "+ "; color: var(--yellow); }
    details.cfg[open] summary::before { content: "- "; }
    .cfg-body { position: relative; border-top: 1px solid var(--line); }
    .cfg-body pre { margin: 0; padding: 14px 78px 14px 14px; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px;
      line-height: 1.6; overflow-x: auto; color: var(--ink); }
    .server-foot { display: flex; gap: 12px; margin-top: auto; padding-top: 4px; }
    .mini-link { font-size: 13px; color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--line); padding-bottom: 1px; }
    .mini-link:hover { color: var(--yellow); border-color: var(--yellow); }
    .noresult { text-align: center; color: var(--muted); padding: 50px 20px; grid-column: 1 / -1; }

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
        <a href="/catalog/">Catalog</a><a href="/mcp/" aria-current="page">MCP</a><a href="/components/">Components</a><a href="/guides/">Guides</a><a href="/#pillars">Tools</a>
      </nav>
      <a class="cart-link" href="/stack/" aria-label="My stack">""" + CART_SVG + """<span class="cart-count" data-cart-count style="display:none">0</span></a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
      <nav class="mnav" id="mnav" aria-label="Mobile">
        <a href="/catalog/">API Catalog</a><a href="/mcp/" aria-current="page">MCP</a><a href="/components/">Components</a><a href="/guides/">Guides</a><a href="/#pillars">Tools</a><a href="/stack/">My Stack</a>
      </nav>
    </div>
  </div></div>

  <main class="wrap">
    <div class="page-head">
      <p class="kicker">Pillar 02 // One standard plug</p>
      <h1>MCP Server Directory</h1>
      <p id="pageSub">MCP is one standard way for your agent to reach files, apps, and services. Pick a server below, run its install command, paste the config into your agent client, and it can use that tool right away.</p>
    </div>

    <div class="how">
      <div class="how-step"><div class="n">Step 01</div><h3>Run the install command</h3><p>Most servers install with one command. No accounts, no dashboards, no waiting.</p></div>
      <div class="how-step"><div class="n">Step 02</div><h3>Paste the config</h3><p>Copy the config block into your MCP client (Claude Desktop, Cursor, or your agent setup). Swap in your own paths or keys where marked.</p></div>
      <div class="how-step"><div class="n">Step 03</div><h3>Restart and ask</h3><p>Restart the client and ask your agent to use the new tool. If it can see it, it is working.</p></div>
    </div>

    <div class="tools">
      <div class="search"><input id="q" type="search" placeholder="Search servers, e.g. sqlite, github, web search" aria-label="Search MCP servers" autocomplete="off"></div>
    </div>
    <div class="chips" id="chips" role="group" aria-label="Filter by category"></div>
    <p class="count" id="count"></p>
    <ul class="servers" id="servers"></ul>
  </main>

  <footer>
    <div class="footer-inner"><strong>%%N%% servers, verified against official repos on September 19, 2026.</strong> Install commands and configs come from the official documentation. If a command fails, check the source link for the latest version.
      <p class="footer-trust">Every server here is free to run. Anything that needs a key only needs a free one.</p>
      <div class="footer-credit"><span>&copy; 2026 hiddeninwest</span><span class="footer-sep" aria-hidden="true">&middot;</span><a href="mailto:contact@plugmyagent.com">contact@plugmyagent.com</a><span class="footer-sep" aria-hidden="true">&middot;</span><a href="https://x.com/hiddeninwest" target="_blank" rel="noopener" aria-label="hiddeninwest on X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.451-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg></a></div>
    </div>
  </footer>
</div>

<script>
""" + CART_JS + """
(function(){
  const SERVERS = %%SERVERS_JSON%%;

  function esc(s){ return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

  const cats = ["All"].concat(Array.from(new Set(SERVERS.map(s => s.category))).sort());
  let activeCat = "All";
  let query = "";

  const chipsEl = document.getElementById("chips");
  const listEl = document.getElementById("servers");
  const countEl = document.getElementById("count");
  const qEl = document.getElementById("q");

  function keyBadge(s){
    if (!s.key_required) return '<span class="tag nokey">No key</span>';
    if (s.key_free) return '<span class="tag key">Free key</span>';
    return '<span class="tag">Key needed</span>';
  }

  function cardHtml(s){
    const cfg = JSON.stringify({ mcpServers: s.config_json }, null, 2);
    return `<li class="server">
      <div class="server-top"><h3>${esc(s.name)}</h3></div>
      <p class="desc">${esc(s.description)}</p>
      <div class="tags"><span class="tag">${esc(s.category)}</span>${keyBadge(s)}<span class="tag">${esc(s.license)}</span></div>
      <div class="cmd"><code>${esc(s.install_command)}</code><button class="copy-btn" data-copy="${esc(s.install_command)}" type="button">Copy</button></div>
      <details class="cfg">
        <summary>Client config</summary>
        <div class="cfg-body"><pre>${esc(cfg)}</pre><button class="copy-btn" data-copy-raw type="button">Copy</button></div>
      </details>
      <div class="server-foot">
        <a class="mini-link" href="${esc(s.source_url)}" target="_blank" rel="noopener">Source</a>
      </div>
    </li>`;
  }

  async function copyText(text, btn){
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

  function render(){
    chipsEl.innerHTML = cats.map(c =>
      `<button class="fchip${c === activeCat ? " on" : ""}" data-cat="${esc(c)}" type="button">${esc(c)}</button>`
    ).join("");
    const q = query.trim().toLowerCase();
    const shown = SERVERS.filter(s => {
      if (activeCat !== "All" && s.category !== activeCat) return false;
      if (!q) return true;
      return (s.name + " " + s.description + " " + s.install_command).toLowerCase().includes(q);
    });
    countEl.textContent = shown.length === SERVERS.length
      ? `${SERVERS.length} free MCP servers`
      : `${shown.length} of ${SERVERS.length} servers`;
    listEl.innerHTML = shown.length
      ? shown.map(cardHtml).join("")
      : `<li class="noresult"><h3>Nothing matches</h3><p>Try a different search or category.</p></li>`;
  }

  chipsEl.addEventListener("click", function(e){
    const b = e.target.closest("[data-cat]");
    if (!b) return;
    activeCat = b.getAttribute("data-cat");
    render();
  });
  qEl.addEventListener("input", function(){ query = qEl.value; render(); });

  listEl.addEventListener("click", function(e){
    const b = e.target.closest(".copy-btn");
    if (!b) return;
    if (b.hasAttribute("data-copy-raw")) {
      const pre = b.parentElement.querySelector("pre");
      copyText(pre.textContent, b);
    } else {
      copyText(b.getAttribute("data-copy"), b);
    }
  });

  document.getElementById("burger").addEventListener("click", function(){
    const mnav = document.getElementById("mnav");
    const open = mnav.classList.toggle("open");
    this.setAttribute("aria-expanded", String(open));
  });

  render();
})();
</script>
</body>
</html>
"""

    page = head.replace("%%SERVERS_JSON%%", servers_json).replace("%%N%%", str(len(servers))).replace("400+ free APIs", api_count_copy() + " free APIs")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)

    # sanity checks
    assert "\u2014" not in page, "em dash found"
    print(f"wrote {OUT} ({len(page)//1024} KB, {len(servers)} servers)")


if __name__ == "__main__":
    main()
