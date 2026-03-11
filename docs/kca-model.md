# The KCA model

A framework for organizing every component in an AI-augmented operations system into one of three layers: Knowledge, Capability, and Activity.

## Why you need a model

Without a shared classification system, every question about the system -- "where should this new file live?", "should this load automatically?", "what depends on what?" -- requires reasoning from scratch. Session A puts a config in one place, session B puts a similar one somewhere else, and within weeks the system is a maze of ad-hoc decisions.

The KCA model gives you a map. When the map is accurate, placement decisions are fast lookups instead of ten-minute deliberations. When you're unsure, three concrete tests tell you where something belongs.

## The three layers

### Knowledge -- what the system knows

Reference material the system consults but never automatically executes. Knowledge is pulled, never pushed. No Knowledge component activates on a schedule, on a hook event, or at session start. If something activates automatically, it belongs in Capability even if its content reads like knowledge.

Knowledge has the highest authority and the slowest rate of change.

**Examples:** Development principles, architectural decisions, past session records (when consulted for context), system inventories, meeting transcripts (when referenced).

### Capability -- what the system is set up to do

Standing apparatus and behavioral governance that persists between sessions, ready to activate on a trigger. Capability fires. Every component in this layer either loads automatically (CLAUDE.md, hooks, LaunchAgents) or fires when invoked (skills, scripts, slash commands).

Capability has medium authority and medium rate of change.

**Examples:** CLAUDE.md files, agent definitions, hooks, skills, LaunchAgent plists, Python scripts, SQLite databases, rules files.

### Activity -- what the system is doing right now

Live, ephemeral processes currently executing. Activity is born from Capability's configuration and dies when the process ends. Nothing in Activity survives without being captured into another layer.

Activity has the lowest authority and the fastest rate of change.

**Examples:** A running Claude Code session, a spawned agent in flight, an active LaunchAgent process, a hook script currently executing.

## The five sub-layers

The three layers break into five sub-layers that make placement more precise:

```
Knowledge
  Principles   -- normative (what SHOULD be)
                  Highest authority. Slowest change. Human judgment to modify.
                  Build principles, patterns, anti-patterns, architectural decisions.

  Experience   -- empirical (what HAS BEEN)
                  Medium authority. Grows continuously.
                  Session records, memory files, system inventories, decision journals.

Capability
  Machinery    -- standing apparatus (files, agents, scripts that load and fire)
                  Infrastructure that provides capabilities.
                  CLAUDE.md, agent definitions, databases, LaunchAgents, Python scripts.

  Protocols    -- behavioral governance (rules, hooks, skills that constrain behavior)
                  Governance that directs how Machinery and Activity operate.
                  Rules files, hooks, skills, sweeps, verification protocols.

Activity
  Execution    -- live processes (sessions, running agents, scripts in flight)
                  Fully ephemeral. Born from Configuration, dies when process ends.
                  Active sessions, running agents, tool calls in progress.
```

### Machinery vs. protocols

This is the most common point of confusion. The distinguishing question: does this component **provide infrastructure** (Machinery) or **govern behavior** (Protocols)?

- A database is infrastructure. A hook that validates file size before writes is governance.
- CLAUDE.md is infrastructure (it loads context into sessions). A rules file is governance (it constrains behavior within sessions).
- An agent definition is infrastructure (apparatus that activates). A skill that enforces coding standards is governance.

If you removed a Machinery component, the system would lose a **capability**. If you removed a Protocols component, the system would lose a **constraint**.

### Principles vs. experience

The second common confusion. The distinguishing question: is this **prescriptive** (what should be) or **descriptive** (what has been)?

- "Always write tests before implementation" is a principle (prescriptive).
- "In session #847 we discovered that the API rate limits at 100 req/min" is experience (descriptive).
- Both are Knowledge. Neither fires automatically. The difference determines authority level and maintenance rhythm.

## The three placement tests

When you need to determine where a component belongs, apply these tests in order. Most components resolve at test 1.

### Test 1 -- Consult vs. fire

**Question:** "Would you consult this like a reference, or does it load and fire automatically?"

Imagine a new session starts. Does this component get pulled in and read when needed (consult = Knowledge)? Or does it load/activate/fire without anyone choosing to consult it (fire = Capability)? Or is it a currently-running process (Activity)?

**Example:** Rules files in `~/.claude/rules/` fire automatically -- they load into every session and constrain behavior without anyone choosing to read them. That is Capability/Protocols. The build principles document is consulted -- loaded when you need guidance, not automatically. That is Knowledge/Principles.

