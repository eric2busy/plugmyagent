#!/usr/bin/env python3
"""Generate the plugmyagent Guides section (Pillar 04).

Outputs (under the repo root passed as argv[1], defaults to this script's build dir):
  guides/index.html
  guides/beginners-guide-to-ai-agents/index.html

Run from the repo root: python3 build/tools/generate-guides.py
"""
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")

HEAD_TMPL = """<!doctype html>
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
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="PlugMyAgent" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{ogalt}" />
  <meta name="twitter:image" content="https://www.plugmyagent.com/og-card.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #f5f7f5;
      --muted: #9aa39e;
      --paper: #0b0d0d;
      --white: #101314;
      --line: rgba(255,255,255,.09);
      --yellow: #ff6b1a;
      --yellow-soft: rgba(255,107,26,.14);
      --green: #4ade80;
      --shadow: 0 22px 60px rgba(0,0,0,.55);
      --radius-md: 18px;
      --radius-sm: 12px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; background: #0b0d0d; color-scheme: dark; overflow-x: clip; }}
    body {{
      margin: 0; overflow-x: clip; background: #0b0d0d; color: var(--ink);
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 16px; line-height: 1.65; -webkit-font-smoothing: antialiased;
    }}
    a {{ color: inherit; }}
    h1, h2, h3 {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.2; }}
    .site-header {{ position: sticky; top: 0; z-index: 40; background: rgba(11,13,13,.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }}
    .site-header-inner {{ width: min(1120px, 100%); margin: 0 auto; padding: 11px clamp(16px, 4vw, 32px); display: flex; align-items: center; justify-content: space-between; min-height: 56px; position: relative; }}
    .brandmark {{ display: inline-flex; align-items: center; }}
    .brandmark img {{ display: block; height: 26px; width: auto; }}
    .header-right {{ display: flex; align-items: center; }}
    .cnav {{ display: flex; gap: 26px; align-items: center; }}
    .cnav a {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color .18s; }}
    .cnav a:hover {{ color: var(--yellow); }}
    .cnav a[aria-current="page"] {{ color: var(--ink); }}
    .cart-link {{ display: inline-flex; align-items: center; padding: 8px; margin-left: 14px; color: var(--muted); }}
    .cart-link:hover {{ color: var(--yellow); }}
    .cart-link svg {{ width: 22px; height: 22px; }}
    .cart-count {{ font-size: 11px; background: var(--yellow); color: #0b0d0d; border-radius: 999px; padding: 1px 7px; margin-left: 6px; font-weight: 700; }}
    .burger {{ display: none; background: none; border: 0; cursor: pointer; padding: 12px 2px 12px 14px; }}
    .burger span {{ display: block; width: 22px; height: 2px; border-radius: 2px; background: var(--ink); margin: 5px 0; transition: transform .2s, opacity .2s, background .2s; }}
    .burger:hover span {{ background: var(--yellow); }}
    .burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); background: var(--yellow); }}
    .burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
    .burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); background: var(--yellow); }}
    .mnav {{ display: none; }}
    @media (max-width: 760px) {{
      .cnav {{ display: none; }}
      .burger {{ display: block; }}
      .mnav {{ display: block; position: absolute; top: calc(100% + 8px); right: 16px; min-width: 230px; z-index: 60;
        background: var(--white); border: 1px solid var(--line); border-radius: 12px; padding: 8px; box-shadow: var(--shadow);
        opacity: 0; transform: translateY(-6px); pointer-events: none; transition: opacity .18s, transform .18s; }}
      .mnav.open {{ opacity: 1; transform: none; pointer-events: auto; }}
      .mnav a {{ display: block; padding: 12px 14px; border-radius: 8px;
        font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
        color: var(--muted); text-decoration: none; }}
      .mnav a:hover {{ background: var(--yellow-soft); color: var(--yellow); }}
      .mnav a[aria-current="page"] {{ color: var(--ink); }}
    }}
    .wrap {{ width: min(1120px, 100%); margin: 0 auto; padding: 0 clamp(16px, 4vw, 32px); }}
    .hero {{ padding: clamp(40px, 6vw, 72px) 0 clamp(16px, 3vw, 28px); position: relative; }}
    .eyebrow {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px; letter-spacing: .18em; text-transform: uppercase; color: var(--yellow); margin-bottom: 18px; }}
    .hero h1 {{ font-size: clamp(30px, 4.6vw, 46px); margin: 0 0 14px; letter-spacing: -0.02em; }}
    .neon {{ color: var(--yellow); }}
    .lede {{ font-size: clamp(16px, 1.9vw, 18px); color: var(--muted); max-width: 660px; margin: 0 0 22px; }}
    .btn {{ display: inline-flex; align-items: center; gap: 8px; font-weight: 700; text-decoration: none; border-radius: 999px; transition: transform .15s, box-shadow .15s; }}
    .btn-neon {{ background: var(--yellow); color: #0b0d0d; padding: 14px 28px; box-shadow: 0 8px 30px rgba(255,107,26,.35); }}
    .btn-neon:hover {{ transform: translateY(-2px); box-shadow: 0 12px 36px rgba(255,107,26,.45); }}
    .btn-ghost {{ border: 1px solid var(--line); color: var(--ink); padding: 13px 26px; }}
    .btn-ghost:hover {{ border-color: var(--yellow); color: var(--yellow); }}
    .hero-cta {{ display: flex; gap: 14px; flex-wrap: wrap; }}
    .article {{ width: min(760px, 100%); margin: 0 auto; padding: 12px clamp(16px, 4vw, 32px) 64px; }}
    .article h2 {{ font-size: clamp(24px, 4vw, 32px); margin: 52px 0 16px; letter-spacing: -0.01em; }}
    .article h2 .secnum {{ color: var(--yellow); font-family: "Azeret Mono", ui-monospace, monospace; font-size: .6em; vertical-align: middle; margin-right: 12px; letter-spacing: .1em; }}
    .article h3 {{ font-size: 20px; margin: 32px 0 10px; }}
    .article p {{ color: #d7dcd8; margin: 0 0 18px; }}
    .article ul, .article ol {{ color: #d7dcd8; margin: 0 0 20px; padding-left: 22px; }}
    .article li {{ margin-bottom: 10px; }}
    .article strong {{ color: var(--ink); }}
    .big-idea {{ border: 1px solid var(--line); border-left: 4px solid var(--yellow); background: var(--white); border-radius: var(--radius-sm); padding: 22px 24px; margin: 28px 0; }}
    .big-idea.first {{ margin-top: 4px; }}
    .big-idea p {{ margin: 0; font-size: 18px; }}
    .big-idea .kicker {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--yellow); display: block; margin-bottom: 10px; }}
    table.compare {{ width: 100%; border-collapse: collapse; margin: 24px 0 30px; font-size: 15px; }}
    table.compare th, table.compare td {{ text-align: left; padding: 14px 16px; border: 1px solid var(--line); vertical-align: top; }}
    table.compare th {{ background: var(--white); font-family: "Azeret Mono", ui-monospace, monospace; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }}
    table.compare th:first-child {{ color: var(--muted); }}
    table.compare th:last-child {{ color: var(--yellow); }}
    table.compare td {{ color: #d7dcd8; }}
    @media (max-width: 640px) {{ table.compare, table.compare tbody {{ display: block; }} table.compare tr:first-child {{ display: none; }} table.compare tr {{ display: flex; flex-wrap: wrap; margin-bottom: 14px; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; background: var(--white); }} table.compare tr > th {{ flex: 1 1 100%; border: 0; border-bottom: 1px solid var(--line); text-transform: uppercase; letter-spacing: .14em; }} table.compare tr > td {{ flex: 1 1 0; min-width: 0; border: 0; padding: 12px 14px 16px; }} table.compare tr > td:first-of-type {{ border-right: 1px solid var(--line); }} table.compare tr > td::before {{ content: attr(data-label); display: block; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 10px; letter-spacing: .18em; text-transform: uppercase; margin-bottom: 8px; }} table.compare tr > td:first-of-type::before {{ color: var(--muted); }} table.compare tr > td:last-of-type::before {{ color: var(--yellow); }} }}
    .promptbox {{ background: #0e1111; border: 1px solid var(--line); border-left: 4px solid var(--yellow); border-radius: var(--radius-sm); padding: 18px 20px; margin: 18px 0 24px; position: relative; }}
    .promptbox .plabel {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); display: block; margin-bottom: 10px; }}
    .promptbox .plabel.bad {{ color: #ff8a70; }}
    .promptbox .plabel.good {{ color: var(--green); }}
    .promptbox p {{ margin: 0; font-size: 15.5px; color: var(--ink); }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 24px 0 30px; }}
    .gcard {{ background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 22px; }}
    .gcard h3 {{ margin: 0 0 10px; font-size: 18px; }}
    .gcard h3 .ico {{ color: var(--yellow); margin-right: 8px; }}
    .gcard p {{ margin: 0; font-size: 15px; color: var(--muted); }}
    .checklist {{ list-style: none; padding: 0; margin: 20px 0 28px; }}
    .checklist li {{ background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 16px 18px 16px 52px; position: relative; margin-bottom: 12px; }}
    .checklist li::before {{ content: attr(data-n); position: absolute; left: 16px; top: 14px; width: 24px; height: 24px; border-radius: 50%; background: var(--yellow-soft); color: var(--yellow); font-weight: 800; font-size: 13px; display: flex; align-items: center; justify-content: center; }}
    .dlbox {{ border: 1px solid var(--yellow); background: linear-gradient(180deg, rgba(255,107,26,.12), rgba(255,107,26,.03)); border-radius: var(--radius-md); padding: 30px; margin: 44px 0 20px; text-align: center; }}
    .dlbox h3 {{ margin: 0 0 10px; font-size: 22px; }}
    .dlbox p {{ color: var(--muted); margin: 0 0 20px; }}
    .guide-card {{ display: flex; gap: 22px; align-items: flex-start; background: var(--white); border: 1px solid var(--line); border-radius: var(--radius-md); padding: 26px; text-decoration: none; margin: 26px 0; transition: border-color .18s, transform .15s; }}
    .guide-card:hover {{ border-color: var(--yellow); transform: translateY(-2px); }}
    .guide-card .gnum {{ font-family: "Azeret Mono", ui-monospace, monospace; color: var(--yellow); font-size: 13px; letter-spacing: .14em; white-space: nowrap; padding-top: 4px; }}
    .guide-card h3 {{ margin: 0 0 8px; font-size: 21px; }}
    .guide-card p {{ margin: 0; color: var(--muted); font-size: 15px; }}
    .guide-card .gmeta {{ display: block; margin-top: 12px; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--yellow); }}
    .index-kicker {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--yellow); display: block; margin: 48px 0 0; }}
    h2.index-h {{ margin-top: 8px; }}
    .index-sub {{ color: var(--muted); font-size: 15px; margin: 0 0 6px; }}
    .crumbs {{ font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin-bottom: 26px; }}
    .crumbs a {{ color: var(--muted); text-decoration: none; }}
    .crumbs a:hover {{ color: var(--yellow); }}
    .crumbs .sep {{ margin: 0 8px; opacity: .5; }}
    .crumbs .cur {{ color: var(--yellow); }}
    footer {{ border-top: 1px solid var(--line); margin-top: 40px; }}
    .footer-inner {{ width: min(1120px, 100%); margin: 0 auto; padding: 34px clamp(16px, 4vw, 32px) 44px; color: var(--muted); font-size: 14px; }}
    .footer-inner strong {{ color: var(--ink); }}
    .footer-trust {{ margin: 12px 0 0; }}
    .footer-credit {{ display: flex; align-items: center; gap: 12px; margin-top: 18px; }}
    .footer-sep {{ opacity: .4; }}
    .footer-credit a {{ display: inline-flex; }}
    .footer-credit svg {{ width: 18px; height: 18px; fill: var(--muted); transition: fill .18s; }}
    .footer-credit a:hover svg {{ fill: var(--yellow); }}
  </style>
</head>
<body>
  <div class="site-header"><div class="site-header-inner">
    <a class="brandmark" href="/" aria-label="PlugMyAgent home"><img src="/plug-lockup-v2.png" alt="PlugMyAgent"></a>
    <div class="header-right">
      <nav class="cnav" aria-label="Primary">
        <a href="/catalog/">Catalog</a><a href="/mcp/">MCP</a><a href="/components/">Components</a><a href="/guides/" aria-current="page">Guides</a><a href="/#pillars">Tools</a>
      </nav>
      <a class="cart-link" href="/stack/" aria-label="My stack"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.6"/><circle cx="17" cy="20" r="1.6"/><path d="M2.5 3.5h2.6l2.5 12.2a1.5 1.5 0 0 0 1.5 1.2h7.9a1.5 1.5 0 0 0 1.5-1.2L20.5 7H6"/></svg><span class="cart-count" data-cart-count style="display:none">0</span></a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
      <nav class="mnav" id="mnav" aria-label="Mobile">
        <a href="/catalog/">API Catalog</a><a href="/mcp/">MCP</a><a href="/components/">Components</a><a href="/guides/" aria-current="page">Guides</a><a href="/stack/">My Stack</a>
      </nav>
    </div>
  </div></div>
"""

