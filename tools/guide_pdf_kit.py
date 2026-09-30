#!/usr/bin/env python3
"""Shared design kit for the PlugMyAgent guides PDF series.

One design system for every guide in the series (beginner, intermediate,
advanced): the same cover, section pages, running footers, and brand
colors. Per-guide scripts supply only the content.

iOS-SAFE RULES (2026-09-23): flow layout only, solid colors only, zero
opacity, zero absolute positioning. iOS's PDF renderer drops transparency
and absolutely-positioned full-page layers. Full-bleed pages need the
background set explicitly on @page (body background does not paint the
@page margin areas).
"""
import base64
import os

_here = os.path.dirname(os.path.abspath(__file__))

_logo_path = os.path.join(_here, "..", "plug-lockup-v2.png")
with open(_logo_path, "rb") as f:
    LOGO = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

CSS = """
@page {
  size: Letter;
  margin: 0.72in 0.78in 0.95in 0.78in;
  background: #0b0d0d;
  @bottom-center {
    content: "";
    border-top: 2px solid #ff6b1a;
    width: 100%;
    margin: 0 0.78in;
    padding-top: 8px;
  }
  @bottom-left {
    content: "plugmyagent.com";
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 7.5pt;
    letter-spacing: 0.04em;
    color: #6f7570;
    margin-left: 0.78in;
    padding-top: 12px;
    white-space: nowrap;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 7.5pt;
    letter-spacing: 0.08em;
    color: #6f7570;
    margin-right: 0.78in;
    padding-top: 12px;
    white-space: nowrap;
  }
}
@page cover { margin: 0;
  @bottom-center { content: none; }
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Inter", "DejaVu Sans", sans-serif;
  font-size: 10.8pt;
  line-height: 1.62;
  color: #f2f4f2;
  background: #0b0d0d;
}
.cover {
  page: cover;
  width: 8.5in;
  height: 11in;
  background: linear-gradient(160deg, #121110 0%, #0b0d0d 45%, #0b0d0d 100%);
}
.cover-main { height: 8.3in; padding: 0.72in 0.85in 0; }
.cover .topbar { display: flex; justify-content: space-between; align-items: center; }
.cover .topbar img { height: 34px; }
.cover .topbar .tag { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.18em; color: #6f7570; }
.cover .kicker { font-family: "DejaVu Sans Mono", monospace; font-size: 10pt;
  letter-spacing: 0.30em; color: #ff6b1a; margin-top: 1.4in; }
.cover h1 { font-size: 56pt; line-height: 1.04; letter-spacing: -0.02em;
  margin: 18px 0 0; font-weight: 800; }
.cover h1 .neon { color: #ff6b1a; }
.cover .rule { width: 1.5in; border-top: 4px solid #ff6b1a; margin: 30px 0 26px; }
.cover .lede { font-size: 13pt; line-height: 1.6; color: #a7ada8; max-width: 5.9in; margin: 0; }
.cover-ghost { height: 1.5in; margin: -0.5in 0 0; padding-right: 0.4in;
  font-size: 170pt; font-weight: 800; line-height: 1; letter-spacing: -0.05em;
  color: #1d1710; text-align: right; }
.cover-foot { height: 0.7in; margin: 0 0.85in; border-top: 2px solid #232826;
  padding-top: 12px; display: flex; justify-content: space-between;
  font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.10em; color: #6f7570; }
section.page { break-before: page; }
.sec-head { margin: 0 0 20px; }
.sec-head .num { font-family: "DejaVu Sans Mono", monospace; font-size: 10pt;
  letter-spacing: 0.28em; color: #ff6b1a; }
.sec-head h2 { font-size: 25pt; line-height: 1.16; letter-spacing: -0.015em;
  margin: 10px 0 0; font-weight: 800; }
.sec-head .sub { color: #a7ada8; font-size: 11pt; margin: 10px 0 0; max-width: 6.2in; }
.pull { border-left: 5px solid #ff6b1a; background: #111413;
  border-top: 1px solid #232826; border-right: 1px solid #232826; border-bottom: 1px solid #232826;
  border-radius: 0 12px 12px 0; padding: 20px 24px; margin: 26px 0; }
.pull .k { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.22em; color: #ff6b1a; display: block; margin-bottom: 8px; }
.pull p { font-size: 16pt; line-height: 1.4; font-weight: 700; margin: 0; letter-spacing: -0.01em; }
table.cmp { width: 100%; border-collapse: collapse; margin: 8px 0 0; font-size: 10pt; }
table.cmp th { background: #ff6b1a; color: #0b0d0d; text-align: left;
  font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; letter-spacing: 0.14em;
  padding: 10px 14px; }
table.cmp th:first-child { border-radius: 10px 0 0 0; }
table.cmp th:last-child { border-radius: 0 10px 0 0; }
table.cmp td { border: 1px solid #232826; padding: 12px 14px; vertical-align: top; color: #cfd4cf; }
table.cmp tr:last-child td:first-child { border-radius: 0 0 0 10px; }
table.cmp tr:last-child td:last-child { border-radius: 0 0 10px 0; }
table.cmp td.rowh { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.12em; color: #ff6b1a; background: #111413; width: 1.9in; }
p { margin: 0 0 12px; }
p strong, li strong { color: #ffffff; }
.ex { margin: 0 0 18px; }
.ex h3 { font-size: 13pt; margin: 0 0 10px; font-weight: 700; }
.ex h3 .n { color: #ff6b1a; font-family: "DejaVu Sans Mono", monospace; font-size: 10pt; margin-right: 8px; }
.moves { display: flex; gap: 12px; }
.move { flex: 1; background: #111413; border: 1px solid #232826; border-radius: 10px;
  padding: 12px 14px; border-top: 3px solid #232826; }
.move.bad { border-top-color: #ff8a5c; }
.move.good { border-top-color: #4ade80; }
.move .lab { font-family: "DejaVu Sans Mono", monospace; font-size: 7.5pt;
  letter-spacing: 0.20em; display: block; margin-bottom: 6px; }
.move.bad .lab { color: #ff8a5c; }
.move.good .lab { color: #4ade80; }
.move p { margin: 0; font-size: 10pt; line-height: 1.55; color: #dfe3df; }
.grid { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 6px; }
.card { width: 48.7%; background: #111413; border: 1px solid #232826; border-radius: 12px;
  padding: 20px 18px 18px; }
.card h3 { font-size: 12pt; margin: 0 0 8px; font-weight: 700; }
.card h3 .dot { color: #ff6b1a; margin-right: 6px; }
.card p { margin: 0; font-size: 10pt; color: #a7ada8; line-height: 1.6; }
.step { display: flex; gap: 16px; margin: 0 0 16px; align-items: flex-start; }
.step .sn { flex: 0 0 44px; width: 44px; height: 44px; border-radius: 50%;
  background: #ff6b1a; color: #0b0d0d; font-weight: 800; font-size: 15pt;
  text-align: center; line-height: 44px; }
.step .st { padding-top: 2px; }
.step .st p { margin: 0; }
.tip { border: 1.5px solid #ff6b1a; border-radius: 12px; padding: 16px 18px; margin: 22px 0 0;
  background: #161310; }
.tip .k { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.22em; color: #ff6b1a; display: block; margin-bottom: 8px; }
.tip p { margin: 0; font-size: 10.5pt; }
.tip code { font-family: "DejaVu Sans Mono", monospace; font-size: 11pt; color: #ff6b1a;
  background: #0b0d0d; border: 1px solid #232826; border-radius: 6px; padding: 2px 8px; }
.shield { background: #111413; border: 1px solid #232826; border-left: 5px solid #4ade80;
  border-radius: 0 12px 12px 0; padding: 18px 22px; margin: 6px 0 26px; }
.shield .k { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.22em; color: #4ade80; display: block; margin-bottom: 8px; }
.shield p { margin: 0 0 10px; font-size: 10.5pt; }
.shield p:last-child { margin-bottom: 0; }
.closer { margin-top: 30px; border: 1.5px solid #232826; border-radius: 14px; padding: 26px 28px;
  background: #111413; text-align: center; }
.closer .k { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  letter-spacing: 0.26em; color: #ff6b1a; display: block; margin-bottom: 10px; }
.closer h2 { font-size: 21pt; margin: 0 0 10px; letter-spacing: -0.01em; }
.closer p { color: #a7ada8; font-size: 10.5pt; margin: 0 0 6px; }
.closer .brand { margin-top: 16px; padding-top: 14px; border-top: 1px solid #232826;
  font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; letter-spacing: 0.12em; color: #6f7570; }
"""


