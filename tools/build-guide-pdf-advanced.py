#!/usr/bin/env python3
"""Build the designed, plugmyagent-branded PDF for the AI agents advanced guide.

Purpose-built paged layout via WeasyPrint (not a web print stylesheet):
cover page, section pages, running footers with page numbers.
The design system lives in guide_pdf_kit.py and is shared by the whole guide series.

Usage: python3 tools/build-guide-pdf-advanced.py
Output: build/guides/advanced-guide-to-ai-agents/ai-agents-advanced-guide.pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_pdf_kit import cover_html, render_guide_pdf

here = os.path.dirname(os.path.abspath(__file__))
build_root = os.path.dirname(here)
out_dir = os.path.join(build_root, "guides", "advanced-guide-to-ai-agents")
os.makedirs(out_dir, exist_ok=True)

COVER = cover_html(
    kicker="FROM SYSTEMS TO LEVERAGE",
    title_html='An advanced guide<br/>to <span class="neon">AI agents.</span>',
    lede_html="You run systems that work without you. Now compose them: chain specialist agents, build your own workflows, feed them your data, and run the whole thing like a small ops team.",
    guide_tag="GUIDES // PILLAR 04 // GUIDE 003",
    ghost_no="03",
)

html_body = COVER + """
<section class="page">
  <div class="sec-head">
    <div class="num">01</div>
    <h2>The advanced leap: from using agents to composing them</h2>
    <p class="sub">Beginner was one task. Intermediate was systems. Advanced is composition.</p>
  </div>
  <p>The beginner move was handing over one task with a finish line. The intermediate move was building systems that run without you asking each time. The advanced move is composing: chaining specialist agents together, feeding them your own data, and building workflows bigger than any single prompt.</p>
  <p>Think of it as going from playing an instrument to conducting. One agent is a talented employee. A composed team of agents, wired to your data and your tools, is a department.</p>
  <div class="moves">
    <div class="move bad"><span class="lab">One giant prompt</span><p>&ldquo;Do my market research, write the report, make the slides, and email it.&rdquo; One agent, one breath, fingers crossed.</p></div>
    <div class="move good"><span class="lab">A composed workflow</span><p>A researcher gathers. A planner organizes. A maker drafts. A checker reviews. Each one has a tight brief and hands off a finished artifact.</p></div>
  </div>
  <div class="pull">
    <span class="k">The big idea</span>
    <p>Beginners delegate tasks. Intermediates build systems. Advanced users compose teams. The leverage compounds at every level.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">02</div>
    <h2>Chain agents together: specialists beat generalists</h2>
    <p class="sub">One agent doing everything is a bottleneck. Split the work.</p>
  </div>
  <p>A single agent juggling research, analysis, writing, and review does each one worse than a specialist would. The advanced pattern is the assembly line: small agents, each with one job and a tight brief.</p>
  <p>The handoff rule makes it work: each agent passes the next one a finished artifact, not a chat log. &ldquo;Here are the 10 sources, ranked&rdquo; beats &ldquo;here is our whole conversation, good luck.&rdquo;</p>
  <div class="grid">
    <div class="card"><h3><span class="dot">&#9679;</span>The Researcher</h3><p>Gathers raw material: sources, prices, options, facts. Never judges, just collects.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>The Planner</h3><p>Turns raw material into structure: outlines, comparisons, shortlists. Never writes the final draft.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>The Maker</h3><p>Produces the artifact: the draft, the sheet, the summary. Works only from the plan, never from raw chaos.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>The Checker</h3><p>Reviews the maker&apos;s output against your rules before anything ships. Cheap insurance. Expensive to skip.</p></div>
  </div>
  <div class="tip">
    <span class="k">Start with two</span>
    <p>You do not need four agents on day one. Split your hardest workflow into researcher and maker first. Add the planner and checker once the handoffs feel natural.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">03</div>
    <h2>Build your own workflows: the recipe pattern</h2>
    <p class="sub">Name the steps, define the handoffs, set the checkpoints.</p>
  </div>
  <p>A workflow is a recipe your agents follow every time. Write it once, run it forever. Every good recipe has four parts.</p>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Name it.</strong> &ldquo;The Friday client report.&rdquo; A name turns a prompt into a thing the team can run.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>List the steps in order,</strong> with what each step produces. Gather, organize, draft, review.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>Define the handoffs:</strong> what exactly passes from one step to the next. Artifacts, not conversations.</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>Set the checkpoints:</strong> where it pauses and waits for you. Money moves, public output, and judgment calls always checkpoint.</p></div></div>
  <div class="tip">
    <span class="k">Copy-paste: turn anything into a workflow</span>
    <p>&ldquo;Turn this into a reusable workflow: [describe the outcome]. Break it into steps. For each step, tell me what it needs as input and what it produces as output. Mark the checkpoints where you must pause and wait for my approval.&rdquo;</p>
  </div>
  <div class="pull">
    <span class="k">The big idea</span>
    <p>A workflow you write once and run fifty times is fifty tasks you never delegate again.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">04</div>
    <h2>Feed it your data: APIs, docs, and knowledge bases</h2>
    <p class="sub">An agent is only as good as what it can reach.</p>
  </div>
  <p>The biggest jump in output quality comes from inputs, not prompts. Give your agents your world. Your docs: paste the manual, upload the price sheet, share the policy. Your data: the spreadsheet, the notes, the customer list. Your live tools: connected through APIs so the agent can check the real numbers instead of guessing.</p>
  <p>This is where plugmyagent earns its keep: the catalog lists 450+ free APIs your agents can call, and the MCP server directory wires tools straight into your agent with copy-paste config.</p>
  <div class="moves">
    <div class="move bad"><span class="lab">Generic answers</span><p>An agent answering from training data alone. Confident, outdated, and wrong about your prices.</p></div>
    <div class="move good"><span class="lab">Your answers</span><p>The same agent with your price sheet, your return policy, and your shipping API. Now it answers like your best rep, at 2am, instantly.</p></div>
  </div>
  <div class="shield">
    <span class="k">The data rule</span>
    <p>Never let an agent guess what it could look up. If the answer exists in your docs or your tools, connect it before you prompt.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">05</div>
    <h2>Guardrails and evals: trust, but verify</h2>
    <p class="sub">Advanced users do not hope. They check.</p>
  </div>
  <p>The more your agents do on their own, the more you need ways to catch mistakes early. Three mechanisms, all plain English.</p>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Show your work.</strong> &ldquo;Cite your sources for every claim.&rdquo; If it cannot point at the source, it does not ship.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>Spot checks.</strong> Audit a random sample every week. Five minutes, once a week, catches drift before it becomes damage.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>Golden examples.</strong> Keep 3 to 5 cases where you know the right answer cold. When you change a workflow, run it against those cases first. If it fails a golden example, it does not go live.</p></div></div>
  <div class="tip">
    <span class="k">The eval habit</span>
    <p>Before you trust a new workflow, run it on three cases where you already know the answer. New workflows earn trust. They do not start with it.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">06</div>
    <h2>Run it like an ops team</h2>
    <p class="sub">Give the team structure and it stops feeling like a toy.</p>
  </div>
  <p>At this level you are managing, not prompting. Borrow the structure real teams use.</p>
  <div class="grid">
    <div class="card"><h3><span class="dot">&#9679;</span>Roles</h3><p>Who does what: your researcher, your planner, your maker, your checker. Write it down once.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>The standup</h3><p>Your morning briefing becomes the team&apos;s roll call: what ran overnight, what needs you, what is next.</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>Escalation rules</h3><p>The advanced approval habit: &ldquo;Handle it unless money moves, a customer is involved, or you are less than 80% sure. Then bring it to me with your recommendation.&rdquo;</p></div>
    <div class="card"><h3><span class="dot">&#9679;</span>The weekly review</h3><p>Fifteen minutes every Friday: what worked, what broke, one improvement for next week. Systems that do not get reviewed quietly rot.</p></div>
  </div>
  <div class="pull">
    <span class="k">The big idea</span>
    <p>You are not using an AI anymore. You are running a small ops team that happens to be software. Manage it like one.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">07</div>
    <h2>Know the costs: tokens, limits, and picking your model</h2>
    <p class="sub">Leverage is cheap. Waste is not.</p>
  </div>
  <p>Every request costs compute, and the bill is real whether you see it or not. The advanced skill is spending it where it matters.</p>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>Big models for judgment calls.</strong> Negotiations, strategy, anything where nuance matters.</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>Small, fast models for grunt work.</strong> Sorting, summarizing, reformatting, first drafts.</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>Batch the routine.</strong> One scheduled sweep beats twenty ad-hoc questions.</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>Respect rate limits.</strong> Space out heavy jobs. Run the big ones overnight.</p></div></div>
  <div class="tip">
    <span class="k">The 80/20 rule</span>
    <p>80% of the value comes from cheap, consistent automation. Save the heavyweight model for the 20% where judgment actually matters. Most people do the reverse.</p>
  </div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">08</div>
    <h2>Four advanced plays</h2>
    <p class="sub">Copy, paste, customize. Each one composes multiple agents.</p>
  </div>
  <div class="step"><div class="sn">1</div><div class="st"><p><strong>The research swarm.</strong> &ldquo;Break [question] into 4 angles. Research each angle in parallel. Then merge everything into one brief: the consensus, the disagreements, and the 3 sources I should read myself.&rdquo;</p></div></div>
  <div class="step"><div class="sn">2</div><div class="st"><p><strong>The content pipeline.</strong> &ldquo;Take my [rough notes] and run the pipeline: planner makes the outline, maker drafts all three formats [post, email, one-pager], checker enforces my voice rules [short, no fluff, no hype]. Show me only the final drafts.&rdquo;</p></div></div>
  <div class="step"><div class="sn">3</div><div class="st"><p><strong>The data watchdog.</strong> &ldquo;Watch [spreadsheet / API / price feed]. Alert me the moment anything moves more than [X] or breaks the pattern. Include what changed and a draft of the response.&rdquo;</p></div></div>
  <div class="step"><div class="sn">4</div><div class="st"><p><strong>The personal CRM.</strong> &ldquo;After every meeting I log, record: what was decided, what I promised, and the follow-up date. Every Friday, send me the open loops: what is overdue, what is due next week, and who I have not followed up with.&rdquo;</p></div></div>
</section>

<section class="page">
  <div class="sec-head">
    <div class="num">09</div>
    <h2>What&rsquo;s next</h2>
  </div>
  <div class="tip">
    <span class="k">Pass it on</span>
    <p>Know someone still doing everything themselves? Send them guide 001. New to Muse? Enter the code <code>DGC4EX</code> in Settings within 48 hours of joining: you get 1 billion tokens, and so does the person who invited you.</p>
  </div>
  <div class="closer">
    <span class="k">Keep going</span>
    <h2>This is guide 003.</h2>
    <p>You have gone from chatbot to coworker to systems builder to leverage. You delegate tasks, build systems, and compose teams of agents wired to your data.</p>
    <p>The free API catalog, the MCP server directory, and the component library are live now. Next up: setup walkthroughs with keys, auth, and copy-paste config blocks that work the first time.</p>
    <div class="brand">PLUGMYAGENT.COM &nbsp;//&nbsp; &copy; 2026 HIDDENINWEST</div>
  </div>
</section>
"""

out_pdf = os.path.join(out_dir, "ai-agents-advanced-guide.pdf")
render_guide_pdf(
    "An Advanced Guide to AI Agents: From Systems to Leverage",
    html_body,
    out_pdf,
)
