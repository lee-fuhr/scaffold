# Adapting this starter kit

This is a template, not a finished system. Here is how to make it yours.

## Step 1: Replace all placeholders

Search the repo for `[YOUR_` and replace every instance:

```bash
grep -r "\[YOUR_" --include="*.md" --include="*.sh" --include="*.plist" .
```

Common placeholders you will find:

| Placeholder | Replace with | Example |
|-------------|-------------|---------|
| `[YOUR_NAME]` | Your name | `Jane Smith` |
| `[YOUR_ORG]` | Your organization identifier | `com.acme` |
| `[YOUR_GITHUB]` | Your GitHub username or org | `acme-labs` |
| `[YOUR_PROJECT]` | Your primary project name | `client-dashboard` |
| `[YOUR_WORKING_DIR]` | Your Claude Code working directory | `/Users/you/projects` |
| `[YOUR_VENV_PATH]` | Python virtual environment path | `~/.local/venvs/ops` |

## Step 2: Set up your CLAUDE.md hierarchy

Claude Code loads instructions from CLAUDE.md files at multiple levels. Decide your tier structure:

**Tier 1 -- Global** (`~/.claude/CLAUDE.md`)
Behaviors that apply to every session regardless of project. Put your core operating philosophy here: delegation preferences, response format, questioning protocol, verification requirements.

**Tier 2 -- Rules** (`~/.claude/rules/*.md`)
Auto-loaded behavioral governance. Each file is a focused concern: code quality standards, voice/writing style, integration-specific behaviors. Keep each file under 100 lines and focused on one domain.

**Tier 3 -- Project** (`/path/to/project/CLAUDE.md`)
Project-specific context and instructions. Tech stack, conventions, key file locations, project-specific agent routing.

**Tier 4 -- Directory** (`/path/to/project/subdir/CLAUDE.md`)
Subdirectory overrides. Rare -- use only when a directory has genuinely different rules (e.g., a `docs/` folder with different formatting standards).

Start with Tier 1 and Tier 2. Add project-level CLAUDE.md files as you start working in specific codebases. Most people never need Tier 4.

### What goes in CLAUDE.md vs. rules files

**CLAUDE.md:** Identity, operating mode, response format, session management, broad directives. Think "who you are and how you work."

**Rules files:** Specific behavioral constraints. Think "what you must always/never do." Code quality standards, naming conventions, integration configurations, security protocols.

The practical test: if it applies regardless of what task you're doing, it's probably CLAUDE.md. If it's a specific constraint that kicks in during certain types of work, it's a rules file.

## Step 3: Choose which hooks to enable

Hooks fire automatically on Claude Code events. Start conservative -- every hook adds latency and complexity.

**Recommended first hooks:**

| Hook | Event | Purpose |
|------|-------|---------|
| `session-start.sh` | SessionStart | Set up session context, load state files |
| `pre-tool-use.sh` | PreToolUse | Validate dangerous operations before they execute |

**Add later when you need them:**

| Hook | Event | Purpose |
|------|-------|---------|
| `post-tool-use.sh` | PostToolUse | Log operations, update state |
| `notification.sh` | Stop | Alert you when long-running sessions finish |
| `user-prompt.sh` | UserPromptSubmit | Pre-process or validate user input |

**Hook principles:**
- Hooks must be fast. If it takes more than 1-2 seconds, it's too slow for a hook.
- Hooks must be reliable. A failing hook disrupts every session.
- Start with 1-2 hooks. Add more only when you feel a specific pain point.

## Step 4: Create your first agent definitions

Agent definitions are markdown files that configure how spawned agents behave. A minimal definition:

```markdown
# [Agent name]

## Role
[One sentence: what this agent does]

## Instructions
[Specific behavioral directives for this agent type]

## Constraints
[What this agent must NOT do]

## Output format
[What the agent returns when done]
```

**Start with these agent types:**

1. **Code agent** -- writes and modifies code, runs tests
2. **Research agent** -- reads files, searches codebases, reports findings
3. **QA agent** -- reviews code, runs verification checklists

You do not need 47 agents on day one. Start with 2-3 that match your actual work patterns and add more as you discover repeated delegation needs.

## Step 5: Set up background jobs

LaunchAgents are macOS-specific. If you are not on macOS, use cron jobs or systemd timers instead.

A LaunchAgent template is in `launchagents/templates/`. To enable one:

```bash
# 1. Customize the plist
cp launchagents/templates/com.[YOUR_ORG].example.plist \
   ~/Library/LaunchAgents/com.myorg.session-indexer.plist

# 2. Edit: set paths, schedule, logging
open ~/Library/LaunchAgents/com.myorg.session-indexer.plist

# 3. Load it
launchctl load ~/Library/LaunchAgents/com.myorg.session-indexer.plist

# 4. Verify it's running
launchctl list | grep myorg
```

**Good first background jobs:**
- Session indexer -- catalog your Claude Code sessions for searchability
- Memory consolidation -- merge per-session memories into long-term storage
- Health check -- verify your hooks, scripts, and databases are healthy

**Background job principles:**
- Every job must log its output somewhere you will actually look
- Every job needs a health check (how do you know it's still working?)
- Start with daily schedules. Move to hourly only when daily is insufficient.

## Step 6: Growing the system over time

The system grows through a natural cycle:

1. **You notice a pain point** in your Claude Code workflow (repeated manual steps, inconsistent behavior, lost context between sessions)
2. **You build a solution** (a new hook, a new agent type, a new background job, a new knowledge file)
3. **You classify it** using the KCA model (is this Knowledge, Capability, or Activity?) and put it in the right place
4. **You observe it working** (or not) over multiple sessions
5. **Proven patterns become principles** -- document what you've learned in your build methodology

### Signs you're growing well

- New components have obvious homes in the existing structure
- You can explain to someone (or a new Claude session) why each piece exists
- Removing a component would cause a specific, nameable loss
- Your system documentation stays roughly current because components are well-classified

### Signs you're growing poorly

- New files go wherever is convenient, no consistent logic
- You have multiple files that do similar things and you're not sure which is canonical
- CLAUDE.md is over 500 lines and growing
- You have hooks/scripts that you're afraid to touch because you're not sure what depends on them
- Background jobs that you're not sure are still running or still needed

### Maintenance rhythm

| Cadence | Action |
|---------|--------|
| Per session | Capture decisions and learnings while they're fresh |
| Weekly | Review what you built this week; is anything misplaced? |
| Monthly | Audit background jobs (still running? still needed?). Review CLAUDE.md for bloat |
| Quarterly | Full system review. Delete what's dead. Document what's undocumented |

The quarterly review is the most important. Systems rot from neglect faster than from bad decisions.
