# Stack setup instructions

**You are Claude Code. The user has asked you to set up the AI ops stack. Follow these steps exactly. Run each command, confirm success, then proceed to the next.**

---

## Step 1: Clone the repos

```bash
git clone https://github.com/lee-fuhr/build-bible ~/build-bible
git clone https://github.com/lee-fuhr/atlas ~/atlas
git clone https://github.com/lee-fuhr/memeta ~/memeta
```

If a directory already exists, skip that clone and note it.

---

## Step 2: Set up Memeta

```bash
python3 -m venv ~/.local/venvs/memory-system
~/.local/venvs/memory-system/bin/pip install -e ~/memeta
```

Run `~/.local/venvs/memory-system/bin/pytest ~/memeta/tests/ -q --ignore=~/memeta/tests/wild` to confirm the install. If tests pass, proceed.

---

## Step 3: Copy slash commands

```bash
mkdir -p ~/.claude/commands
cp ~/build-bible/commands/qq-bible-add.md ~/.claude/commands/
cp ~/atlas/commands/qq-arch-add.md ~/.claude/commands/
cp ~/atlas/commands/qq-arch-load.md ~/.claude/commands/
```

This gives the user `/qq-bible-add` (ingest knowledge into the Build Bible), `/qq-arch-add` (register a new system component), and `/qq-arch-load` (route to the right Atlas section).

---

## Step 4: Create rules files

```bash
mkdir -p ~/.claude/rules
```

Create `~/.claude/rules/build-bible.md` with this content:

```markdown
<!-- Auto-loaded rule: Build Bible reference -->

## How we build

**Full document:** `~/build-bible/build-bible.md`

Load this when: starting a project, making architecture decisions, choosing patterns, or when any rule below seems relevant.

### Always active

1. Orchestrate, don't execute — delegate to specialist agents. Solo execution only for single atomic actions.
2. TDD: red, green, refactor — tests must fail first. No exceptions.
3. Simplicity wins — delete what isn't earning its complexity. 500-line file limit.
4. Single source of truth — one canonical store per data domain. No sync jobs, no drift.
5. Checkpoint gates — measurable criteria, specific dates, predetermined failure response.
6. Prevent, don't recover — validate before acting. Layered pre-validation for external actions.
7. Atomic operations — temp file + rename. Never leave partial state.
8. Observe everything — structured logging, health checks, tiered alerting for every service.

### Anti-patterns to catch

| Name | Signal |
|------|--------|
| The 49-day research agent | Automation running without checkpoint validation |
| The premature learning engine | Building ML/scoring at low data volume |
| The retrospective test | Tests written after implementation |
| Multiple sources of truth | Sync jobs between data stores |
| The god file | Any file approaching 500 lines |
| The silent service | Deployed service with no monitoring |
```

Create `~/.claude/rules/atlas.md` with this content:

```markdown
<!-- Auto-loaded rule: Atlas architecture reference -->

## Atlas — system component placement

**Full document:** `~/atlas/atlas-framework.md`

Load this when: placing a new component, resolving a conflict, or asking "where does X live?"

### The KCA model

```
Knowledge   ← what the system KNOWS (consultable, never auto-fires)
  ├─ Principles  → Build Bible, architectural decisions
  └─ Experience  → memory system, session index, decision journal

Capability  ← what the system is SET UP TO DO (fires on trigger)
  ├─ Machinery   → CLAUDE.md, agents, LaunchAgents, databases, scripts
  └─ Protocols   → hooks, skills, rules files, SOPs

Activity    ← what the system is DOING RIGHT NOW (ephemeral)
  └─ Execution   → live sessions, running scripts, active agents
```

### The 3 placement tests

1. **Consult-vs-fire** — activates automatically? → Capability. Sits waiting to be read? → Knowledge.
2. **Authority record** — single source of truth for principles? → Knowledge/Principles. For empirical facts? → Knowledge/Experience.
3. **Stability as property** — changes rarely, governs much? → Knowledge. Changes per session? → Capability.
```

---

## Step 5: Memeta session hook

Add the memory consolidation hook so memories are extracted at the end of each session. Add this to `~/.claude/settings.json` under `hooks.Stop`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.local/venvs/memory-system/bin/python3 ~/memeta/hooks/session-memory-consolidation-async.py"
          }
        ]
      }
    ]
  }
}
```

If `settings.json` already has hooks, merge carefully — don't overwrite existing entries.

---

## Step 6: Confirm

Report:
- Which repos were cloned (or already existed)
- Whether Memeta tests passed and how many
- Which commands are now in `~/.claude/commands/`
- Whether rules files were created
- Whether the Memeta hook was added

Then tell the user: start a new Claude Code session for the rules to take effect. Run `/qq-bible-add` on anything worth keeping. Run `/qq-arch-add` when adding a new component to your system.
