# ai-ops-starter

A starter kit for building an AI-augmented operations system with Claude Code.

## The problem

Claude Code is powerful on its own. But once you move past single sessions into a real operating system -- agents, hooks, background jobs, knowledge files, skills, config hierarchies, memory systems -- things get complicated fast. Where do agent definitions go? How should CLAUDE.md files layer? What fires automatically vs. what gets consulted? How do you keep 50 components from becoming an unmaintainable mess?

This repo gives you a starting structure. Not a dump of someone's production configs, but a curated template with `[YOUR_...]` placeholders, sensible defaults, and enough scaffolding to stand up a working system in an afternoon.

## What you get

```
ai-ops-starter/
|
|-- claude/                       # Claude Code configuration
|   |-- CLAUDE.md                 # Root instructions (load every session)
|   |-- rules/                    # Auto-loaded behavioral rules
|   |   |-- atlas.md              # Architecture model quick reference
|   |   |-- how-we-build.md       # Build principles summary
|   |   +-- voice.md              # Writing style enforcement
|   +-- skills/
|       +-- README.md             # Skills guide + template
|
|-- hooks/                        # Event-driven automation
|   |-- README.md                 # Hook reference (events, stdin/stdout, security)
|   |-- session-rename.py         # Template: rename sessions on Stop event
|   +-- topic-capture.py          # Template: extract topics on UserPromptSubmit
|
|-- launchagents/                 # macOS background jobs
|   |-- README.md                 # LaunchAgent guide (install, manage, debug)
|   +-- templates/
|       +-- daily-digest.plist.template   # Customizable daily-run plist
|
|-- scripts/                      # Python utilities
|   +-- session-indexer/
|       +-- README.md             # Session indexing pattern + schema
|
|-- docs/                         # Documentation
|   |-- kca-model.md              # The Knowledge/Capability/Activity framework
|   |-- adapting-this.md          # How to make this starter kit yours
|   +-- anti-patterns.md          # Common mistakes to avoid
|
|-- ARCHITECTURE.md               # Architecture overview + pointers to full framework
+-- README.md                     # This file
```

## Prerequisites

- **Claude Code** installed and working ([claude.ai/claude-code](https://claude.ai/claude-code))
- **macOS** for LaunchAgent background jobs (the rest works cross-platform)
- **Python 3.11+** for utility scripts
- A text editor you're comfortable with -- you'll be customizing markdown files

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/[YOUR_GITHUB]/ai-ops-starter.git
cd ai-ops-starter

# 2. Review and customize CLAUDE.md
# Replace all [YOUR_...] placeholders with your specifics
open claude/CLAUDE.md

# 3. Copy Claude config to your home directory
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
cp claude/rules/*.md ~/.claude/rules/
# Or symlink if you prefer to keep everything in the repo:
# ln -s $(pwd)/claude/CLAUDE.md ~/.claude/CLAUDE.md

# 4. Enable your first hook (add to ~/.claude/settings.json)
# See hooks/README.md for the settings.json configuration
cp hooks/topic-capture.py ~/.claude/hooks/

# 5. Start a Claude Code session and verify
claude
```

## The architecture behind this

This starter kit is organized around the **KCA model** (Knowledge / Capability / Activity) -- a framework for classifying every component in an AI-augmented system:

- **Knowledge** -- what the system knows (consulted as reference, never fires automatically)
- **Capability** -- what the system can do (standing apparatus that loads and fires on triggers)
- **Activity** -- what the system is doing right now (ephemeral, dies when the process ends)

See [docs/kca-model.md](docs/kca-model.md) for the full explanation, or [ARCHITECTURE.md](ARCHITECTURE.md) for how this repo maps to the model.

## Companion repos

This starter kit handles the operational scaffolding. For the methodology and deeper frameworks:

| Repo | What it provides |
|------|-----------------|
| [build-bible](https://github.com/lee-fuhr/build-bible) | Development methodology -- principles, patterns, anti-patterns, playbook phases. The "how we build" reference. |
| [atlas](https://github.com/lee-fuhr/atlas) | Full architectural framework -- the KCA model in depth, placement tests, inter-layer flows, precedence rules. |
| [memeta](https://github.com/lee-fuhr/memeta) | Memory system -- FSRS spaced repetition for persistent cross-session memory. |

Each repo stands alone. Use what you need.

## How this is meant to be used

This is a **v1.0 starting point**. Fork it, gut what you don't need, add what you do. The structure matters more than the specific contents -- once you understand why hooks live in one place and knowledge files live in another, you can grow the system in whatever direction your work requires.

Do not expect updates. This is a seed, not a dependency.

## Key concepts

**CLAUDE.md hierarchy.** Claude Code loads instructions from multiple CLAUDE.md files. This starter kit uses a tiered approach: global (applies everywhere) > project (applies to one codebase) > directory (applies to one folder). Put broad behavioral rules at the top, specific project context lower.

**Hooks vs. skills.** Hooks fire automatically on events (session start, before a tool call, on stop). Skills are invoked on demand. The distinction matters -- hooks should be fast and non-blocking; skills can be heavier.

**LaunchAgents.** macOS-native scheduled jobs. Use them for background maintenance: session indexing, memory consolidation, health checks. They run whether or not Claude Code is open.

**Rules files.** Auto-loaded markdown in `~/.claude/rules/`. Use them for behavioral governance that should apply to every session without being part of the main CLAUDE.md instruction set.

## License

MIT. See [LICENSE](LICENSE).