FOOT_TMPL = """  <footer>
    <div class="footer-inner"><strong>{footline}</strong>
      <p class="footer-trust">An independent, hand-maintained catalog of free APIs for AI agents. No ads, no sponsored placements, just tools worth your time.</p>
      <div class="footer-credit"><span>&copy; 2026 hiddeninwest</span><span class="footer-sep" aria-hidden="true">&middot;</span><a href="mailto:contact@plugmyagent.com">contact@plugmyagent.com</a><span class="footer-sep" aria-hidden="true">&middot;</span><a href="https://x.com/hiddeninwest" target="_blank" rel="noopener" aria-label="hiddeninwest on X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.451-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg></a></div>
    </div>
  </footer>

<script>
(function(){{
  var KEY = "plugmyagent_stack_v1";
  function read(){{ try {{ var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v : []; }} catch (_) {{ return []; }} }}
  function paint(){{ var n = read().length;
    document.querySelectorAll("[data-cart-count]").forEach(function(b){{ b.textContent = n; b.style.display = n > 0 ? "" : "none"; }}); }}
  document.addEventListener("pma:stack", paint);
  window.addEventListener("storage", function(e){{ if (e.key === KEY) paint(); }});
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", paint); else paint();
}})();
document.getElementById("burger").addEventListener("click", function(){{
  const mnav = document.getElementById("mnav");
  const open = mnav.classList.toggle("open");
  this.setAttribute("aria-expanded", open ? "true" : "false");
}});
</script>
</body>
</html>
"""

