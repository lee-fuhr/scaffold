# Scaffold

Every Claude Code setup post on Reddit reinvents the same scaffolding. This is that scaffolding — the folder structure, hooks, skills, and templates that keep showing up in the systems that actually work.

---

## The problem

You know what you want: hooks that fire on events, background jobs that run while you sleep, agents with defined roles, a CLAUDE.md hierarchy that applies different rules to different contexts. You just don't want to spend a week on folder structure before you do any real work.

The structure isn't trivial to get right. Put things in the wrong layer and you'll spend sessions debugging why Claude behaves inconsistently. Start without templates and every hook is a blank file with no reference point. Skip the documentation and three months later you won't remember why the system is built the way it is.

## What changes

**You start building, not scaffolding.** The folder structure is already organized around the KCA model (Knowledge / Capability / Activity). You replace placeholders, not architecture decisions.

**You have working templates to copy.** Not examples from someone else's production system that won't fit your needs -- annotated templates with `[YOUR_...]` placeholders and inline explanations of what each piece does.

**You understand why things go where they go.** Every directory has a README. The docs explain the reasoning, not just the layout. When you add a new component six months from now, you know which folder it belongs in.

## What's in it

```
scaffold/
|
|-- claude/                       # Claude Code configuration
|   |-- CLAUDE.md                 # Root instructions (loaded every session)
|   |-- rules/                    # Auto-loaded behavioral rules
|   |   |-- atlas.md              # Architecture model quick reference
|   |   |-- how-we-build.md       # Build principles summary
|   |   +-- voice.md              # Writing style enforcement
|   +-- skills/
|       +-- README.md             # Skills guide and template
|
|-- hooks/                        # Event-driven automation
|   |-- README.md                 # Hook reference (events, stdin/stdout, security)
|   |-- session-rename.py         # Template: rename sessions on Stop event
|   +-- topic-capture.py          # Template: extract topics on UserPromptSubmit
|
|-- launchagents/                 # macOS background jobs
|   |-- README.md                 # LaunchAgent guide (install, manage, debug)
|   +-- templates/
|       +-- daily-digest.plist.template
|
|-- scripts/                      # Python utilities
|   +-- session-indexer/
|       +-- README.md             # Session indexing pattern and schema
|
|-- docs/
|   |-- kca-model.md              # The Knowledge/Capability/Activity framework
|   |-- adapting-this.md          # How to make this starter kit yours
|   +-- anti-patterns.md          # Common mistakes to avoid at setup time
|
|-- ARCHITECTURE.md               # Architecture overview with pointers to full framework
+-- README.md                     # This file
```

**Get started:** `git clone`, replace `[YOUR_...]` placeholders, copy to `~/.claude/`. Running in an afternoon.

---

## Part of the stack

| Repo | What it does |
|------|-------------|
| **[Build Bible](https://github.com/lee-fuhr/build-bible)** | The engineering methodology — principles, patterns, and failure modes from across the field, synthesized into one living reference. |
| **[Atlas](https://github.com/lee-fuhr/atlas)** | The architectural model — a structural framework for where every component lives, built from the patterns that hold together at scale. |
| **[Memeta](https://github.com/lee-fuhr/memeta)** | The memory system — every technique that works for giving AI agents persistent memory, unified and coexisting additively. |
| **[Scaffold](https://github.com/lee-fuhr/scaffold)** | The starter kit — folder structure, hooks, skills, and templates that production systems converge on, ready to clone. |

This is a seed, not a dependency. Fork it, gut what you don't need, grow it in your direction.

## Contributing

The structure of an AI ops system is still being figured out. If you've found a hook pattern, LaunchAgent approach, CLAUDE.md hierarchy, or folder structure that works better than what's here -- open an issue or a PR. The starter kit should reflect what's actually working in production, not a snapshot from when it was first built.

---

MIT -- see [LICENSE](LICENSE)
