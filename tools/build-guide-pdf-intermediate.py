#!/usr/bin/env python3
"""Build the designed, plugmyagent-branded PDF for the AI agents intermediate guide.

Purpose-built paged layout via WeasyPrint (not a web print stylesheet):
cover page, section pages, running footers with page numbers.
The design system lives in guide_pdf_kit.py and is shared by the whole guide series.

Usage: python3 tools/build-guide-pdf-intermediate.py
Output: build/guides/intermediate-guide-to-ai-agents/ai-agents-intermediate-guide.pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_pdf_kit import cover_html, render_guide_pdf

here = os.path.dirname(os.path.abspath(__file__))
build_root = os.path.dirname(here)
out_dir = os.path.join(build_root, "guides", "intermediate-guide-to-ai-agents")
os.makedirs(out_dir, exist_ok=True)

COVER = cover_html(
    kicker="FROM TASKS TO SYSTEMS",
    title_html='An intermediate guide<br/>to <span class="neon">AI agents.</span>',
    lede_html="You know how to hand your agent a task. Now learn to build systems that run without you: memory that matters, connected tools, schedules that stick, and projects that manage themselves.",
    guide_tag="GUIDES // PILLAR 04 // GUIDE 002",
    ghost_no="02",
)

html_body = COVER + """
<section class="page">
  <div class="sec-head">
    <div class="num">01</div>
    <h2>The level-up: stop assigning tasks, start building systems</h2>
  </div>
  <p>The beginner move is handing over one task with a finish line. The intermediate move is setting up a workflow that runs without you asking each time.</p>
  <p>The shift is small, but everything changes with it: from &ldquo;do this&rdquo; to &ldquo;handle this, ongoing.&rdquo; A task ends. A system keeps working. Your agent can do both, but systems are where the real leverage lives.</p>
  <div class="moves">
    <div class="move bad"><span class="lab">The beginner version</span><p>&ldquo;Check this price now.&rdquo;</p></div>
    <div class="move good"><span class="lab">The intermediate version</span><p>&ldquo;Watch this price every day and tell me the moment it drops below $400.&rdquo; You asked once. It works forever.</p></div>
  </div>
  <div class="pull">
    <span class="k">The big idea</span>
    <p>Tasks save you minutes. Systems save you hours. This guide is about systems.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">02</div>
    <h2>Teach it how you work: memory that matters</h2>
    <p class="sub">Tell it the durable stuff once, and stop repeating yourself.</p>
  </div>
  <p>Your agent remembers context across conversations. The intermediate skill is feeding it the things that do not change: how you like your emails (short, no fluff), your budget rules, your projects, the names and details it keeps needing.</p>
  <p>When it gets something wrong about you, correct it the way you would a person: &ldquo;from now on, always use my work email for drafts.&rdquo; Say it once. It sticks.</p>
  <div class="shield">
    <span class="k">Two rules for memory</span>
    <p><strong>One:</strong> preferences and context go in memory.</p>
    <p><strong>Two:</strong> secrets never do. Passwords and keys go in the secure vault, never in the chat.</p>
  </div>
  <div class="tip">
    <span class="k">Memory tip</span>
    <p>Every few weeks, ask it &ldquo;what do you remember about me and how I like to work?&rdquo; Delete what is stale. Memory is a garden, not a hard drive.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">03</div>
    <h2>Connect your world: inbox, calendar, files</h2>
    <p class="sub">An agent with no connections is a brilliant assistant locked out of your office.</p>
  </div>
  <div class="grid">
    <div class="card"><h3><span class="dot">&#9679;</span>Calendar</h3><p>It can schedule, reschedule, and warn you about conflicts before you walk into them.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Inbox</h3><p>It can triage, draft replies, and surface only the messages that need your decision.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Files</h3><p>It can organize, summarize, and pull the right document the moment you need it.</p></div>
  </div>
  <p style="margin-top: 18px;">You grant access once. After that, the approval habit in section 06 decides what it does on its own and what it brings to you first.</p>
  <div class="pull">
    <span class="k">The trust ladder</span>
    <p>Start with read access everywhere. Let it look before it touches. Expand to write access once it proves it handles the small stuff. Read is cheap. Write is earned.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">04</div>
    <h2>Put it on a schedule: briefings, checks, watches</h2>
    <p class="sub">Three patterns cover almost every recurring need.</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>The briefing.</strong> A digest on your schedule. &ldquo;Every weekday at 7:30am, send me a 5-bullet briefing: the top news in my industry, my calendar for the day, and anything on my watch list that moved.&rdquo;</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>The check.</strong> A sweep that stays quiet unless something real happens. &ldquo;Every morning, check my inbox. Draft replies to anything routine. Only ping me about the ones that need my decision.&rdquo;</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>The watch.</strong> A standing alert with a trigger. &ldquo;Watch flights to Denver for October. Tell me the moment a round trip drops under $250.&rdquo;</p></div></div>
  <div class="tip">
    <span class="k">The rule for all three</span>
    <p>Define the trigger, the quiet hours, and what &ldquo;tell me&rdquo; means. Vague schedules create noise. Precise schedules create leverage.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">05</div>
    <h2>Run long projects without losing the plot</h2>
  </div>
  <p>Big work dies in long, shapeless conversations. The intermediate move is milestones plus checkpoints.</p>
  <p>Before it starts, ask for the plan: &ldquo;Break this into milestones and show me the plan before you do anything.&rdquo; Approve the plan, then let it run. Then add one rule: &ldquo;Report back after each milestone with what is done and what is next. Do not wait until the end.&rdquo;</p>
  <p>Keep one conversation per project. Everything it learns stays in one place, and you can scroll up any time to see how a decision was made.</p>
  <div class="tip">
    <span class="k">When a project stalls</span>
    <p>Do not restart from zero. Say &ldquo;pick up where we left off: the last finished milestone was X, continue from Y.&rdquo; Context is the asset. Protect it.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">06</div>
    <h2>The approval habit: what to auto-allow vs always check</h2>
  </div>
  <p>You do not want to approve everything. You also do not want to approve nothing. Set the line once, in plain words.</p>
  <div class="moves">
    <div class="move good"><span class="lab">Green list: auto-allow</span><p>Research, drafts, organizing files, summaries, reminders, price checks. Anything reversible and private.</p></div>
    <div class="move bad"><span class="lab">Red list: always check</span><p>Spending money, sending or posting anything, touching accounts, changing settings, deleting anything. Anything hard to undo.</p></div>
  </div>
  <p style="margin-top: 16px;">Tell your agent: &ldquo;Draft anything, send nothing. Research anything, buy nothing. If it is hard to undo, ask me first.&rdquo;</p>
  <div class="pull">
    <span class="k">The principle</span>
    <p>When in doubt, it asks. That is the deal that makes everything else safe.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">07</div>
    <h2>When it goes wrong: the 3-minute fix</h2>
    <p class="sub">It will misunderstand you sometimes. The fix is almost always fast.</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Point at the exact problem.</strong> Not &ldquo;this is wrong&rdquo; but &ldquo;the dates are wrong, use October 16 to 18, not September.&rdquo; Specific corrections teach. Vague ones do not.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>Give the correction once, then move on.</strong> &ldquo;From now on, prices in USD.&rdquo; Done. Do not re-explain every time.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>If the output is vague, ask for shape.</strong> &ldquo;Give me the top 3 with prices and links, not a paragraph.&rdquo; Agents default to prose. Tell it the format you want.</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>If it assumed wrong, add the constraint it missed.</strong> Most bad output is a missing constraint, not a bad agent. &ldquo;You assumed business travel. This is a family trip with two kids.&rdquo; Then let it redo.</p></div></div>
  <div class="tip">
    <span class="k">Do not restart from zero</span>
    <p>A correction inside the same conversation keeps everything it already got right.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">08</div>
    <h2>Five intermediate plays</h2>
    <p class="sub">Copy, paste, customize. Each one is a system, not a task.</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>The Monday briefing.</strong> &ldquo;Every Monday at 8am, send me: the 3 biggest stories in [my field], any price drops on my watch list, and conflicts in my calendar this week.&rdquo;</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>The inbox triage.</strong> &ldquo;Every weekday at 9am, scan my inbox. Draft replies to anything routine. Flag the 3 messages that need my decision, with a one-line summary of each. Send nothing.&rdquo;</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>The project tracker.</strong> &ldquo;Track my [project name] project. Every Friday, ask me for a status update, then reply with: what is done, what is stuck, and what is next.&rdquo;</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>The deal watch.</strong> &ldquo;Watch [product, flight, hotel]. Alert me the moment the price drops below [number] or a clearly better option appears. Include the link.&rdquo;</p></div></div>
  <div class="step"><div class="sn">5</div><div class="st"><p><strong>The content multiplier.</strong> &ldquo;Take my [notes / voice memo / rough draft] and turn it into three things: a social post, a short email, and a one-pager. Keep my voice, cut the fluff.&rdquo;</p></div></div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">09</div>
    <h2>What&rsquo;s next</h2>
  </div>
  <div class="tip">
    <span class="k">Pass it on</span>
    <p>Know someone still stuck on chatbots? Send them the beginner guide first. New to Muse? Enter the code <code>DGC4EX</code> in Settings within 48 hours of joining: you get 1 billion tokens, and so does the person who invited you.</p>
  </div>
  <div class="closer">
    <span class="k">Keep going</span>
    <h2>This is guide 002.</h2>
    <p>The advanced guide is next: chaining agents together, building custom workflows, connecting your own tools and data, and running your agent like a small ops team.</p>
    <p>The free API catalog, the MCP server directory, and the component library are live now.</p>
    <div class="brand">PLUGMYAGENT.COM &nbsp;//&nbsp; &copy; 2026 HIDDENINWEST</div>
  </div>
</section>
"""

out_pdf = os.path.join(out_dir, "ai-agents-intermediate-guide.pdf")
render_guide_pdf(
    "An Intermediate Guide to AI Agents: From Tasks to Systems",
    html_body,
    out_pdf,
)
