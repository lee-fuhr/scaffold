# Scripts

## Overview

Utility scripts that support your AI operations infrastructure. These are standalone
Python (or shell) scripts that run on their own — either manually, via LaunchAgents,
or triggered by hooks.

## Organization

Organize scripts by function:

```
scripts/
  maintenance/       # Cleanup, rotation, health checks
  analysis/          # Data analysis, reporting, metrics
  automation/        # Recurring workflows, integrations
  session-indexer/   # Session transcript indexing (see its own README)
  setup.sh           # One-time setup script for this repo
```

## Naming conventions

- Use descriptive names: `consolidate-memories.py`, not `cm.py`
- Use hyphens between words: `daily-digest.py`, not `daily_digest.py` or `dailyDigest.py`
- Prefix with verb: `run-`, `check-`, `sync-`, `build-`, `clean-`

## Connecting to LaunchAgents

To run a script on a schedule:

1. Write the script in `scripts/`
2. Create a plist from the template in `launchagents/templates/`
3. Point the plist's `ProgramArguments` at your script
4. Install the plist to `~/Library/LaunchAgents/`

See `launchagents/README.md` for full instructions.

## Connecting to hooks

To run a script in response to Claude Code events:

1. Write the script following the hook interface (stdin JSON, stdout JSON)
2. Register it in `~/.claude/settings.json` under the appropriate event
3. See `hooks/README.md` for the full interface spec

## Virtual environments

If your scripts have Python dependencies, create a virtual environment:

```bash
# IMPORTANT: never create venvs in cloud-synced folders (iCloud, Google Drive, Dropbox)
# Put them in ~/.local/venvs/ instead
python3 -m venv ~/.local/venvs/ai-ops
source ~/.local/venvs/ai-ops/bin/activate
pip install -r requirements.txt
```

Point your LaunchAgent plists at the venv's Python:
`~/.local/venvs/ai-ops/bin/python3`
