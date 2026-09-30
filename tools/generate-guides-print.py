#!/usr/bin/env python3
"""Build a plugmyagent-branded, print-optimized HTML of the AI agents beginner's
guide, for PDF export.

Usage: python3 tools/generate-guides-print.py /tmp/guides-print
"""
import base64
import importlib.util
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
_gen_path = os.path.join(here, "generate-guides.py")
_spec = importlib.util.spec_from_file_location("generate_guides", _gen_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
GUIDE_BODY = _mod.GUIDE_BODY

out_dir = "/tmp/guides-print"
os.makedirs(out_dir, exist_ok=True)

# Brand lockup as a data URI so the file:// render picks it up.
logo_path = os.path.join(here, "..", "plug-lockup-v2.png")
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("ascii")

body = GUIDE_BODY
# Strip the hero CTAs (buttons are meaningless on paper)
body = re.sub(r'<div class="hero-cta">.*?</div>', '', body, flags=re.S)
# Drop the "take this guide with you" download box: self-referential inside the PDF
body = re.sub(r'<div class="dlbox">.*?</div>', '', body, flags=re.S)
# De-orphan the Muse availability paragraph (its antecedent sits on the prior page)
body = body.replace(
    "You reach it on the web at muse.ai",
    "You reach Muse on the web at muse.ai",
)
# Eric's personal Muse referral code, PDF only
body = body.replace(
    "If you live in the US or Canada, you are in. Other agents work the same way from here.</li>",
    "If you live in the US or Canada, you are in. Tip: enter referral code "
    "<strong>DGC4EX</strong> in Settings within 48 hours of joining and you will "
    "both get 1 billion tokens. Other agents work the same way from here.</li>",
)
# Branded masthead
masthead = (
    '<div class="masthead">\n'
    f'  <img class="brandlogo" src="data:image/png;base64,{logo_b64}" alt="PlugMyAgent" />\n'
    '  <div class="tagline">Guides // Pillar 04 // Guide 001</div>\n'
    "</div>\n"
)
body = body.replace("<main>", "<main>" + masthead, 1)

css = """
  @page { size: Letter; margin: 0; }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family: "Inter", -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         font-size: 11pt; line-height: 1.62; color: #e9edea; background: #0b0d0d;
         margin: 0; padding: 0.7in 0.75in; }
  main { max-width: 100%; }
  .masthead { border-bottom: 3px solid #ff6b1a; padding-bottom: 12px; margin-bottom: 4px;
              display: flex; align-items: center; justify-content: space-between; }
  .masthead .brandlogo { height: 30px; }
  .masthead .tagline { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 8.5pt;
                       letter-spacing: .16em; text-transform: uppercase; color: #8b918c; }
  .hero { padding: 26px 0 8px; }
  .eyebrow { display: none; }
  h1 { font-size: 27pt; line-height: 1.14; letter-spacing: -0.015em; margin: 0 0 14px; color: #f4f6f4; }
  h1 .neon { color: #ff6b1a; }
  .lede { font-size: 12.5pt; color: #b9beb9; max-width: 100%; }
  h2 { font-size: 16pt; margin: 32px 0 10px; page-break-after: avoid; break-after: avoid; color: #f4f6f4; }
  h2 .secnum { color: #ff6b1a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
               font-size: 10pt; margin-right: 10px; }
  h3 { font-size: 12.5pt; margin: 20px 0 8px; page-break-after: avoid; break-after: avoid; color: #f4f6f4; }
  p, li { orphans: 3; widows: 3; }
  strong { color: #f4f6f4; }
  .big-idea { border: 1px solid #232826; border-left: 4px solid #ff6b1a; background: #101313;
              border-radius: 10px; padding: 14px 16px; margin: 18px 0;
              page-break-inside: avoid; break-inside: avoid; }
  .big-idea .kicker { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 8pt;
                      letter-spacing: .18em; text-transform: uppercase; color: #ff6b1a;
                      display: block; margin-bottom: 6px; }
  .big-idea p { margin: 0; color: #e9edea; }
  table.compare { width: 100%; border-collapse: collapse; margin: 16px 0 20px; font-size: 10pt;
                  page-break-inside: avoid; break-inside: avoid; }
  table.compare th, table.compare td { text-align: left; padding: 9px 11px; border: 1px solid #232826;
                                       vertical-align: top; }
  table.compare th { background: #151918; color: #ff6b1a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
                     font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; }
  table.compare td { color: #cfd4cf; }
  .promptbox { background: #101313; border: 1px solid #232826; border-left: 4px solid #ff6b1a;
               border-radius: 10px; padding: 12px 14px; margin: 12px 0 16px;
               page-break-inside: avoid; break-inside: avoid; }
  .promptbox .plabel { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 8pt;
                       letter-spacing: .16em; text-transform: uppercase; color: #8b918c;
                       display: block; margin-bottom: 6px; }
  .promptbox .plabel.bad { color: #ff8a5c; }
  .promptbox .plabel.good { color: #4ade80; }
  .promptbox p { margin: 0; color: #e9edea; }
  .cards { margin: 16px 0 20px; }
  .gcard { border: 1px solid #232826; background: #101313; border-radius: 10px; padding: 12px 14px;
           margin-bottom: 10px; page-break-inside: avoid; break-inside: avoid; }
  .gcard h3 { margin: 0 0 4px; font-size: 11.5pt; color: #f4f6f4; }
  .gcard h3 .ico { color: #ff6b1a; }
  .gcard p { margin: 0; font-size: 10.5pt; color: #b9beb9; }
  .checklist { list-style: none; padding: 0; margin: 14px 0 20px; }
  .checklist li { border: 1px solid #232826; background: #101313; border-radius: 10px;
                  padding: 10px 12px 10px 46px; position: relative; margin-bottom: 8px;
                  page-break-inside: avoid; break-inside: avoid; color: #cfd4cf; }
  .checklist li::before { content: attr(data-n); position: absolute; left: 12px; top: 9px; width: 23px;
                          height: 23px; border-radius: 50%; background: #ff6b1a; color: #0b0d0d;
                          font-weight: 800; font-size: 10.5pt; display: flex; align-items: center;
                          justify-content: center; }
  .pdffooter { margin-top: 36px; border-top: 3px solid #ff6b1a; padding-top: 10px; font-size: 9pt;
               color: #8b918c; display: flex; justify-content: space-between;
               font-family: ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .06em;
               page-break-inside: avoid; break-inside: avoid; }
"""

html = (
    "<!doctype html>\n"
    '<html lang="en">\n'
    "<head>\n"
    '<meta charset="utf-8" />\n'
    "<title>A Beginner's Guide to AI Agents: From Chatbot to Coworker</title>\n"
    "<style>" + css + "</style>\n"
    "</head>\n"
    "<body>\n" + body + "\n"
    '<div class="pdffooter"><span>plugmyagent.com/guides/beginners-guide-to-ai-agents</span>'
    "<span>&copy; 2026 hiddeninwest</span></div>\n"
    "</body>\n"
    "</html>\n"
)

if "\u2014" in html:
    raise SystemExit("em dash found in print HTML")
if "dlbox" in body:
    raise SystemExit("dlbox not stripped from print HTML")

out = os.path.join(out_dir, "beginners-guide.html")
with open(out, "w") as f:
    f.write(html)
print("wrote", out)
