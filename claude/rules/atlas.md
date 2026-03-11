<!-- Auto-loaded rule: Atlas section index -->
<!-- Lives at: ~/.claude/rules/atlas.md -->
<!-- The Atlas is your system architecture reference — the map of how everything fits. -->
<!-- Customize sections to match YOUR Atlas document. -->
<!-- See: https://github.com/lee-fuhr/atlas for the full reference. -->

## Atlas (system architecture reference)

**Full Atlas:** `[YOUR_WORKSPACE]/atlas.md`
**Never load the full Atlas.** Load sections by trigger below.

### When to load each section

<!-- Map your Atlas sections here. The key idea: load ONLY the section you need,
     not the whole document. This preserves context window for actual work. -->

| Section | Load when... |
|---------|-------------|
| **0** How to use | You need to understand the Atlas itself |
| **1** The model | Placing a new component; answering "where does X live?" |
| **2** Precedence | Resolving a conflict between rules or instructions |
| **3** Knowledge / Principles | Working with the build bible; adding architectural decisions |
| **4** Knowledge / Experience | Working with memory systems or session records |
| **5** Capability / Machinery | Working with CLAUDE.md, agents, LaunchAgents, databases, scripts |
| **6** Capability / Protocols | Working with hooks, skills, rules files, or behavioral governance |
| **7** Activity / Execution | Debugging live sessions; understanding failure modes |
| **8** The arrows | Tracing how something propagates through the system |
| **9** Cross-cutting | System health, consistency, session boot sequence |
| **10** Document index | Finding a specific document in the system |

### The KCA model (quick reference)

<!-- KCA = Knowledge, Capability, Activity. This is the core architectural model.
     Adapt or replace with your own architecture model. -->

```
Knowledge   <-- what the system KNOWS (consultable, pulled, never auto-fires)
  |-- Principles  -> Build bible, architectural decisions, universal learnings
  +-- Experience  -> Memory system, session index, decision journal

Capability  <-- what the system is SET UP TO DO (standing apparatus, fires on trigger)
  |-- Machinery   -> CLAUDE.md, agent definitions, LaunchAgents, databases, scripts
  +-- Protocols   -> hooks, skills, rules files, SOPs

Activity    <-- what the system is DOING RIGHT NOW (ephemeral, born from Capability)
  +-- Execution   -> live sessions, running scripts, active agents
```

### Placement tests

<!-- Use these when deciding where a new component belongs in your architecture. -->

1. **Consult-vs-fire** — Does it activate automatically or fire on a trigger? Capability. Does it sit waiting to be read? Knowledge.
2. **Authority record** — Is it the single source of truth for normative guidance? Knowledge/Principles. For empirical facts? Knowledge/Experience.
3. **Stability** — Changes rarely, governs much? Knowledge. Changes per project, fires per session? Capability or Activity.

### Document triangle

<!-- Your core governing documents. Customize names and paths. -->

| Doc | Answers |
|-----|---------|
| Atlas | How it all fits together |
| Build bible | How we build |
| Directory | What exists (component inventory) |
| Memory system | What we remember |