**Where intuition misleads:** Agent definitions feel like knowledge -- you'd read them to understand the agent roster. But they fire: when a session spawns an agent, the definition loads and configures that agent's behavior. Standing apparatus that activates on invocation = Capability/Machinery.

### Test 2 -- Authority record

**Question:** "Is this the canonical source, or a derived copy?"

Trace the information to its source. If this component IS the authoritative source, it lives where its nature dictates. If it's a summary or derivative, the derivative lives downstream.

**Example:** A build principle like "Orchestrate, don't execute" in the principles document = canonical, Knowledge/Principles. The CLAUDE.md summary of that same principle = derived copy, Capability/Machinery. The CLAUDE.md entry isn't a principle; it's a piece of machinery that loads the principle's summary into each session.

### Test 3 -- Stability as property

**Question:** "Is this stable because it's foundational, or stable because it's battle-tested?"

Some components are very stable. The question is why. Stable because it expresses foundational beliefs = Knowledge/Principles. Stable because it's been refined through use and works well = Capability.

**Example:** "Single source of truth -- no sync jobs between data stores" is stable because it's a foundational design belief = Knowledge/Principles. A Python script that's been running unchanged for months is stable because it works = Capability/Machinery.

## Mapping common Claude Code components

| Component | Layer | Sub-layer | Why |
|-----------|-------|-----------|-----|
| CLAUDE.md | Capability | Machinery | Loads every session, configures behavior |
| Rules files (`~/.claude/rules/`) | Capability | Protocols | Auto-loaded, govern behavior |
| Hooks (pre-tool-use, session-start, etc.) | Capability | Protocols | Fire on events, govern behavior |
| Skills | Capability | Protocols | Invoked on demand, govern behavior |
| Agent definitions | Capability | Machinery | Standing apparatus, fire when spawned |
| LaunchAgent plists | Capability | Machinery | Fire on schedule |
| Python utility scripts | Capability | Machinery | Fire when invoked |
| SQLite databases (schema + engine) | Capability | Machinery | Active I/O infrastructure |
| Database records (the data itself) | Knowledge | Experience | Empirical record, consulted as reference |
| Build/dev principles | Knowledge | Principles | Consulted, prescriptive, highest authority |
| Architecture decisions | Knowledge | Principles | Consulted, prescriptive, foundational |
| MEMORY.md | Knowledge | Experience | Empirical record, consulted as reference |
| Session history | Knowledge | Experience | Empirical record, consulted as reference |
| System inventory/directory | Knowledge | Experience | Empirical catalog, consulted as reference |
| Active Claude Code session | Activity | Execution | Ephemeral, dies when session ends |
| Running background agent | Activity | Execution | Ephemeral, dies when task completes |
| Hook script currently executing | Activity | Execution | Ephemeral, dies when hook finishes |

## The six arrows (inter-layer flows)

The layers are not static. Six directional flows connect them:

```
1. Constraint      Knowledge/Principles --> Capability
                   Principles constrain what Capability can do.

2. Configuration   Capability --> Activity/Execution
                   Capability configures how Activity runs.

3. Capture         Activity/Execution --> Knowledge/Experience
                   Activity produces artifacts that become Experience.

4. Adaptation      Knowledge/Experience --> Capability/Protocols
                   Experience informs changes to Protocols.

5. Codification    Capability/Protocols --> Knowledge/Principles
                   Proven Protocols get elevated to Principles (requires human judgment).

6. Escalation      Activity/Execution --> Knowledge/Principles (bypass)
                   Emergency direct path, human-only.
```

These arrows are what keep the system alive. Without Capture (#3), Activity produces nothing lasting. Without Adaptation (#4), experience never improves the system. Without Codification (#5), proven patterns never become principles.

The most important arrow for day-to-day work is **Configuration (#2)**: your CLAUDE.md, hooks, rules files, and agent definitions configure every session. Get Capability right and Activity takes care of itself.

## Further reading

- [ARCHITECTURE.md](../ARCHITECTURE.md) -- how this starter kit maps to the KCA model
- [adapting-this.md](adapting-this.md) -- how to customize this system for your work
- [anti-patterns.md](anti-patterns.md) -- common mistakes when building AI-augmented systems
- [atlas](https://github.com/lee-fuhr/atlas) -- the full architectural framework with precedence rules, cross-cutting concerns, and evolution protocols
