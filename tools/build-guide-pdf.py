#!/usr/bin/env python3
"""Build the designed, plugmyagent-branded PDF for the AI agents beginner's guide.

Purpose-built paged layout via WeasyPrint (not a web print stylesheet):
cover page, section pages, running footers with page numbers.
The design system lives in guide_pdf_kit.py and is shared by the whole guide series.

Usage: python3 tools/build-guide-pdf.py
Output: build/guides/beginners-guide-to-ai-agents/ai-agents-beginners-guide.pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_pdf_kit import render_guide_pdf

here = os.path.dirname(os.path.abspath(__file__))
build_root = os.path.dirname(here)
out_dir = os.path.join(build_root, "guides", "beginners-guide-to-ai-agents")
os.makedirs(out_dir, exist_ok=True)

html_body = """
<div class="cover">
  <div class="cover-main">
    <div class="topbar">
      <img src="__LOGO__" alt="PlugMyAgent" />
      <div class="tag">GUIDES // PILLAR 04 // GUIDE 001</div>
    </div>
    <div class="kicker">FROM CHATBOT TO COWORKER</div>
    <h1>A beginner&rsquo;s guide<br/>to <span class="neon">AI agents.</span></h1>
    <div class="rule"></div>
    <p class="lede">If you have only ever chatted with AI, you are using about ten percent of what it can do. This guide shows how a personal AI agent turns &ldquo;ask me anything&rdquo; into &ldquo;consider it done.&rdquo; No jargon, no setup required to understand it.</p>
  </div>
  <div class="cover-ghost">01</div>
  <div class="cover-foot"><span>PLUGMYAGENT.COM</span><span>SEPTEMBER 2026</span></div>
</div>