GUIDE_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Pillar 04 // Guide 001</div>
      <h1>From chatbot to coworker:<br><span class="neon">a beginner's guide to AI agents.</span></h1>
      <p class="lede">If you have only ever chatted with AI, you are using about ten percent of what it can do. This guide shows how a personal AI agent turns "ask me anything" into "consider it done." No jargon, no setup required to understand it.</p>
      <div class="hero-cta">
        <a class="btn btn-neon" href="#start">Read the guide</a>
        <a class="btn btn-ghost" href="./ai-agents-beginners-guide.pdf" download>Download the PDF</a>
      </div>
    </div>
  </section>

  <article class="article" id="start">
    <h2><span class="secnum">01</span>The one idea: a chatbot answers, an agent acts</h2>
    <p>You already know the chatbot move. You type a question, it types an answer, and the conversation ends. An AI agent works differently. You hand it an outcome, and it does the work to get there: it plans the steps, uses tools, checks sources, builds things, and reports back when it is done.</p>
    <div class="big-idea">
      <span class="kicker">The shift in one sentence</span>
      <p><strong>Stop asking for answers. Start handing over outcomes.</strong></p>
    </div>
    <table class="compare">
      <tr><th></th><th>Chatbot</th><th>AI agent</th></tr>
      <tr><th>You ask for</th><td data-label="Chatbot">An answer</td><td data-label="AI agent">An outcome</td></tr>
      <tr><th>It does</th><td data-label="Chatbot">Writes a reply</td><td data-label="AI agent">Runs the errands, checks the sources, builds the thing</td></tr>
      <tr><th>After you close the app</th><td data-label="Chatbot">Nothing</td><td data-label="AI agent">Keeps working and reports back</td></tr>
      <tr><th>Best for</th><td data-label="Chatbot">Quick questions</td><td data-label="AI agent">Real tasks with real deliverables</td></tr>
    </table>

    <h2><span class="secnum">02</span>Meet your AI agent</h2>
    <p>A personal AI agent is your own dedicated assistant with its own computer that keeps working between conversations. It remembers your context, keeps going in the background, and every conversation is one to one: just you and your agent. Examples include Muse (Meta's personal AI agent) and OpenClaw. This guide uses Muse as the running example, but the playbook works for any of them.</p>
    <p>You reach Muse on the web at <strong>muse.ai</strong>, in the <strong>iOS and Android apps</strong>, or over <strong>WhatsApp</strong>. It is available in the US and Canada.</p>
    <p>Think of it this way: a chatbot is a very smart stranger you meet fresh every time. An agent is a sharp assistant who already knows how you work.</p>

    <h2><span class="secnum">03</span>See the difference: four before-and-after swaps</h2>
    <p>The fastest way to feel the shift is to watch a chatbot request become an agent request.</p>

    <h3>1. The hotel hunt</h3>
    <div class="promptbox"><span class="plabel bad">Chatbot move</span><p>"What are some good hotels in Vegas?"</p></div>
    <div class="promptbox"><span class="plabel good">Agent move</span><p>"Find the best Sunday-night hotel deal near the Strip for September 27, under $120, with free parking. Keep watching prices and tell me if something better shows up before Friday."</p></div>

    <h3>2. The resume</h3>
    <div class="promptbox"><span class="plabel bad">Chatbot move</span><p>"Write me a resume summary."</p></div>
    <div class="promptbox"><span class="plabel good">Agent move</span><p>"Here is my work history. Build me a one-page resume tailored for office manager roles, and save it as both a PDF and a Word file."</p></div>

    <h3>3. The side hustle</h3>
    <div class="promptbox"><span class="plabel bad">Chatbot move</span><p>"How do I start a side business?"</p></div>
    <div class="promptbox"><span class="plabel good">Agent move</span><p>"Research three side business ideas I can start with zero dollars and my background in customer service and design. Rank them by realistic first-month income and turn the winner into a one-page plan."</p></div>

    <h3>4. The reminder that actually works</h3>
    <div class="promptbox"><span class="plabel bad">Chatbot move</span><p>"Remind me to call the dentist."</p></div>
    <div class="promptbox"><span class="plabel good">Agent move</span><p>"Remind me to call the dentist Tuesday at 9am. If I have not confirmed by 10, nudge me again."</p></div>

    <h2><span class="secnum">04</span>What you can hand it today</h2>
    <p>Six kinds of work where the agent version beats the chatbot version every time.</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>Research and comparisons</h3><p>Deep dives with sources, price comparisons, best-of lists ranked by what actually matters to you.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Documents and decks</h3><p>Reports, spreadsheets, presentations, resumes, one-pagers. It writes them and hands you the file.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Build simple things</h3><p>Web pages, landing pages, small tools and prototypes you can open and use, not just read about.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Watch things for you</h3><p>Prices, inboxes, listings, schedules. It checks on a schedule and only pings you when something real happens.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Keep you on track</h3><p>Goals, trips, projects, reminders, morning briefings. It carries the plan so you do not have to.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Draft your words</h3><p>Emails, messages, posts, replies. It drafts everything and nothing goes out without your say-so.</p></div>
    </div>

    <h2><span class="secnum">05</span>How to prompt it well: the delegation recipe</h2>
    <p>Good agent prompts read like a good work assignment. Four ingredients:</p>
    <ol>
      <li><strong>The outcome.</strong> What does "done" look like? Name the deliverable.</li>
      <li><strong>The context.</strong> Dates, budget, links, background. The stuff it cannot guess.</li>
      <li><strong>The constraints.</strong> Budget, tone, length, what to avoid.</li>
      <li><strong>The check.</strong> For anything outward-facing, say "show me before you send anything."</li>
    </ol>
    <div class="promptbox"><span class="plabel bad">Vague</span><p>"Plan my trip."</p></div>
    <div class="promptbox"><span class="plabel good">Delegated</span><p>"Plan a 3-day weekend trip to San Diego, October 16 to 18, $600 total budget for two people. We like food and beaches and hate crowds. Give me a day-by-day plan with prices and links, and flag anything that needs booking ahead."</p></div>
    <p>Notice the second one does not just ask a question. It hands over a job with a finish line.</p>

    <h2><span class="secnum">06</span>Staying in control: the approval card</h2>
    <p>Handing work to an agent does not mean handing over your judgment. When something needs your decision, you get an approval card that says exactly what it wants to do. Nothing moves until you say yes.</p>
    <p>It will check with you before it spends money, sends a message, posts anything publicly, touches your accounts, or does anything hard to undo. Logins and keys go into a secure vault, never into the chat. You stay the decider. It stays the doer.</p>

    <h2><span class="secnum">07</span>Your first week: five copy-paste starters</h2>
    <p>Do not start with "what can you do." Start with one of these.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Research something you are actually buying.</strong> "Research the 5 best noise-canceling headphones under $200 and rank them by comfort for long calls. Include prices and links."</li>
      <li data-n="2"><strong>Turn messy notes into a clean doc.</strong> "Turn these notes into a clean one-page summary: [paste your notes]."</li>
      <li data-n="3"><strong>Set a daily briefing.</strong> "Every morning, check the news on [your topic] and send me a 3-bullet briefing."</li>
      <li data-n="4"><strong>Draft, do not send.</strong> "Draft an email to my landlord about the leaky faucet. Keep it short and polite. Do not send it."</li>
      <li data-n="5"><strong>Build something small.</strong> "Build me a simple one-page site for my side project. Keep it clean and mobile-friendly."</li>
    </ol>

    <h2><span class="secnum">08</span>Getting started in three steps</h2>
    <ol class="checklist">
      <li data-n="1"><strong>Pick an agent and get the app.</strong> Start with Muse: open <strong>muse.ai</strong> on the web, or grab the iOS or Android app. If you live in the US or Canada, you are in. Other agents work the same way from here.</li>
      <li data-n="2"><strong>Start with one real task</strong> from the list above, not a test question. Real stakes teach you the workflow faster.</li>
      <li data-n="3"><strong>Manage it like a person.</strong> Give feedback the way you would to an assistant: "good, but shorter" or "redo this with the new dates." It learns how you like things.</li>
    </ol>
    <div class="promptbox"><span class="plabel good">Do it hands-on</span><p>Walkthrough W01 sets up your first AI agent in 10 minutes: account, app, and your first real task, step by step. <a href="/guides/walkthroughs/your-first-ai-agent/" style="color: var(--yellow);">Start W01 &rarr;</a></p></div>

    <div class="dlbox">
      <h3>Take this guide with you</h3>
      <p>The full guide as a clean, shareable PDF. Send it to the friend who still thinks AI is just a chatbot.</p>
      <a class="btn btn-neon" href="./ai-agents-beginners-guide.pdf" download>Download the PDF</a>
    </div>
    <a class="guide-card" href="/guides/intermediate-guide-to-ai-agents/">
      <span class="gnum">002</span>
      <span>
        <h3>Next: the intermediate guide</h3>
        <p>From Tasks to Systems: stop assigning tasks and start building systems. Memory that matters, connected tools, schedules that stick, and five copy-paste plays.</p>
        <span class="gmeta">Intermediate &middot; 10 min read &middot; PDF included</span>
      </span>
    </a>
  </article>
</main>
"""

GUIDE2_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Pillar 04 // Guide 002</div>
      <h1>From tasks to systems:<br><span class="neon">an intermediate guide to AI agents.</span></h1>
      <p class="lede">You finished the beginner's guide: you can hand your agent a task. This is the sequel. Memory that matters, connected tools, schedules that stick, long projects, and five copy-paste systems that run without you.</p>
      <div class="hero-cta">
        <a class="btn btn-neon" href="#start">Read the guide</a>
        <a class="btn btn-ghost" href="./ai-agents-intermediate-guide.pdf" download>Download the PDF</a>
      </div>
    </div>
  </section>

  <article class="article" id="start">
    <p><a href="/guides/beginners-guide-to-ai-agents/" style="color: var(--yellow);">New here? Start with guide 001, the beginner's guide, first.</a></p>

    <h2><span class="secnum">01</span>The level-up: stop assigning tasks, start building systems</h2>
    <p>The beginner move is handing over one task with a finish line. The intermediate move is setting up a workflow that runs without you asking each time.</p>
    <p>The shift is small, but everything changes with it: from "do this" to "handle this, ongoing." A task ends. A system keeps working. Your agent can do both, but systems are where the real leverage lives.</p>
    <div class="promptbox"><span class="plabel bad">The beginner version</span><p>"Check this price now."</p></div>
    <div class="promptbox"><span class="plabel good">The intermediate version</span><p>"Watch this price every day and tell me the moment it drops below $400." You asked once. It works forever.</p></div>
    <div class="big-idea">
      <span class="kicker">The big idea</span>
      <p><strong>Tasks save you minutes. Systems save you hours. This guide is about systems.</strong></p>
    </div>

    <h2><span class="secnum">02</span>Teach it how you work: memory that matters</h2>
    <p>Your agent remembers context across conversations. The intermediate skill is feeding it the things that do not change: how you like your emails (short, no fluff), your budget rules, your projects, the names and details it keeps needing.</p>
    <p>When it gets something wrong about you, correct it the way you would a person: "from now on, always use my work email for drafts." Say it once. It sticks.</p>
    <div class="big-idea">
      <span class="kicker">Two rules for memory</span>
      <p><strong>One:</strong> preferences and context go in memory.<br><strong>Two:</strong> secrets never do. Passwords and keys go in the secure vault, never in the chat.</p>
    </div>
    <div class="big-idea">
      <span class="kicker">Memory tip</span>
      <p>Every few weeks, ask it "what do you remember about me and how I like to work?" Delete what is stale. <strong>Memory is a garden, not a hard drive.</strong></p>
    </div>

    <h2><span class="secnum">03</span>Connect your world: inbox, calendar, files</h2>
    <p>An agent with no connections is a brilliant assistant locked out of your office. Connections change that.</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>Calendar</h3><p>It can schedule, reschedule, and warn you about conflicts before you walk into them.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Inbox</h3><p>It can triage, draft replies, and surface only the messages that need your decision.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Files</h3><p>It can organize, summarize, and pull the right document the moment you need it.</p></div>
    </div>
    <p>You grant access once. After that, the approval habit in section 06 decides what it does on its own and what it brings to you first.</p>
    <div class="big-idea">
      <span class="kicker">The trust ladder</span>
      <p><strong>Start with read access everywhere. Let it look before it touches.</strong> Expand to write access once it proves it handles the small stuff. Read is cheap. Write is earned.</p>
    </div>
    <div class="promptbox"><span class="plabel good">Do it hands-on</span><p>Walkthrough W03 connects your first MCP server in five minutes: the fastest way to feel what "connected tools" actually means. <a href="/guides/walkthroughs/first-mcp-server/" style="color: var(--yellow);">Start W03 &rarr;</a></p></div>

    <h2><span class="secnum">04</span>Put it on a schedule: briefings, checks, watches</h2>
    <p>Three patterns cover almost every recurring need.</p>
    <div class="promptbox"><span class="plabel">The briefing</span><p>"Every weekday at 7:30am, send me a 5-bullet briefing: the top news in my industry, my calendar for the day, and anything on my watch list that moved."</p></div>
    <div class="promptbox"><span class="plabel">The check</span><p>"Every morning, check my inbox. Draft replies to anything routine. Only ping me about the ones that need my decision."</p></div>
    <div class="promptbox"><span class="plabel">The watch</span><p>"Watch flights to Denver for October. Tell me the moment a round trip drops under $250."</p></div>
    <div class="big-idea">
      <span class="kicker">The rule for all three</span>
      <p>Define the trigger, the quiet hours, and what "tell me" means. <strong>Vague schedules create noise. Precise schedules create leverage.</strong></p>
    </div>

    <h2><span class="secnum">05</span>Run long projects without losing the plot</h2>
    <p>Big work dies in long, shapeless conversations. The intermediate move is milestones plus checkpoints.</p>
    <p>Before it starts, ask for the plan: "Break this into milestones and show me the plan before you do anything." Approve the plan, then let it run. Then add one rule: "Report back after each milestone with what is done and what is next. Do not wait until the end."</p>
    <p>Keep one conversation per project. Everything it learns stays in one place, and you can scroll up any time to see how a decision was made.</p>
    <div class="promptbox"><span class="plabel">When a project stalls</span><p>"Pick up where we left off: the last finished milestone was X, continue from Y." Do not restart from zero. Context is the asset. Protect it.</p></div>

    <h2><span class="secnum">06</span>The approval habit: what to auto-allow vs always check</h2>
    <p>You do not want to approve everything. You also do not want to approve nothing. Set the line once, in plain words.</p>
    <div class="promptbox"><span class="plabel good">Green list: auto-allow</span><p>Research, drafts, organizing files, summaries, reminders, price checks. Anything reversible and private.</p></div>
    <div class="promptbox"><span class="plabel bad">Red list: always check</span><p>Spending money, sending or posting anything, touching accounts, changing settings, deleting anything. Anything hard to undo.</p></div>
    <div class="promptbox"><span class="plabel">The script</span><p>"Draft anything, send nothing. Research anything, buy nothing. If it is hard to undo, ask me first."</p></div>
    <div class="big-idea">
      <span class="kicker">The principle</span>
      <p><strong>When in doubt, it asks. That is the deal that makes everything else safe.</strong></p>
    </div>

    <h2><span class="secnum">07</span>When it goes wrong: the 3-minute fix</h2>
    <p>It will misunderstand you sometimes. The fix is almost always fast.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Point at the exact problem.</strong> Not "this is wrong" but "the dates are wrong, use October 16 to 18, not September." Specific corrections teach. Vague ones do not.</li>
      <li data-n="2"><strong>Give the correction once, then move on.</strong> "From now on, prices in USD." Done. Do not re-explain every time.</li>
      <li data-n="3"><strong>If the output is vague, ask for shape.</strong> "Give me the top 3 with prices and links, not a paragraph." Agents default to prose. Tell it the format you want.</li>
      <li data-n="4"><strong>If it assumed wrong, add the constraint it missed.</strong> Most bad output is a missing constraint, not a bad agent. "You assumed business travel. This is a family trip with two kids." Then let it redo.</li>
    </ol>
    <div class="big-idea">
      <span class="kicker">Do not restart from zero</span>
      <p><strong>A correction inside the same conversation keeps everything it already got right.</strong></p>
    </div>

    <h2><span class="secnum">08</span>Five intermediate plays</h2>
    <p>Copy, paste, customize. Each one is a system, not a task.</p>
    <div class="promptbox"><span class="plabel">Play 1: the Monday briefing</span><p>"Every Monday at 8am, send me: the 3 biggest stories in [my field], any price drops on my watch list, and conflicts in my calendar this week."</p></div>
    <div class="promptbox"><span class="plabel">Play 2: the inbox triage</span><p>"Every weekday at 9am, scan my inbox. Draft replies to anything routine. Flag the 3 messages that need my decision, with a one-line summary of each. Send nothing."</p></div>
    <div class="promptbox"><span class="plabel">Play 3: the project tracker</span><p>"Track my [project name] project. Every Friday, ask me for a status update, then reply with: what is done, what is stuck, and what is next."</p></div>
    <div class="promptbox"><span class="plabel">Play 4: the deal watch</span><p>"Watch [product, flight, hotel]. Alert me the moment the price drops below [number] or a clearly better option appears. Include the link."</p></div>
    <div class="promptbox"><span class="plabel">Play 5: the content multiplier</span><p>"Take my [notes / voice memo / rough draft] and turn it into three things: a social post, a short email, and a one-pager. Keep my voice, cut the fluff."</p></div>

    <h2><span class="secnum">09</span>What&apos;s next</h2>
    <p>You have gone from chatbot to coworker to systems builder. The advanced guide is next: chaining agents together, building custom workflows, connecting your own tools and data, and running your agent like a small ops team.</p>

    <div class="dlbox">
      <h3>Take this guide with you</h3>
      <p>The full intermediate guide as a clean, shareable PDF. Same series, same format.</p>
      <a class="btn btn-neon" href="./ai-agents-intermediate-guide.pdf" download>Download the PDF</a>
    </div>
    <a class="guide-card" href="/guides/beginners-guide-to-ai-agents/">
      <span class="gnum">001</span>
      <span>
        <h3>Missed the first one?</h3>
        <p>From Chatbot to Coworker: the beginner's guide that starts the series. The chatbot-to-agent shift, the delegation recipe, and five starter tasks.</p>
        <span class="gmeta">Beginner &middot; 8 min read &middot; PDF included</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/advanced-guide-to-ai-agents/">
      <span class="gnum">003</span>
      <span>
        <h3>Next: the advanced guide</h3>
        <p>From Systems to Leverage: compose teams of specialist agents, build your own workflows, feed them your data, and run the whole thing like a small ops team.</p>
        <span class="gmeta">Advanced &middot; 12 min read &middot; PDF included</span>
      </span>
    </a>
  </article>
</main>
"""


GUIDE3_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Pillar 04 // Guide 003</div>
      <h1>From systems to leverage:<br><span class="neon">an advanced guide to AI agents.</span></h1>
      <p class="lede">You run systems that work without you. Now compose them: chain specialist agents, build your own workflows, feed them your data, and run the whole thing like a small ops team.</p>
      <div class="hero-cta">
        <a class="btn btn-neon" href="#start">Read the guide</a>
        <a class="btn btn-ghost" href="./ai-agents-advanced-guide.pdf" download>Download the PDF</a>
      </div>
    </div>
  </section>

  <article class="article" id="start">
    <p><a href="/guides/intermediate-guide-to-ai-agents/" style="color: var(--yellow);">Coming from guide 002? Good. This is where composition starts.</a></p>

    <h2><span class="secnum">01</span>The advanced leap: from using agents to composing them</h2>
    <p>The beginner move was handing over one task with a finish line. The intermediate move was building systems that run without you asking each time. The advanced move is composing: chaining specialist agents together, feeding them your own data, and building workflows bigger than any single prompt.</p>
    <p>Think of it as going from playing an instrument to conducting. One agent is a talented employee. A composed team of agents, wired to your data and your tools, is a department.</p>
    <div class="promptbox"><span class="plabel bad">One giant prompt</span><p>"Do my market research, write the report, make the slides, and email it." One agent, one breath, fingers crossed.</p></div>
    <div class="promptbox"><span class="plabel good">A composed workflow</span><p>A researcher gathers. A planner organizes. A maker drafts. A checker reviews. Each one has a tight brief and hands off a finished artifact.</p></div>
    <div class="big-idea">
      <span class="kicker">The big idea</span>
      <p><strong>Beginners delegate tasks. Intermediates build systems. Advanced users compose teams.</strong> The leverage compounds at every level.</p>
    </div>

    <h2><span class="secnum">02</span>Chain agents together: specialists beat generalists</h2>
    <p>A single agent juggling research, analysis, writing, and review does each one worse than a specialist would. The advanced pattern is the assembly line: small agents, each with one job and a tight brief.</p>
    <p>The handoff rule makes it work: each agent passes the next one a finished artifact, not a chat log. "Here are the 10 sources, ranked" beats "here is our whole conversation, good luck."</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>The Researcher</h3><p>Gathers raw material: sources, prices, options, facts. Never judges, just collects.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>The Planner</h3><p>Turns raw material into structure: outlines, comparisons, shortlists. Never writes the final draft.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>The Maker</h3><p>Produces the artifact: the draft, the sheet, the summary. Works only from the plan, never from raw chaos.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>The Checker</h3><p>Reviews the maker's output against your rules before anything ships. Cheap insurance. Expensive to skip.</p></div>
    </div>
    <div class="big-idea">
      <span class="kicker">Start with two</span>
      <p>You do not need four agents on day one. <strong>Split your hardest workflow into researcher and maker first.</strong> Add the planner and checker once the handoffs feel natural.</p>
    </div>

    <h2><span class="secnum">03</span>Build your own workflows: the recipe pattern</h2>
    <p>A workflow is a recipe your agents follow every time. Write it once, run it forever. Every good recipe has four parts.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Name it.</strong> "The Friday client report." A name turns a prompt into a thing the team can run.</li>
      <li data-n="2"><strong>List the steps in order,</strong> with what each step produces. Gather, organize, draft, review.</li>
      <li data-n="3"><strong>Define the handoffs:</strong> what exactly passes from one step to the next. Artifacts, not conversations.</li>
      <li data-n="4"><strong>Set the checkpoints:</strong> where it pauses and waits for you. Money moves, public output, and judgment calls always checkpoint.</li>
    </ol>
    <div class="promptbox"><span class="plabel">Copy-paste: turn anything into a workflow</span><p>"Turn this into a reusable workflow: [describe the outcome]. Break it into steps. For each step, tell me what it needs as input and what it produces as output. Mark the checkpoints where you must pause and wait for my approval."</p></div>
    <div class="big-idea">
      <span class="kicker">The big idea</span>
      <p><strong>A workflow you write once and run fifty times is fifty tasks you never delegate again.</strong></p>
    </div>

    <h2><span class="secnum">04</span>Feed it your data: APIs, docs, and knowledge bases</h2>
    <p>The biggest jump in output quality comes from inputs, not prompts. Give your agents your world. Your docs: paste the manual, upload the price sheet, share the policy. Your data: the spreadsheet, the notes, the customer list. Your live tools: connected through APIs so the agent can check the real numbers instead of guessing.</p>
    <p>This is where plugmyagent earns its keep: the catalog lists 450+ free APIs your agents can call, and the MCP server directory wires tools straight into your agent with copy-paste config.</p>
    <div class="promptbox"><span class="plabel good">Do it hands-on</span><p>Walkthrough W03 connects your first MCP server in five minutes, no API keys needed. <a href="/guides/walkthroughs/first-mcp-server/" style="color: var(--yellow);">Start W03 &rarr;</a></p></div>
    <div class="promptbox"><span class="plabel bad">Generic answers</span><p>An agent answering from training data alone. Confident, outdated, and wrong about your prices.</p></div>
    <div class="promptbox"><span class="plabel good">Your answers</span><p>The same agent with your price sheet, your return policy, and your shipping API. Now it answers like your best rep, at 2am, instantly.</p></div>
    <div class="big-idea">
      <span class="kicker">The data rule</span>
      <p><strong>Never let an agent guess what it could look up.</strong> If the answer exists in your docs or your tools, connect it before you prompt.</p>
    </div>

    <h2><span class="secnum">05</span>Guardrails and evals: trust, but verify</h2>
    <p>The more your agents do on their own, the more you need ways to catch mistakes early. Three mechanisms, all plain English.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Show your work.</strong> "Cite your sources for every claim." If it cannot point at the source, it does not ship.</li>
      <li data-n="2"><strong>Spot checks.</strong> Audit a random sample every week. Five minutes, once a week, catches drift before it becomes damage.</li>
      <li data-n="3"><strong>Golden examples.</strong> Keep 3 to 5 cases where you know the right answer cold. When you change a workflow, run it against those cases first. If it fails a golden example, it does not go live.</li>
    </ol>
    <div class="big-idea">
      <span class="kicker">The eval habit</span>
      <p>Before you trust a new workflow, run it on three cases where you already know the answer. <strong>New workflows earn trust. They do not start with it.</strong></p>
    </div>

    <h2><span class="secnum">06</span>Run it like an ops team</h2>
    <p>At this level you are managing, not prompting. Borrow the structure real teams use.</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>Roles</h3><p>Who does what: your researcher, your planner, your maker, your checker. Write it down once.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>The standup</h3><p>Your morning briefing becomes the team's roll call: what ran overnight, what needs you, what is next.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Escalation rules</h3><p>The advanced approval habit: "Handle it unless money moves, a customer is involved, or you are less than 80% sure. Then bring it to me with your recommendation."</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>The weekly review</h3><p>Fifteen minutes every Friday: what worked, what broke, one improvement for next week. Systems that do not get reviewed quietly rot.</p></div>
    </div>
    <div class="big-idea">
      <span class="kicker">The big idea</span>
      <p><strong>You are not using an AI anymore. You are running a small ops team that happens to be software.</strong> Manage it like one.</p>
    </div>

    <h2><span class="secnum">07</span>Know the costs: tokens, limits, and picking your model</h2>
    <p>Every request costs compute, and the bill is real whether you see it or not. The advanced skill is spending it where it matters.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Big models for judgment calls.</strong> Negotiations, strategy, anything where nuance matters.</li>
      <li data-n="2"><strong>Small, fast models for grunt work.</strong> Sorting, summarizing, reformatting, first drafts.</li>
      <li data-n="3"><strong>Batch the routine.</strong> One scheduled sweep beats twenty ad-hoc questions.</li>
      <li data-n="4"><strong>Respect rate limits.</strong> Space out heavy jobs. Run the big ones overnight.</li>
    </ol>
    <div class="big-idea">
      <span class="kicker">The 80/20 rule</span>
      <p><strong>80% of the value comes from cheap, consistent automation.</strong> Save the heavyweight model for the 20% where judgment actually matters. Most people do the reverse.</p>
    </div>

    <h2><span class="secnum">08</span>Four advanced plays</h2>
    <p>Copy, paste, customize. Each one composes multiple agents.</p>
    <div class="promptbox"><span class="plabel">Play 1: the research swarm</span><p>"Break [question] into 4 angles. Research each angle in parallel. Then merge everything into one brief: the consensus, the disagreements, and the 3 sources I should read myself."</p></div>
    <div class="promptbox"><span class="plabel">Play 2: the content pipeline</span><p>"Take my [rough notes] and run the pipeline: planner makes the outline, maker drafts all three formats [post, email, one-pager], checker enforces my voice rules [short, no fluff, no hype]. Show me only the final drafts."</p></div>
    <div class="promptbox"><span class="plabel">Play 3: the data watchdog</span><p>"Watch [spreadsheet / API / price feed]. Alert me the moment anything moves more than [X] or breaks the pattern. Include what changed and a draft of the response."</p></div>
    <div class="promptbox"><span class="plabel">Play 4: the personal CRM</span><p>"After every meeting I log, record: what was decided, what I promised, and the follow-up date. Every Friday, send me the open loops: what is overdue, what is due next week, and who I have not followed up with."</p></div>

    <h2><span class="secnum">09</span>What&apos;s next</h2>
    <p>You have gone from chatbot to coworker to systems builder to leverage. You delegate tasks, build systems, and compose teams of agents wired to your data.</p>
    <div class="big-idea">
      <span class="kicker">Put it into practice</span>
      <p><strong>Reading about leverage is not leverage.</strong> <a href="/guides/walkthroughs/openclaw-setup/" style="color: var(--yellow);">Walkthrough W02</a> sets up your own self-hosted agent, and <a href="/guides/walkthroughs/first-mcp-server/" style="color: var(--yellow);">walkthrough W03</a> plugs in its first tool. That is the whole advanced stack, running on your machine.</p>
    </div>

    <div class="dlbox">
      <h3>Take this guide with you</h3>
      <p>The full advanced guide as a clean, shareable PDF. Same series, same format.</p>
      <a class="btn btn-neon" href="./ai-agents-advanced-guide.pdf" download>Download the PDF</a>
    </div>
    <a class="guide-card" href="/guides/intermediate-guide-to-ai-agents/">
      <span class="gnum">002</span>
      <span>
        <h3>Missed the second one?</h3>
        <p>From Tasks to Systems: stop assigning tasks and start building systems. Memory that matters, connected tools, schedules that stick, and five copy-paste plays.</p>
        <span class="gmeta">Intermediate &middot; 10 min read &middot; PDF included</span>
      </span>
    </a>
  </article>
</main>
"""


INDEX_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Pillar 04 // Guides</div>
      <h1>Guides that take you<br><span class="neon">from curious to dangerous.</span></h1>
      <p class="lede">Plain-English walkthroughs for the agentic era. No jargon, no computer science degree, just the shortest path from "what is this" to "look what I built."</p>
    </div>
  </section>
  <div class="article">
    <div class="big-idea first">
      <span class="kicker">Start here</span>
      <p><strong>New to all of this? Read guide 001 (8 min), then do walkthrough W01 (10 min).</strong> That pair is the whole on-ramp: the ideas first, then your hands on the keyboard. Everything else builds on those two.</p>
    </div>
    <span class="index-kicker">Learn</span>
    <h2 class="index-h">The guides</h2>
    <p class="index-sub">Read these to understand what AI agents can do and how to think about them. Read in order.</p>
    <a class="guide-card" href="/guides/beginners-guide-to-ai-agents/">
      <span class="gnum">001</span>
      <span>
        <h3>From Chatbot to Coworker: A Beginner's Guide to AI Agents</h3>
        <p>You already know how to chat with AI. This guide teaches the real unlock: handing your personal AI agent actual work. The chatbot-to-agent shift, what to delegate, how to prompt well, and five starter tasks for your first week.</p>
        <span class="gmeta">Beginner &middot; 8 min read &middot; PDF included</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/intermediate-guide-to-ai-agents/">
      <span class="gnum">002</span>
      <span>
        <h3>From Tasks to Systems: An Intermediate Guide to AI Agents</h3>
        <p>The sequel: stop assigning tasks and start building systems. Memory that matters, connected tools, schedules that stick, long projects, and five copy-paste plays.</p>
        <span class="gmeta">Intermediate &middot; 10 min read &middot; PDF included</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/advanced-guide-to-ai-agents/">
      <span class="gnum">003</span>
      <span>
        <h3>From Systems to Leverage: An Advanced Guide to AI Agents</h3>
        <p>The finale of the trilogy: compose teams of specialist agents, build your own workflows, feed them your data, and run the whole thing like a small ops team.</p>
        <span class="gmeta">Advanced &middot; 12 min read &middot; PDF included</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/connect-your-first-api/">
      <span class="gnum">004</span>
      <span>
        <h3>Connect Your First API: Zero to Working Agent in 10 Minutes</h3>
        <p>The hands-on setup guide: pick a free API, connect it to any agent, and run your first live test. No signup on the fast path, no specific agent required.</p>
        <span class="gmeta">Beginner &middot; 10 min &middot; Hands-on</span>
      </span>
    </a>
    <span class="index-kicker">Do</span>
    <h2 class="index-h">Pick your setup track</h2>
    <p class="index-sub">Two ways to get a working agent. Pick one, not both. Whichever you choose, guide 004 connects its first API.</p>
    <div class="big-idea">
      <span class="kicker">Track A: the 10-minute agent</span>
      <p><strong>On your phone in 10 minutes, no terminal.</strong> You end up with a Muse agent, ready for tools.</p>
    </div>
    <a class="guide-card" href="/guides/walkthroughs/your-first-ai-agent/">
      <span class="gnum">W01</span>
      <span>
        <h3>Your first AI agent, set up in 10 minutes</h3>
        <p>From zero to a working personal AI agent: account, app, and your first real task. The hands-on companion to guide 001.</p>
        <span class="gmeta">10 min &middot; Beginner &middot; Free to start</span>
      </span>
    </a>
    <div class="big-idea">
      <span class="kicker">Track B: the self-hosted agent</span>
      <p><strong>On your own machine, fully yours.</strong> Do W02, then W03. You end up with an OpenClaw agent with MCP plug-ins.</p>
    </div>
    <a class="guide-card" href="/guides/walkthroughs/openclaw-setup/">
      <span class="gnum">W02</span>
      <span>
        <h3>Set up OpenClaw: your own self-hosted agent</h3>
        <p>Install the free, open-source agent on your own machine, run the onboarding wizard, and chat with it from your browser or phone.</p>
        <span class="gmeta">20 min &middot; Intermediate &middot; Free and open source</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/walkthroughs/first-mcp-server/">
      <span class="gnum">W03</span>
      <span>
        <h3>Connect your first MCP server</h3>
        <p>Give your agent its first plug-in: the official Fetch server, added with one command. No API keys, five minutes. Puts guide 002's "connect your world" into practice.</p>
        <span class="gmeta">5 min &middot; Beginner &middot; Free</span>
      </span>
    </a>
    <div class="big-idea">
      <div class="big-idea">
      <span class="kicker">After either track</span>
      <p><strong>Guide 004 works with whichever agent you just made:</strong> <a href="/guides/connect-your-first-api/" style="color: var(--yellow);">connect your first API in 10 minutes &rarr;</a></p>
    </div>
    <div class="big-idea">
      <span class="kicker">After that</span>
      <p><strong>Tool-by-tool deep dives for the agents in your stack.</strong> Guides are hand-written and kept current.</p>
    </div>
  </div>
</main>
"""


WALK_CSS = """<style>
.codeblock { position: relative; background: #0e1111; border: 1px solid var(--line); border-radius: var(--radius-sm); margin: 18px 0 24px; overflow: hidden; }
.codeblock pre { margin: 0; padding: 18px 76px 18px 20px; overflow-x: auto; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 13.5px; line-height: 1.65; color: #d7dcd8; white-space: pre; }
.codeblock .copy-btn { position: absolute; top: 10px; right: 10px; background: var(--white); border: 1px solid var(--line); color: var(--muted); font-family: "Azeret Mono", ui-monospace, monospace; font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; padding: 7px 12px; border-radius: 8px; cursor: pointer; transition: color .15s, border-color .15s; }
.codeblock .copy-btn:hover { color: var(--yellow); border-color: var(--yellow); }
.codeblock .copy-btn.copied { color: var(--green); border-color: var(--green); }
.codeblock .cblabel { display: block; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); padding: 12px 20px 0; }
.wmeta { display: flex; gap: 10px; flex-wrap: wrap; margin: 0 0 26px; }
.wmeta span { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 7px 14px; }
.wmeta span.hot { color: var(--yellow); border-color: var(--yellow); }
.article code { font-family: "Azeret Mono", ui-monospace, monospace; font-size: .88em; background: #161a1a; border: 1px solid var(--line); border-radius: 6px; padding: 2px 7px; color: var(--yellow); }
.success { border: 1px solid var(--line); border-left: 4px solid var(--green); background: var(--white); border-radius: var(--radius-sm); padding: 18px 20px; margin: 20px 0 30px; }
.success .k { font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--green); display: block; margin-bottom: 8px; }
.success p { margin: 0; font-size: 15px; }
.trouble { border: 1px solid var(--line); border-radius: var(--radius-md); padding: 24px; margin: 34px 0; background: var(--white); }
.trouble h3 { margin: 0 0 6px; font-size: 19px; }
.trouble details { border-top: 1px solid var(--line); padding: 14px 0; }
.trouble details:first-of-type { border-top: 0; }
.trouble summary { cursor: pointer; font-weight: 600; font-size: 15.5px; list-style: none; }
.trouble summary::-webkit-details-marker { display: none; }
.trouble summary::before { content: "+ "; color: var(--yellow); font-weight: 700; }
.trouble details[open] summary::before { content: "- "; }
.trouble summary:hover { color: var(--yellow); }
.trouble details p { margin: 10px 0 0; font-size: 15px; color: var(--muted); }
.trouble details .codeblock { margin: 12px 0 4px; }
.backlink { display: inline-block; font-family: "Azeret Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); text-decoration: none; margin-bottom: 26px; }
.backlink:hover { color: var(--yellow); }
</style>
"""

WALK_SCRIPT = """<script>
(function(){
  document.querySelectorAll(".codeblock").forEach(function(block){
    var btn = block.querySelector(".copy-btn");
    var pre = block.querySelector("pre");
    if (!btn || !pre) return;
    btn.addEventListener("click", function(){
      var text = pre.innerText;
      var done = function(){
        btn.textContent = "Copied";
        btn.classList.add("copied");
        setTimeout(function(){ btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1600);
      };
      var fallback = function(){
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch(e){}
        document.body.removeChild(ta); done();
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
    });
  });
})();
</script>
"""

WALKHUB_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Walkthroughs</div>
      <h1>Setup walkthroughs<br><span class="neon">that work the first time.</span></h1>
      <p class="lede">Keys, auth, and copy-paste config blocks, every step verified against the official documentation. Two tracks, one choice: the 10-minute phone agent or the self-hosted machine agent.</p>
    </div>
  </section>
  <div class="article">
    <a class="backlink" href="/guides/">&larr; All guides</a>
    <p><strong>The hands-on half of the guides.</strong> The guides teach the ideas; these get you set up. Brand new? Read <a href="/guides/beginners-guide-to-ai-agents/" style="color: var(--yellow);">guide 001</a> first, then pick your track below.</p>
    <div class="big-idea">
      <span class="kicker">Track A: the 10-minute agent</span>
      <p><strong>Want it on your phone in 10 minutes, no terminal?</strong> Start here. You end up with a Muse agent on your phone, ready for tools.</p>
    </div>
    <a class="guide-card" href="/guides/walkthroughs/your-first-ai-agent/">
      <span class="gnum">W01</span>
      <span>
        <h3>Your first AI agent, set up in 10 minutes</h3>
        <p>From zero to a working personal AI agent: account, app, and your first real task. Uses Muse as the running example.</p>
        <span class="gmeta">10 min &middot; Beginner &middot; Free to start</span>
      </span>
    </a>
    <div class="big-idea">
      <span class="kicker">Track B: the self-hosted agent</span>
      <p><strong>Want it on your own machine, fully yours?</strong> Do W02, then W03. You end up with an OpenClaw agent on your computer with MCP plug-ins.</p>
    </div>
    <a class="guide-card" href="/guides/walkthroughs/openclaw-setup/">
      <span class="gnum">W02</span>
      <span>
        <h3>Set up OpenClaw: your own self-hosted agent</h3>
        <p>Install the free, open-source agent on your own machine, run the onboarding wizard, and chat with it from your browser or phone.</p>
        <span class="gmeta">20 min &middot; Intermediate &middot; Free and open source</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/walkthroughs/first-mcp-server/">
      <span class="gnum">W03</span>
      <span>
        <h3>Connect your first MCP server</h3>
        <p>Give your agent its first plug-in: the official Fetch server, added with one command. No API keys, five minutes.</p>
        <span class="gmeta">5 min &middot; Beginner &middot; Free</span>
      </span>
    </a>
    <div class="big-idea">
      <span class="kicker">After either track</span>
      <p><strong>Guide 004 works with whichever agent you just made.</strong> <a href="/guides/connect-your-first-api/" style="color: var(--yellow);">Connect your first API in 10 minutes &rarr;</a> More walkthroughs are on the way: tool-by-tool deep dives for the agents in your stack.</p>
    </div>
  </div>
</main>
"""

WALK1_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Walkthroughs // W01</div>
      <h1>Your first AI agent,<br><span class="neon">set up in 10 minutes.</span></h1>
      <p class="lede">From zero to a working personal AI agent: account, app, and your first real task. We use Muse as the running example; the steps work the same way for any personal agent.</p>
      <div class="wmeta"><span class="hot">10 minutes</span><span>Beginner</span><span>Free to start</span></div>
    </div>
  </section>
  <article class="article" id="start">
    <div class="crumbs"><a href="/guides/">Guides</a><span class="sep">/</span><a href="/guides/walkthroughs/">Walkthroughs</a><span class="sep">/</span><span class="cur">W01</span></div>
    <p><strong>Goes with guide 001:</strong> <a href="/guides/beginners-guide-to-ai-agents/" style="color: var(--yellow);">From Chatbot to Coworker</a>. Read it first if you have not. This is its hands-on companion.</p>
    <div class="big-idea">
      <span class="kicker">What you end up with</span>
      <p><strong>A Muse agent on your phone, ready in 10 minutes.</strong> This is Track A: the fastest path, no terminal, hosted for you. Want it on your own machine instead? That is <a href="/guides/walkthroughs/openclaw-setup/" style="color: var(--yellow);">Track B, walkthrough W02</a>.</p>
    </div>
    <h2><span class="secnum">01</span>Create your account</h2>
    <p>Open <strong>muse.ai</strong> in your browser and sign up. Use an email address you actually check: login codes and important notices go there.</p>
    <div class="big-idea">
      <span class="kicker">Referral tip</span>
      <p>New to Muse? Enter the code <strong>DGC4EX</strong> in Settings within 48 hours of joining: you get 1 billion tokens, and so does the person who invited you.</p>
    </div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>You are logged in at muse.ai and you see the chat window. That is your agent's home base.</p>
    </div>

    <h2><span class="secnum">02</span>Get the app on your phone</h2>
    <p>Search for Muse in the App Store (iPhone) or Google Play (Android) and install the official app. Log in with the same account you just created.</p>
    <p>Prefer the browser? That works too. The point is having your agent one tap away instead of buried in a tab you never open.</p>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>You are logged in on your phone. Same agent, same memory, two places.</p>
    </div>

    <h2><span class="secnum">03</span>Connect WhatsApp (optional, recommended)</h2>
    <p>In Settings, find WhatsApp linking and follow the prompts to connect your number. This puts your agent inside the app you already check fifty times a day.</p>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>Send your agent a message from WhatsApp and get a reply. Now it lives where you live.</p>
    </div>

    <h2><span class="secnum">04</span>Give it one real task</h2>
    <p>Do not start with "what can you do." Start with something from your actual life.</p>
    <div class="promptbox"><span class="plabel">Copy, paste, customize</span><p>"Here is what is on my plate this week: [paste your list]. Turn it into a prioritized plan for Monday to Friday, with time estimates. Flag anything that looks unrealistic."</p></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>It hands back a finished plan, not just advice. If it asks a clarifying question first, that is good: it is scoping the job before doing it.</p>
    </div>

    <div class="trouble">
      <h3>When something goes wrong</h3>
      <details>
        <summary>I am outside the US or Canada and cannot sign up</summary>
        <p>Muse currently serves the US and Canada. If you are elsewhere, skip to walkthrough W02: OpenClaw is self-hosted and has no region limits.</p>
      </details>
      <details>
        <summary>The WhatsApp code never arrives</summary>
        <p>Check the number for typos, wait two minutes, then request a new code. Still nothing? Use the app or the web for now and retry tomorrow. This step is optional.</p>
      </details>
      <details>
        <summary>It answered like a chatbot instead of doing the work</summary>
        <p>Give it the delegation recipe from guide 001: the outcome, the context, the constraints, and the check ("show me before you send anything"). Then run the task again.</p>
      </details>
    </div>

    <a class="guide-card" href="/guides/walkthroughs/openclaw-setup/">
      <span class="gnum">W02</span>
      <span>
        <h3>Next: set up OpenClaw</h3>
        <p>Your own self-hosted AI agent on your own machine: install, onboard, and chat from your browser or phone.</p>
        <span class="gmeta">20 min &middot; Intermediate &middot; Free and open source</span>
      </span>
    </a>
  </article>
</main>
"""

WALK2_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Walkthroughs // W02</div>
      <h1>Set up OpenClaw:<br><span class="neon">your own self-hosted agent.</span></h1>
      <p class="lede">OpenClaw is a free, open-source AI agent that runs on your own machine and talks to you through a browser dashboard, WhatsApp, or Telegram. This walkthrough takes you from zero to your first chat.</p>
      <div class="wmeta"><span class="hot">20 minutes</span><span>Intermediate</span><span>Free and open source</span></div>
    </div>
  </section>
  <article class="article" id="start">
    <div class="crumbs"><a href="/guides/">Guides</a><span class="sep">/</span><a href="/guides/walkthroughs/">Walkthroughs</a><span class="sep">/</span><span class="cur">W02</span></div>
    <p><strong>Track B, part 1 of 2.</strong> This is the self-hosted path; <a href="/guides/walkthroughs/first-mcp-server/" style="color: var(--yellow);">walkthrough W03</a> then adds its first MCP server. On the phone path instead? Start at <a href="/guides/walkthroughs/your-first-ai-agent/" style="color: var(--yellow);">walkthrough W01</a>.</p>
    <div class="big-idea">
      <span class="kicker">What you end up with</span>
      <p><strong>An OpenClaw agent running on your own machine.</strong> This is Track B: self-hosted, fully yours, terminal required. Want the 10-minute phone path instead? That is <a href="/guides/walkthroughs/your-first-ai-agent/" style="color: var(--yellow);">Track A, walkthrough W01</a>.</p>
    </div>
    <h2><span class="secnum">01</span>Install Node.js 22 or newer</h2>
    <p>OpenClaw runs on Node.js, version 22 or higher. Check what you have:</p>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>node --version</pre></div>
    <p>No Node yet, or the version is too old? Install the LTS release from nodejs.org, then close your terminal completely and open a fresh one.</p>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>The terminal prints a version like v22.14.0 or higher.</p>
    </div>

    <h2><span class="secnum">02</span>Install OpenClaw</h2>
    <p>On macOS or Linux, run the official installer:</p>
    <div class="codeblock"><span class="cblabel">macOS / Linux</span><button class="copy-btn" type="button">Copy</button><pre>curl -fsSL https://openclaw.ai/install.sh | bash</pre></div>
    <p>On Windows, open PowerShell and run:</p>
    <div class="codeblock"><span class="cblabel">Windows PowerShell</span><button class="copy-btn" type="button">Copy</button><pre>iwr -useb https://openclaw.ai/install.ps1 | iex</pre></div>
    <p>Prefer npm? This works too:</p>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>npm install -g openclaw@latest</pre></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p><code>openclaw --version</code> prints a version number. The command exists and your terminal knows where it lives.</p>
    </div>

    <h2><span class="secnum">03</span>Run the onboarding wizard</h2>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw onboard --install-daemon</pre></div>
    <p>The wizard walks you through three decisions in plain words:</p>
    <ol>
      <li><strong>Which AI model powers your agent.</strong> Pick Anthropic, OpenAI, OpenRouter, or a local model via Ollama. The hosted options need an API key; the wizard asks for it and stores it securely.</li>
      <li><strong>How the gateway runs.</strong> Accept the default: the wizard installs it as a background service so your agent keeps working when the terminal is closed.</li>
      <li><strong>Which chat channels to connect.</strong> WhatsApp, Telegram, Discord. You can add these later too.</li>
    </ol>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>The wizard finishes without errors. Your settings live in <code>~/.openclaw/openclaw.json</code> and your agent's workspace in <code>~/.openclaw/workspace</code>.</p>
    </div>

    <h2><span class="secnum">04</span>Check that it is alive</h2>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw gateway status</pre></div>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw health</pre></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>Gateway status says running. Health reports OK. If either one complains, jump to troubleshooting below before continuing.</p>
    </div>

    <h2><span class="secnum">05</span>Open the dashboard and say hello</h2>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw dashboard</pre></div>
    <p>Or open <strong>http://127.0.0.1:18789/</strong> directly in your browser. This is your agent's control room: chat, integrations, and settings in one place.</p>
    <div class="promptbox"><span class="plabel">Your first message</span><p>"Hi. Tell me what you can do, and what you need from me to do it well."</p></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>The dashboard loads and your agent answers. You now have a working self-hosted agent.</p>
    </div>

    <h2><span class="secnum">06</span>Connect your phone (optional)</h2>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw channels login</pre></div>
    <p>Follow the prompts to link WhatsApp or Telegram. Message your agent from your phone and get a reply.</p>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>A message sent from your phone gets an answer from your agent. Same brain, new doorway.</p>
    </div>

    <div class="trouble">
      <h3>When something goes wrong</h3>
      <details>
        <summary><code>openclaw: command not found</code> after installing</summary>
        <p>Close the terminal completely and open a fresh one so it picks up the new PATH. Still missing? Re-run the installer and read its output for errors.</p>
      </details>
      <details>
        <summary>The gateway will not start, or the port is busy</summary>
        <p>Run it in the foreground to see the actual error:</p>
        <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw gateway --port 18789</pre></div>
        <p>The most common cause is a second copy already running.</p>
      </details>
      <details>
        <summary>On Linux, the agent dies when I log out</summary>
        <p>The official docs call this out: the background service needs lingering enabled so it survives logout:</p>
        <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>sudo loginctl enable-linger $USER</pre></div>
      </details>
      <details>
        <summary>The wizard asks for a model provider and I have no API key</summary>
        <p>Two free paths: choose the local option via Ollama for a fully free setup, or grab a pay-as-you-go key from OpenRouter. Keys go into the wizard, never into a chat.</p>
      </details>
    </div>

    <a class="guide-card" href="/guides/walkthroughs/first-mcp-server/">
      <span class="gnum">W03</span>
      <span>
        <h3>Next: connect your first MCP server</h3>
        <p>Give your new agent its first plug-in: the official Fetch server, added with one command. No API keys, five minutes.</p>
        <span class="gmeta">5 min &middot; Beginner &middot; Free</span>
      </span>
    </a>
  </article>
</main>
"""

WALK3_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Walkthroughs // W03</div>
      <h1>Connect your first<br><span class="neon">MCP server.</span></h1>
      <p class="lede">MCP servers are plug-ins that give your agent new abilities: reading web pages, searching docs, querying databases. This walkthrough adds one server to OpenClaw in under five minutes. No API keys needed.</p>
      <div class="wmeta"><span class="hot">5 minutes</span><span>Beginner</span><span>Free</span></div>
    </div>
  </section>
  <article class="article" id="start">
    <div class="crumbs"><a href="/guides/">Guides</a><span class="sep">/</span><a href="/guides/walkthroughs/">Walkthroughs</a><span class="sep">/</span><span class="cur">W03</span></div>
    <p><strong>Goes with guide 002, section 03</strong> (<a href="/guides/intermediate-guide-to-ai-agents/" style="color: var(--yellow);">Connect your world</a>). This is that section, hands-on.</p>
    <p><strong>Prerequisite:</strong> OpenClaw installed and running. Not there yet? Do <a href="/guides/walkthroughs/openclaw-setup/" style="color: var(--yellow);">walkthrough W02</a> first.</p>
    <div class="big-idea">
      <span class="kicker">What you end up with</span>
      <p><strong>MCP plug-ins on your OpenClaw agent.</strong> This is Track B, part 2 of 2, and it only applies to the OpenClaw agent from W02. On the phone track? <a href="/guides/connect-your-first-api/" style="color: var(--yellow);">Guide 004</a> connects APIs to any agent instead.</p>
    </div>

    <h2><span class="secnum">01</span>Add the Fetch server with one command</h2>
    <p>Fetch is maintained by the MCP team and gives your agent one new ability: fetch any web page and read it as clean text. It needs no API key and no settings beyond its name.</p>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw mcp set fetch '{"command":"npx","args":["-y","@modelcontextprotocol/server-fetch"]}'</pre></div>
    <p>Reading that command: the server is named <code>fetch</code>, it launches with <code>npx</code>, and the <code>-y</code> flag lets npx download the official package automatically.</p>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>Run <code>openclaw mcp list</code>. You see <code>fetch</code> in the list. It is registered.</p>
    </div>

    <h2><span class="secnum">02</span>Confirm it loaded</h2>
    <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw mcp show fetch --json</pre></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>You see the server's details and its <code>fetch</code> tool. Your agent can now call it.</p>
    </div>

    <h2><span class="secnum">03</span>Ask your agent to use it</h2>
    <p>Open your OpenClaw dashboard and send this:</p>
    <div class="promptbox"><span class="plabel">Copy, paste, send</span><p>"Fetch https://example.com and tell me what it says."</p></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>Your agent returns a summary of the page instead of saying it cannot browse. That is your first MCP-powered answer.</p>
    </div>

    <h2><span class="secnum">04</span>Understand what you just configured</h2>
    <p>Every MCP server is one entry under <code>mcp.servers</code> in OpenClaw's config file (<code>~/.openclaw/openclaw.json</code>). Two shapes cover almost everything:</p>
    <div class="codeblock"><span class="cblabel">Local server: launched on your machine</span><button class="copy-btn" type="button">Copy</button><pre>{
  "mcp": {
    "servers": {
      "fetch": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-fetch"]
      }
    }
  }
}</pre></div>
    <div class="codeblock"><span class="cblabel">Remote server: runs somewhere else, key in headers</span><button class="copy-btn" type="button">Copy</button><pre>{
  "mcp": {
    "servers": {
      "docs": {
        "url": "https://mcp.example.com",
        "transport": "streamable-http",
        "headers": { "Authorization": "Bearer YOUR_KEY_HERE" }
      }
    }
  }
}</pre></div>
    <p>The CLI writes this config for you, so you rarely edit the file by hand. One rule from the official docs: never put real secrets inline in the config. Use an environment variable like <code>${MY_API_KEY}</code> and export it before starting the gateway.</p>
    <div class="big-idea">
      <span class="kicker">The pattern</span>
      <p><strong>Pick a server, run <code>openclaw mcp set</code>, check <code>openclaw mcp list</code>, test it.</strong> That is the whole skill. Every future server works the same way.</p>
    </div>

    <h2><span class="secnum">05</span>Find your second server</h2>
    <p>Browse the plugmyagent MCP directory: 34 free servers, every one verified, each with copy-paste config. Pick one that solves a problem you actually have.</p>
    <a class="guide-card" href="/mcp/">
      <span class="gnum">MCP</span>
      <span>
        <h3>The MCP server directory</h3>
        <p>34 genuinely free MCP servers with install commands, copy buttons, and category search. Find your next plug-in.</p>
        <span class="gmeta">Free &middot; Verified &middot; Copy-paste configs</span>
      </span>
    </a>

    <div class="trouble">
      <h3>When something goes wrong</h3>
      <details>
        <summary>The first run hangs for a minute</summary>
        <p>npx is downloading the package the first time. Give it a minute on a decent connection. It is instant on every run after that.</p>
      </details>
      <details>
        <summary>The server is listed but the agent says it cannot use it</summary>
        <p>Start a fresh session so the agent picks up the new tools. If it persists, run <code>openclaw mcp show fetch --json</code> and read the error it reports.</p>
      </details>
      <details>
        <summary>I want to remove a server</summary>
        <div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>openclaw mcp unset fetch</pre></div>
        <p>Then <code>openclaw mcp list</code> to confirm it is gone.</p>
      </details>
    </div>
  </article>
</main>
"""

SETUP_BODY = """<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Guides // Pillar 04 // Guide 004</div>
      <h1>Connect your first API:<br><span class="neon">zero to working agent in 10 minutes.</span></h1>
      <p class="lede">No signup on the fast path. No specific agent required. In ten minutes your agent will call a real API and bring back live data. That is the whole guide, and it works with whatever agent you already use.</p>
      <div class="hero-cta">
        <a class="btn btn-neon" href="#start">Start the 10 minutes</a>
        <a class="btn btn-ghost" href="/catalog/">Browse the catalog</a>
      </div>
    </div>
  </section>

  <article class="article" id="start">
    <div class="big-idea">
      <span class="kicker">The promise</span>
      <p><strong>Ten minutes from now, you will ask your agent something it cannot answer from training data, and it will go fetch the real answer from a live API.</strong> A chatting agent is a toy. A working agent has tools. This guide connects the first one.</p>
    </div>
    <div class="promptbox"><span class="plabel">No agent yet?</span><p><a href="/guides/" style="color: var(--yellow);">Pick a setup track on the guides page</a> (10 minutes), then come back here. This guide works with whichever agent you choose.</p></div>

    <h2><span class="secnum">01</span>The finish line: what "working" looks like</h2>
    <p>Right now your agent chats. After this guide, it acts. You will ask "what is the temperature in Berlin right now" and it will go get the number from a live weather API instead of guessing from memory.</p>
    <p>That gap, between answering from memory and fetching live data, is the entire skill. Everything else on this site is a variation of it.</p>
    <div class="promptbox"><span class="plabel good">Your minute-9 test</span><p>"What is the current temperature in Berlin?" If the answer is a live number, you are done. If it says "Berlin is usually around...", it guessed. Section 05 fixes that in one sentence.</p></div>

    <h2><span class="secnum">02</span>Minutes 0 to 2: pick a boring API</h2>
    <p>For the 10-minute path, pick an API that needs no signup and no key. In the catalog, these carry the <strong>no signup</strong> effort badge. No forms, no waiting for a key email, nothing between you and a working test.</p>
    <ol class="checklist">
      <li data-n="1"><strong>Open the catalog</strong> and look for the no signup badge.</li>
      <li data-n="2"><strong>Pick one you understand.</strong> Weather, crypto prices, jokes, IP lookup. If you know what it should return, you will know instantly whether it worked.</li>
      <li data-n="3"><strong>Copy the endpoint URL</strong> from the API page. That long https address is the tool's address. You hand it to your agent in the next step.</li>
    </ol>
    <div class="big-idea">
      <span class="kicker">Boring is the point</span>
      <p><strong>Your first API should be boring. You are testing the plumbing, not building the product.</strong> Fancy comes later, after the pattern is proven.</p>
    </div>

    <h2><span class="secnum">03</span>Minutes 2 to 4: the only three moves</h2>
    <p>Every API on this site connects the same way. Three moves, no exceptions:</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>1. Get access</h3><p>Copy the endpoint. Grab a key only if the API asks for one. Yours does not, which is why you picked it.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>2. Connect it</h3><p>Tell your agent the tool exists: its address and what it returns. Plain words work.</p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>3. Test it</h3><p>Ask one question only this API can answer. Live data back means it worked.</p></div>
    </div>
    <p>Keys, plug-ins, and libraries are all fancier versions of these three moves. Learn them here and you already know most of every setup on the site.</p>

    <h2><span class="secnum">04</span>Minutes 4 to 7: hand the tool to your agent</h2>
    <p>Your agent needs two things: the <strong>address</strong> (the endpoint URL you copied) and a <strong>description</strong> of what comes back. Open wherever your agent manages tools. It is usually called Tools, Integrations, Plugins, or Actions. Every agent has one.</p>
    <p>Add it like this, using a real keyless weather API as the example:</p>
    <div class="codeblock"><span class="cblabel">The tool, in plain words</span><button class="copy-btn" type="button">Copy</button><pre>Tool name: Current weather
Address: https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m
Use it when: I ask about weather or temperature anywhere.
It returns: JSON with the current temperature in Celsius.</pre></div>
    <p>If your agent takes tools as a chat message instead of a settings screen, send it exactly that text. If it has a tools screen, paste the address into the URL field and the rest into the description. Same information, either door.</p>
    <div class="big-idea">
      <span class="kicker">Why plain words work</span>
      <p><strong>You are not programming. You are delegating.</strong> Brief it the way you would brief a person: here is the tool, here is when to use it, here is what good looks like. Agents are fluent in plain words.</p>
    </div>

    <h2><span class="secnum">05</span>Minutes 7 to 9: run the test</h2>
    <p>Ask the one question:</p>
    <div class="promptbox"><span class="plabel">The test</span><p>"What is the current temperature in Berlin?"</p></div>
    <div class="success">
      <span class="k">What success looks like</span>
      <p>It answers with a specific number, in Celsius, that matches the real world right now. Check it against any weather site if you like. A live number means the tool fired. You have a working agent.</p>
    </div>
    <div class="promptbox"><span class="plabel bad">If it answers from memory</span><p>"Berlin is usually around 15 degrees this time of year" means it guessed without calling the tool. Fix it in one sentence: <strong>"No. Use the weather tool I just gave you and read the number from its response."</strong> Then ask again.</p></div>

    <h2><span class="secnum">06</span>Minute 9 to 10: make it yours</h2>
    <p>You now know the three moves. Add a second tool, a fun one this time: a joke API, a crypto price, the space station location. Same three moves, second rep. Two working tools means the pattern is yours, not luck.</p>
    <p>And when you are ready for APIs that need a key, that is just move 1 with one extra step. Section 07 covers it in 60 seconds.</p>
    <div class="cards">
      <div class="gcard"><h3><span class="ico">&#9679;</span>Free API keys</h3><p>Most of the catalog. One extra step: the key travels in the request header. <a href="#keys" style="color: var(--yellow);">The 60-second version &darr;</a></p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>MCP servers</h3><p>For agents that speak MCP: tools install with one command and a config block. <a href="/guides/walkthroughs/first-mcp-server/" style="color: var(--yellow);">Walkthrough W03 does it in 5 minutes &rarr;</a></p></div>
      <div class="gcard"><h3><span class="ico">&#9679;</span>Libraries</h3><p>JavaScript components install with npm and import in one line. <a href="/components/" style="color: var(--yellow);">Browse the components pillar &rarr;</a></p></div>
    </div>

    <h2 id="keys"><span class="secnum">07</span>The 60-second key version</h2>
    <p>Your second API will probably ask for a free key. Get it from the provider's site (free tier, no card on this catalog's listings), then send it in the request header. Three patterns cover nearly every API on earth:</p>
    <div class="codeblock"><span class="cblabel">Pattern 1: Bearer token (most common)</span><button class="copy-btn" type="button">Copy</button><pre>curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.example.com/v1/data</pre></div>
    <div class="codeblock"><span class="cblabel">Pattern 2: API key header</span><button class="copy-btn" type="button">Copy</button><pre>curl -H "x-api-key: YOUR_KEY" \
  https://api.example.com/v1/data</pre></div>
    <div class="codeblock"><span class="cblabel">Pattern 3: Key in the URL</span><button class="copy-btn" type="button">Copy</button><pre>curl "https://api.example.com/v1/data?key=YOUR_KEY"</pre></div>
    <p>Your API's page on this site shows which pattern it uses. Tell your agent the same way as before, plus one line: "Send my key in the Authorization header."</p>
    <div class="big-idea">
      <span class="kicker">Key hygiene, the short version</span>
      <p><strong>Keys live in your agent's settings or secure vault. Never in a chat message, never in a screenshot, never in code you share.</strong> If a key leaks, revoke it and make a new one. Section 09 has the full rules.</p>
    </div>

    <h2><span class="secnum">08</span>When it breaks: the 3-minute fix list</h2>
    <p>Something will go wrong once. It is almost always one of these five, and each takes under a minute to fix.</p>
    <div class="promptbox"><span class="plabel bad">401 Unauthorized</span><p>The key is missing, wrong, or in the wrong header. Re-copy it from the provider dashboard and check the pattern in section 07.</p></div>
    <div class="promptbox"><span class="plabel bad">404 Not Found</span><p>The endpoint URL has a typo. Compare it character by character with the API page. One wrong letter is enough.</p></div>
    <div class="promptbox"><span class="plabel bad">429 Too Many Requests</span><p>You asked too fast. Free tiers are generous but not infinite. Wait a minute and try again.</p></div>
    <div class="promptbox"><span class="plabel bad">It answers from memory</span><p>It did not call the tool. Say "use the [name] tool" explicitly, naming it. Agents sometimes need the nudge.</p></div>
    <div class="promptbox"><span class="plabel bad">CORS error (browser only)</span><p>The API refused a direct browser call. Have your agent call it instead, or route it through a tiny server. This one is never your fault.</p></div>

    <h2><span class="secnum">09</span>Key hygiene: the five rules</h2>
    <ol class="checklist">
      <li data-n="1"><strong>Keys live in settings or the vault.</strong> Your agent's secure settings, or an environment variable. That is the entire list of approved homes.</li>
      <li data-n="2"><strong>Never in chat, screenshots, or shared code.</strong> If you would not print it on a t-shirt, do not paste it there.</li>
      <li data-n="3"><strong>One key per project.</strong> If one leaks, you revoke one, not everything.</li>
      <li data-n="4"><strong>Leaked means revoked.</strong> The moment a key escapes, delete it at the provider and make a new one. Do not debate it.</li>
      <li data-n="5"><strong>Free tier, calendar reminder.</strong> If a key came with a trial, set a reminder before it ends. Surprise bills are a choice.</li>
    </ol>

    <div class="big-idea">
      <span class="kicker">You are done</span>
      <p><strong>Three moves: get access, connect it, test it.</strong> You did it in ten minutes with a boring weather API. The same three moves connect every listing on this site. Go collect tools.</p>
    </div>

    <a class="guide-card" href="/guides/walkthroughs/first-mcp-server/">
      <span class="gnum">W03</span>
      <span>
        <h3>Next: your first MCP server</h3>
        <p>The plug-in version of what you just did: install the official Fetch MCP server with one command, five minutes, no API keys.</p>
        <span class="gmeta">5 min &middot; Beginner &middot; Free</span>
      </span>
    </a>
    <a class="guide-card" href="/guides/intermediate-guide-to-ai-agents/">
      <span class="gnum">002</span>
      <span>
        <h3>Then: the intermediate guide</h3>
        <p>From Tasks to Systems: memory that matters, connected tools, schedules that stick, and five copy-paste plays for your newly working agent.</p>
        <span class="gmeta">Intermediate &middot; 10 min read &middot; PDF included</span>
      </span>
    </a>
  </article>
</main>
"""


def page(title, desc, canonical, ogalt, body, footline):
    return HEAD_TMPL.format(title=title, desc=desc, canonical=canonical, ogalt=ogalt) + body + FOOT_TMPL.format(footline=footline)


def main():
    guides_dir = os.path.join(ROOT, "guides")
    post_dir = os.path.join(guides_dir, "beginners-guide-to-ai-agents")
    os.makedirs(post_dir, exist_ok=True)

    index_html = page(
        title="Guides | PlugMyAgent",
        desc="Plain-English walkthroughs for the agentic era: from your first AI agent to power-user setups. Start with the beginner's guide, level up with the intermediate guide, and finish with the advanced guide.",
        canonical="https://www.plugmyagent.com/guides/",
        ogalt="PlugMyAgent Guides: plain-English walkthroughs for the agentic era",
        body=INDEX_BODY,
        footline="Guides are hand-written and kept current. Product details verified against official documentation.",
    )
    with open(os.path.join(guides_dir, "index.html"), "w") as f:
        f.write(index_html)

    post_html = page(
        title="A Beginner's Guide to AI Agents: From Chatbot to Coworker | PlugMyAgent",
        desc="New to AI agents? Learn how AI agents turn 'ask me anything' into 'consider it done': what to delegate, how to prompt well, and five starter tasks for week one.",
        canonical="https://www.plugmyagent.com/guides/beginners-guide-to-ai-agents/",
        ogalt="A beginner's guide to AI agents: from chatbot to coworker, by PlugMyAgent",
        body=GUIDE_BODY,
        footline="Guide written September 23, 2026. Muse product details verified against the official Muse documentation.",
    )
    with open(os.path.join(post_dir, "index.html"), "w") as f:
        f.write(post_html)

    post2_dir = os.path.join(guides_dir, "intermediate-guide-to-ai-agents")
    os.makedirs(post2_dir, exist_ok=True)
    post2_html = page(
        title="An Intermediate Guide to AI Agents: From Tasks to Systems | PlugMyAgent",
        desc="Finished the beginner's guide? Learn to build AI agent systems that run without you: memory, connected tools, schedules, long projects, and five copy-paste plays.",
        canonical="https://www.plugmyagent.com/guides/intermediate-guide-to-ai-agents/",
        ogalt="An intermediate guide to AI agents: from tasks to systems, by PlugMyAgent",
        body=GUIDE2_BODY,
        footline="Guide written September 2026. Muse product details verified against the official Muse documentation.",
    )
    with open(os.path.join(post2_dir, "index.html"), "w") as f:
        f.write(post2_html)

    post3_dir = os.path.join(guides_dir, "advanced-guide-to-ai-agents")
    os.makedirs(post3_dir, exist_ok=True)
    post3_html = page(
        title="An Advanced Guide to AI Agents: From Systems to Leverage | PlugMyAgent",
        desc="Ready for the advanced level? Chain specialist AI agents, build your own workflows, feed them your data, and run the whole thing like a small ops team.",
        canonical="https://www.plugmyagent.com/guides/advanced-guide-to-ai-agents/",
        ogalt="An advanced guide to AI agents: from systems to leverage, by PlugMyAgent",
        body=GUIDE3_BODY,
        footline="Guide written September 2026. Muse product details verified against the official Muse documentation.",
    )
    with open(os.path.join(post3_dir, "index.html"), "w") as f:
        f.write(post3_html)

    walk_dir = os.path.join(guides_dir, "walkthroughs")
    os.makedirs(walk_dir, exist_ok=True)
    hub_html = page(
        title="Setup Walkthroughs | PlugMyAgent",
        desc="Keys, auth, and copy-paste config blocks that work the first time: set up your first AI agent in 10 minutes, install OpenClaw, and connect your first MCP server.",
        canonical="https://www.plugmyagent.com/guides/walkthroughs/",
        ogalt="PlugMyAgent setup walkthroughs: keys, auth, and copy-paste config that works",
        body=WALK_CSS + WALKHUB_BODY,
        footline="Walkthroughs are hand-written and kept current. Product details verified against official documentation.",
    )
    with open(os.path.join(walk_dir, "index.html"), "w") as f:
        f.write(hub_html)

    w1_dir = os.path.join(walk_dir, "your-first-ai-agent")
    os.makedirs(w1_dir, exist_ok=True)
    w1_html = page(
        title="Set Up Your Personal AI Agent in 10 Minutes | PlugMyAgent",
        desc="From zero to a working personal AI agent in 10 minutes: create your account, get the app, connect WhatsApp, and run your first real task.",
        canonical="https://www.plugmyagent.com/guides/walkthroughs/your-first-ai-agent/",
        ogalt="Set up your personal AI agent in 10 minutes, by PlugMyAgent",
        body=WALK_CSS + WALK1_BODY + WALK_SCRIPT,
        footline="Walkthrough written September 2026. Muse product details verified against the official Muse documentation.",
    )
    with open(os.path.join(w1_dir, "index.html"), "w") as f:
        f.write(w1_html)

    w2_dir = os.path.join(walk_dir, "openclaw-setup")
    os.makedirs(w2_dir, exist_ok=True)
    w2_html = page(
        title="OpenClaw Setup: Your Own Self-Hosted AI Agent | PlugMyAgent",
        desc="Install the free, open-source OpenClaw agent on your own machine: Node.js, the official installer, the onboarding wizard, and your first chat.",
        canonical="https://www.plugmyagent.com/guides/walkthroughs/openclaw-setup/",
        ogalt="OpenClaw setup: your own self-hosted AI agent, by PlugMyAgent",
        body=WALK_CSS + WALK2_BODY + WALK_SCRIPT,
        footline="Walkthrough written September 2026. Steps verified against the official OpenClaw documentation (docs.openclaw.ai).",
    )
    with open(os.path.join(w2_dir, "index.html"), "w") as f:
        f.write(w2_html)

    w3_dir = os.path.join(walk_dir, "first-mcp-server")
    os.makedirs(w3_dir, exist_ok=True)
    w3_html = page(
        title="Connect Your First MCP Server | PlugMyAgent",
        desc="Give your agent its first plug-in in five minutes: add the official Fetch MCP server to OpenClaw with one command. No API keys needed.",
        canonical="https://www.plugmyagent.com/guides/walkthroughs/first-mcp-server/",
        ogalt="Connect your first MCP server, by PlugMyAgent",
        body=WALK_CSS + WALK3_BODY + WALK_SCRIPT,
        footline="Walkthrough written September 2026. Steps verified against the official OpenClaw MCP documentation and the official MCP reference servers.",
    )
    with open(os.path.join(w3_dir, "index.html"), "w") as f:
        f.write(w3_html)


    setup_dir = os.path.join(guides_dir, "connect-your-first-api")
    os.makedirs(setup_dir, exist_ok=True)
    setup_html = page(
        title="Connect Your First API: Zero to Working Agent in 10 Minutes | PlugMyAgent",
        desc="A beginner-friendly setup guide for any AI agent: pick a free API, connect it, and run your first live test in 10 minutes. No signup needed on the fast path.",
        canonical="https://www.plugmyagent.com/guides/connect-your-first-api/",
        ogalt="Connect your first API in 10 minutes, by PlugMyAgent",
        body=WALK_CSS + SETUP_BODY + WALK_SCRIPT,
        footline="Guide written September 2026. Steps verified against official API documentation.",
    )
    with open(os.path.join(setup_dir, "index.html"), "w") as f:
        f.write(setup_html)

    for name, html in [("index", index_html), ("post", post_html), ("post2", post2_html),
                       ("post3", post3_html), ("hub", hub_html), ("w1", w1_html),
                       ("w2", w2_html), ("w3", w3_html), ("setup", setup_html)]:
        if chr(0x2014) in html:
            raise SystemExit("em dash found in generated page " + name + "; remove before shipping")

    print("wrote guides/index.html")

    print("wrote guides/beginners-guide-to-ai-agents/index.html")
    print("wrote guides/intermediate-guide-to-ai-agents/index.html")
    print("wrote guides/advanced-guide-to-ai-agents/index.html")


if __name__ == "__main__":
    main()