def cover_html(kicker, title_html, lede_html, guide_tag, ghost_no,
               date="SEPTEMBER 2026"):
    """The series cover. title_html may contain <br/> and span.neon."""
    return (
        '<div class="cover">\n'
        '  <div class="cover-main">\n'
        '    <div class="topbar">\n'
        f'      <img src="{LOGO}" alt="PlugMyAgent" />\n'
        f'      <div class="tag">{guide_tag}</div>\n'
        '    </div>\n'
        f'    <div class="kicker">{kicker}</div>\n'
        f'    <h1>{title_html}</h1>\n'
        '    <div class="rule"></div>\n'
        f'    <p class="lede">{lede_html}</p>\n'
        '  </div>\n'
        f'  <div class="cover-ghost">{ghost_no}</div>\n'
        f'  <div class="cover-foot"><span>PLUGMYAGENT.COM</span><span>{date}</span></div>\n'
        '</div>\n'
    )


def render_guide_pdf(title, html_body, out_path):
    """Assemble the document and write the PDF. Guards against em dashes."""
    body_html = html_body.replace("__LOGO__", LOGO)
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n"
        "<title>" + title + "</title>\n"
        "<style>" + CSS + "</style>\n</head>\n<body>\n" + body_html + "\n</body>\n</html>\n"
    )
    if "\u2014" in doc:
        raise SystemExit("em dash found in PDF source")
    from weasyprint import HTML
    HTML(string=doc, base_url=os.path.dirname(out_path)).write_pdf(out_path)
    print("wrote", out_path)