<section class="page">
  <div class="sec-head">
    <div class="num">01</div>
    <h2>The one idea: a chatbot answers, an agent acts</h2>
  </div>
  <p>You already know the chatbot move. You type a question, it types an answer, and the conversation ends. An AI agent works differently. You hand it an outcome, and it does the work to get there: it plans the steps, uses tools, checks sources, builds things, and reports back when it is done.</p>
  <div class="pull">
    <span class="k">The shift in one sentence</span>
    <p>Stop asking for answers. Start handing over outcomes.</p>
  </div>
  <table class="cmp">
    <tr><th></th><th>Chatbot</th><th>AI agent</th></tr>
    <tr><td class="rowh">You ask for</td><td>An answer</td><td>An outcome</td></tr>
    <tr><td class="rowh">It does</td><td>Writes a reply</td><td>Runs the errands, checks the sources, builds the thing</td></tr>
    <tr><td class="rowh">After you close the app</td><td>Nothing</td><td>Keeps working and reports back</td></tr>
    <tr><td class="rowh">Best for</td><td>Quick questions</td><td>Real tasks with real deliverables</td></tr>
  </table>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">02</div>
    <h2>Meet your AI agent</h2>
    <p class="sub">What it is, where it lives, and why it beats starting fresh every time.</p>
  </div>
  <p>A personal AI agent is your own dedicated assistant with its own computer that keeps working between conversations. It remembers your context, keeps going in the background, and every conversation is one to one: just you and your agent. Examples include Muse (Meta&rsquo;s personal AI agent) and OpenClaw. This guide uses Muse as the running example, but the playbook works for any of them.</p>
  <p>You reach Muse on the web at <strong>muse.ai</strong>, in the <strong>iOS and Android apps</strong>, or over <strong>WhatsApp</strong>. It is available in the US and Canada.</p>
  <p>Think of it this way:</p>
  <div class="moves">
    <div class="move bad"><span class="lab">A chatbot is</span><p>A very smart stranger you meet fresh every time.</p></div>
    <div class="move good"><span class="lab">An agent is</span><p>A sharp assistant who already knows how you work.</p></div>
  </div>
  <div class="tip">
    <span class="k">Referral tip</span>
    <p>New to Muse? Enter the code <code>DGC4EX</code> in Settings within 48 hours of joining. You will get 1 billion tokens, and so will the person who invited you.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">03</div>
    <h2>See the difference: four before-and-after swaps</h2>
    <p class="sub">The fastest way to feel the shift is to watch a chatbot request become an agent request.</p>
  </div>
  <div class="ex">
    <h3><span class="n">A</span>The hotel hunt</h3>
    <div class="moves">
      <div class="move bad"><span class="lab">Chatbot move</span><p>&ldquo;What are some good hotels in Vegas?&rdquo;</p></div>
      <div class="move good"><span class="lab">Agent move</span><p>&ldquo;Find the best Sunday-night hotel deal near the Strip for September 27, under $120, with free parking. Keep watching prices and tell me if something better shows up before Friday.&rdquo;</p></div>
    </div>
  </div>
  <div class="ex">
    <h3><span class="n">B</span>The resume</h3>
    <div class="moves">
      <div class="move bad"><span class="lab">Chatbot move</span><p>&ldquo;Write me a resume summary.&rdquo;</p></div>
      <div class="move good"><span class="lab">Agent move</span><p>&ldquo;Here is my work history. Build me a one-page resume tailored for office manager roles, and save it as both a PDF and a Word file.&rdquo;</p></div>
    </div>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">03</div>
    <h2>Before-and-after, continued</h2>
  </div>
  <div class="ex">
    <h3><span class="n">C</span>The side hustle</h3>
    <div class="moves">
      <div class="move bad"><span class="lab">Chatbot move</span><p>&ldquo;How do I start a side business?&rdquo;</p></div>
      <div class="move good"><span class="lab">Agent move</span><p>&ldquo;Research three side business ideas I can start with zero dollars and my background in customer service and design. Rank them by realistic first-month income and turn the winner into a one-page plan.&rdquo;</p></div>
    </div>
  </div>
  <div class="ex">
    <h3><span class="n">D</span>The reminder that actually works</h3>
    <div class="moves">
      <div class="move bad"><span class="lab">Chatbot move</span><p>&ldquo;Remind me to call the dentist.&rdquo;</p></div>
      <div class="move good"><span class="lab">Agent move</span><p>&ldquo;Remind me to call the dentist Tuesday at 9am. If I have not confirmed by 10, nudge me again.&rdquo;</p></div>
    </div>
  </div>
  <div class="pull">
    <span class="k">The pattern</span>
    <p>The chatbot version asks a question. The agent version hands over a job with a finish line.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">04</div>
    <h2>What you can hand it today</h2>
    <p class="sub">Six kinds of work where the agent version beats the chatbot version every time.</p>
  </div>
  <div class="grid">
    <div class="card"><h3><span class="dot">&#9679;</span>Research and comparisons</h3><p>Deep dives with sources, price comparisons, best-of lists ranked by what actually matters to you.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Documents and decks</h3><p>Reports, spreadsheets, presentations, resumes, one-pagers. It writes them and hands you the file.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Build simple things</h3><p>Web pages, landing pages, small tools and prototypes you can open and use, not just read about.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Watch things for you</h3><p>Prices, inboxes, listings, schedules. It checks on a schedule and only pings you when something real happens.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Keep you on track</h3><p>Goals, trips, projects, reminders, morning briefings. It carries the plan so you do not have to.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Draft your words</h3><p>Emails, messages, posts, replies. It drafts everything and nothing goes out without your say-so.</p></div>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">05</div>
    <h2>How to prompt it well: the delegation recipe</h2>
    <p class="sub">Good agent prompts read like a good work assignment. Four ingredients:</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>The outcome.</strong> What does &ldquo;done&rdquo; look like? Name the deliverable.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>The context.</strong> Dates, budget, links, background. The stuff it cannot guess.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>The constraints.</strong> Budget, tone, length, what to avoid.</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>The check.</strong> For anything outward-facing, say &ldquo;show me before you send anything.&rdquo;</p></div></div>
  <div class="moves" style="margin-top: 22px;">
    <div class="move bad"><span class="lab">Vague</span><p>&ldquo;Plan my trip.&rdquo;</p></div>
    <div class="move good"><span class="lab">Delegated</span><p>&ldquo;Plan a 3-day weekend trip to San Diego, October 16 to 18, $600 total budget for two people. We like food and beaches and hate crowds. Give me a day-by-day plan with prices and links, and flag anything that needs booking ahead.&rdquo;</p></div>
  </div>
  <p style="margin-top: 16px; color: #a7ada8;">Notice the second one does not just ask a question. It hands over a job with a finish line.</p>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">06</div>
    <h2>Staying in control: the approval card</h2>
  </div>
  <div class="shield">
    <span class="k">How it keeps you in charge</span>
    <p>Handing work to an agent does not mean handing over your judgment. When something needs your decision, you get an approval card that says exactly what it wants to do. Nothing moves until you say yes.</p>
    <p>It will check with you before it spends money, sends a message, posts anything publicly, touches your accounts, or does anything hard to undo. Logins and keys go into a secure vault, never into the chat. You stay the decider. It stays the doer.</p>
  </div>
  <div class="sec-head" style="margin-top: 30px;">
    <div class="num">07</div>
    <h2>Your first week: five copy-paste starters</h2>
    <p class="sub">Do not start with &ldquo;what can you do.&rdquo; Start with one of these.</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Research something you are actually buying.</strong> &ldquo;Research the 5 best noise-canceling headphones under $200 and rank them by comfort for long calls. Include prices and links.&rdquo;</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>Turn messy notes into a clean doc.</strong> &ldquo;Turn these notes into a clean one-page summary: [paste your notes].&rdquo;</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>Set a daily briefing.</strong> &ldquo;Every morning, check the news on [your topic] and send me a 3-bullet briefing.&rdquo;</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>Draft, do not send.</strong> &ldquo;Draft an email to my landlord about the leaky faucet. Keep it short and polite. Do not send it.&rdquo;</p></div></div>
  <div class="step"><div class="sn">5</div><div class="st"><p><strong>Build something small.</strong> &ldquo;Build me a simple one-page site for my side project. Keep it clean and mobile-friendly.&rdquo;</p></div></div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">08</div>
    <h2>Getting started in three steps</h2>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Pick an agent and get the app.</strong> Start with Muse: open <strong>muse.ai</strong> on the web, or grab the iOS or Android app. If you live in the US or Canada, you are in. Tip: enter referral code <strong>DGC4EX</strong> in Settings within 48 hours of joining and you will both get 1 billion tokens. Other agents work the same way from here.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>Start with one real task</strong> from the list above, not a test question. Real stakes teach you the workflow faster.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>Manage it like a person.</strong> Give feedback the way you would to an assistant: &ldquo;good, but shorter&rdquo; or &ldquo;redo this with the new dates.&rdquo; It learns how you like things.</p></div></div>
  <div class="closer">
    <span class="k">Keep going</span>
    <h2>This is guide 001.</h2>
    <p>More PlugMyAgent guides are on the way. The free API catalog, the MCP server directory, and the component library are live now.</p>
    <div class="brand">PLUGMYAGENT.COM &nbsp;//&nbsp; &copy; 2026 HIDDENINWEST</div>
  </div>
</section>
"""

out_pdf = os.path.join(out_dir, "ai-agents-beginners-guide.pdf")
render_guide_pdf(
    "A Beginner's Guide to AI Agents: From Chatbot to Coworker",
    html_body,
    out_pdf,
)
