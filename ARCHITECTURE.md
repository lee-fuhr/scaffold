# Architecture

This starter kit is organized around the KCA model (Knowledge / Capability / Activity). This document gives you the quick version. For the full framework with precedence rules, inter-layer flows, and evolution protocols, see the [atlas](https://github.com/lee-fuhr/atlas) repo.

## The model

```
Knowledge    -- what the system KNOWS (consulted, pulled, never auto-fires)
  Principles    Normative beliefs: build principles, architecture decisions
  Experience    Empirical records: session history, memory files, system inventories

Capability   -- what the system is SET UP TO DO (standing apparatus, fires on trigger)
  Machinery     Infrastructure: CLAUDE.md, agent definitions, scripts, databases, LaunchAgents
  Protocols     Governance: hooks, skills, rules files, sweeps, verification protocols

Activity     -- what the system is DOING RIGHT NOW (ephemeral, born from Capability)
  Execution     Live processes: active sessions, running agents, scripts in flight
```

Three layers. Five sub-layers. Everything in the system fits into one of them.

## How this repo maps to the model

```
ai-ops-starter/
|
|-- claude/
|   |-- CLAUDE.md            --> Capability / Machinery
|   |                            (loads every session, configures behavior)
|   |
|   |-- rules/               --> Capability / Protocols
|   |                            (auto-loaded, governs behavior)
|   |
|   +-- skills/              --> Capability / Protocols
|                                (invoked on demand, governs behavior)
|
|-- hooks/                   --> Capability / Protocols
|                                (fires on events, governs behavior)
|
|-- launchagents/            --> Capability / Machinery
|                                (fires on schedule, standing infrastructure)
|
|-- scripts/                 --> Capability / Machinery
|                                (fires when invoked, standing infrastructure)
|
|-- docs/                    --> Knowledge / Principles + Experience
|   |-- kca-model.md             (prescriptive: how to classify components)
|   |-- adapting-this.md         (prescriptive: how to customize)
|   +-- anti-patterns.md        (prescriptive: what to avoid)
|
|-- ARCHITECTURE.md          --> Knowledge / Principles
|                                (prescriptive: architectural reference)
|
+-- README.md                --> Knowledge / Experience
                                 (descriptive: what this repo is and how to use it)
```

Notice that most of this repo is Capability. That is intentional. A starter kit is primarily infrastructure and governance scaffolding -- the Knowledge layer grows as you use the system, and the Activity layer is ephemeral by definition.

## The three placement tests

When you add something new and aren't sure where it goes:

**Test 1 -- Consult vs. fire.** Would you consult this like a reference, or does it load and fire automatically? Consult = Knowledge. Fire = Capability. Running right now = Activity.

**Test 2 -- Authority record.** Is this the canonical source, or a derived copy? Canonical sources live where their nature dictates. Derivatives live downstream.

**Test 3 -- Stability as property.** Stable because it's foundational? Knowledge/Principles. Stable because it's battle-tested? Capability.

Most components resolve at test 1. See [docs/kca-model.md](docs/kca-model.md) for worked examples.

## The six arrows

Layers connect through directional flows:

| Arrow | Direction | What it does |
|-------|-----------|-------------|
| Constraint | Knowledge/Principles --> Capability | Principles limit what Capability can do |
| Configuration | Capability --> Activity | Capability configures how sessions run |
| Capture | Activity --> Knowledge/Experience | Sessions produce lasting records |
| Adaptation | Knowledge/Experience --> Capability/Protocols | Experience informs protocol changes |
| Codification | Capability/Protocols --> Knowledge/Principles | Proven protocols become principles |
| Escalation | Activity --> Knowledge/Principles | Emergency bypass, human judgment only |

The most important arrow for getting started is **Configuration**: get your CLAUDE.md, hooks, and rules files right, and your sessions will be well-configured from the start.

## Full framework

This is the 20% that handles 80% of placement decisions. For the complete framework -- including precedence rules for resolving conflicts, cross-cutting concerns, health monitoring, drift detection, and the evolution protocol for changing the architecture itself -- see the [atlas](https://github.com/lee-fuhr/atlas) repo.
