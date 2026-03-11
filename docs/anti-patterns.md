# Anti-patterns

Common mistakes when building AI-augmented operations systems. Each one looks reasonable at first and causes compounding damage over time.

---

## The god file

**What it is:** One massive CLAUDE.md that contains every instruction, every rule, every agent definition, every protocol. 800+ lines, growing with every session.

**What it costs:** Claude Code loads the full file every session, burning context window on instructions that are irrelevant to the current task. Editing becomes dangerous -- changing one section breaks another. New sessions can't quickly find what matters.

**What to do instead:** Use the tiered system. Global CLAUDE.md for identity and broad directives. Rules files for specific behavioral constraints. Project CLAUDE.md for project context. Keep each file under 200 lines with a single clear purpose. If a file is approaching 500 lines, it's a god file in the making -- split it.

---

## Solo execution

**What it is:** The orchestrator (your main Claude Code session) writes code, runs tests, edits files, and debugs -- doing everything directly instead of delegating to specialist agents.

**What it costs:** The orchestrator's context window fills with implementation details instead of coordination state. Quality drops because a generalist session writing code is worse than a specialist agent with focused instructions. You lose parallelism -- one session doing five things sequentially vs. five agents doing them simultaneously.

**What to do instead:** Default to delegation. For every task, ask: "Is this a single atomic action?" If no, delegate to an agent. The orchestrator's job is coordination, synthesis, and quality control. The only things it should execute directly are single-step actions where spinning up an agent would cost more than just doing it.

---

## The retrospective test

**What it is:** Writing implementation code first, then writing tests afterward to confirm it works. The tests always pass because they were written to match the existing behavior.

**What it costs:** Tests that were never seen to fail prove nothing. They don't catch regressions because they were shaped to match the current code, not the intended behavior. When you refactor, these tests break in unhelpful ways because they test implementation details rather than contracts.

**What to do instead:** Red, green, refactor. Write the test first. Watch it fail (the red phase -- this proves the test actually exercises the code). Write the minimum code to make it pass (green). Then refactor while tests stay green. Never skip the red phase. A test that has never failed is a test you cannot trust.

---

## The silent service

**What it is:** A background job (LaunchAgent, cron job, scheduled script) running without logging, monitoring, or health checks. It was set up once and assumed to keep working.

**What it costs:** The job fails silently and you don't notice for weeks or months. Data goes stale. Downstream systems that depend on it degrade gradually. When you finally discover the failure, you've lost the context of what went wrong because there are no logs.

**What to do instead:** Every background job needs three things: (1) structured logging to a file you will actually check, (2) a health check that verifies the job is running and producing expected output, and (3) alerting that notifies you when it fails or when output stops. If you can't answer "how would I know if this job stopped working?" then the job is a silent service.

---

## The 49-day research agent

**What it is:** An automation (agent, script, recurring job) that runs for an extended period without checkpoint validation. Named for a real case: a research agent ran for 49 days before anyone checked whether its output was useful. It wasn't.

**What it costs:** Wasted compute, wasted time, and the false confidence that work is getting done. The longer it runs unchecked, the harder it is to course-correct because you've lost the context of the original intent.

**What to do instead:** Every automation needs checkpoint gates: measurable criteria, specific dates, and a predetermined response for failure. "After 7 days, check: has this produced at least N useful outputs? If no, stop and re-evaluate." The checkpoint must be on a calendar, not "when I get around to it." Short feedback loops are always better than long ones.

---

## Multiple sources of truth

**What it is:** The same data living in two or more places with sync jobs keeping them in agreement. A database and a JSON file that both claim to be authoritative. A CLAUDE.md summary and a principles document that both define the rules.

**What it costs:** Sync jobs fail. When they do, you have two conflicting versions and no way to know which is current. Even when sync works, there's always a window where the sources disagree. Teams and sessions make decisions based on whichever source they happen to read, leading to inconsistent behavior.

**What to do instead:** One canonical store per data domain. Everything else is a derived view that is clearly marked as non-authoritative. If you need the data in a different format, derive it on read rather than syncing it on write. The canonical source is the one where data is created and maintained; everything else points back to it.

---

## Validate-then-pray

**What it is:** Wrapping dangerous operations in try/catch blocks instead of validating preconditions before acting. "Try to write the file, catch the error if it fails" instead of "check that the directory exists, check permissions, check disk space, then write."

**What it costs:** Error handling after the fact is always more expensive than prevention. Partial state is the worst outcome -- the operation half-completed before failing, leaving things in an inconsistent state. Try/catch tells you something went wrong but often not what or why, making debugging harder.

**What to do instead:** Layered pre-validation for any operation with consequences. Check every precondition you can before acting. Validate inputs, verify state, confirm permissions. Use try/catch as a safety net for genuinely unexpected failures, not as a substitute for thinking about what could go wrong. For operations that modify state, use atomic patterns: write to a temp file, then rename.

---

## The premature learning engine

**What it is:** Building ML, scoring algorithms, or automated classification systems before you have enough data to train or validate them. "Let's build a smart prioritization engine" when you have 30 data points.

**What it costs:** Engineering time spent on sophistication that can't be validated. The system produces outputs that look authoritative but are statistically meaningless. Worse, people start trusting the outputs, making decisions based on noise.

**What to do instead:** Start with manual processes and simple heuristics. Collect data. When you have enough volume that manual review is painful and enough history to validate predictions, then build the learning engine. The threshold is higher than you think -- most systems need hundreds to thousands of data points before ML outperforms a human with a spreadsheet.
