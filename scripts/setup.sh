#!/usr/bin/env bash
# setup.sh — Set up the ai-ops-starter directory structure and copy templates.
#
# Usage:
#   bash scripts/setup.sh
#
# This script:
#   1. Creates the directory structure (~/.claude/rules/, ~/.claude/skills/, etc.)
#   2. Copies template files to the right locations (with confirmation prompts)
#   3. Creates placeholder directories for memories, logs, etc.
#   4. Prints a "what to do next" message
#
# Safe to re-run: checks before overwriting any existing files.

set -euo pipefail

# --- Configuration ---

CLAUDE_DIR="$HOME/.claude"
RULES_DIR="$CLAUDE_DIR/rules"
SKILLS_DIR="$CLAUDE_DIR/skills"
HOOKS_DIR="$CLAUDE_DIR/hooks"
LOG_DIR="$HOME/.local/log"
VENVS_DIR="$HOME/.local/venvs"
MEMORY_DIR="$HOME/.local/share/memory"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# Find the repo root (directory containing this script's parent)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Helper functions ---

info() {
    echo "[+] $1"
}

warn() {
    echo "[!] $1"
}

ask_overwrite() {
    local dest="$1"
    if [[ -f "$dest" ]]; then
        echo ""
        warn "File already exists: $dest"
        read -r -p "    Overwrite? (y/N) " response
        case "$response" in
            [yY][eE][sS]|[yY]) return 0 ;;
            *) return 1 ;;
        esac
    fi
    return 0
}

copy_template() {
    local src="$1"
    local dest="$2"

    if ask_overwrite "$dest"; then
        cp "$src" "$dest"
        info "Copied: $dest"
    else
        info "Skipped: $dest (existing file preserved)"
    fi
}

# --- Main ---

echo "============================================"
echo "  ai-ops-starter setup"
echo "============================================"
echo ""
echo "This will create directories and copy template files."
echo "Existing files will NOT be overwritten without confirmation."
echo ""

# Step 1: Create directories

info "Creating directories..."

mkdir -p "$RULES_DIR"
info "  $RULES_DIR"

mkdir -p "$SKILLS_DIR"
info "  $SKILLS_DIR"

mkdir -p "$HOOKS_DIR"
info "  $HOOKS_DIR"

mkdir -p "$LOG_DIR"
info "  $LOG_DIR"

mkdir -p "$VENVS_DIR"
info "  $VENVS_DIR"

mkdir -p "$MEMORY_DIR"
info "  $MEMORY_DIR"

# macOS only: ensure LaunchAgents directory exists
if [[ "$(uname)" == "Darwin" ]]; then
    mkdir -p "$LAUNCH_AGENTS_DIR"
    info "  $LAUNCH_AGENTS_DIR"
fi

echo ""

# Step 2: Copy template files

info "Copying template files..."
echo ""

# Global CLAUDE.md
copy_template "$REPO_DIR/claude/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"

# Rules
copy_template "$REPO_DIR/claude/rules/how-we-build.md" "$RULES_DIR/how-we-build.md"
copy_template "$REPO_DIR/claude/rules/atlas.md" "$RULES_DIR/atlas.md"
copy_template "$REPO_DIR/claude/rules/voice.md" "$RULES_DIR/voice.md"

# Hooks
copy_template "$REPO_DIR/hooks/session-rename.py" "$HOOKS_DIR/session-rename.py"
copy_template "$REPO_DIR/hooks/topic-capture.py" "$HOOKS_DIR/topic-capture.py"

echo ""

# Step 3: Summary and next steps

echo "============================================"
echo "  Setup complete"
echo "============================================"
echo ""
echo "Directories created:"
echo "  $RULES_DIR         <- Auto-loaded rules (active every session)"
echo "  $SKILLS_DIR        <- On-demand skills (loaded when requested)"
echo "  $HOOKS_DIR         <- Event-driven hook scripts"
echo "  $LOG_DIR           <- Log files for LaunchAgents and scripts"
echo "  $VENVS_DIR         <- Python virtual environments (outside cloud sync)"
echo "  $MEMORY_DIR        <- Memory storage (session records, learned facts)"
echo ""
echo "Templates copied (customize these):"
echo "  $CLAUDE_DIR/CLAUDE.md              <- Your global behavior config"
echo "  $RULES_DIR/how-we-build.md         <- Your engineering principles"
echo "  $RULES_DIR/atlas.md                <- Your architecture reference"
echo "  $RULES_DIR/voice.md                <- Your communication style"
echo "  $HOOKS_DIR/session-rename.py       <- Example Stop hook"
echo "  $HOOKS_DIR/topic-capture.py        <- Example UserPromptSubmit hook"
echo ""
echo "Next steps:"
echo ""
echo "  1. CUSTOMIZE TEMPLATES"
echo "     Open each file above and replace [YOUR_...] placeholders with your values."
echo "     Start with CLAUDE.md — it is the most impactful single file."
echo ""
echo "  2. REGISTER HOOKS (optional)"
echo "     To activate the hook templates, add them to ~/.claude/settings.json:"
echo ""
echo '     {'
echo '       "hooks": {'
echo '         "UserPromptSubmit": [{'
echo '           "command": "python3 ~/.claude/hooks/topic-capture.py",'
echo '           "timeout": 5000'
echo '         }],'
echo '         "Stop": [{'
echo '           "command": "python3 ~/.claude/hooks/session-rename.py",'
echo '           "timeout": 5000'
echo '         }]'
echo '       }'
echo '     }'
echo ""
echo "  3. BUILD YOUR BUILD BIBLE (optional)"
echo "     Create a how-we-build.md with your full engineering principles."
echo "     The rules/how-we-build.md file is just a summary that points to it."
echo ""
echo "  4. SET UP LAUNCHAGENTS (optional, macOS only)"
echo "     See launchagents/README.md for instructions on scheduling background jobs."
echo ""
echo "  5. CREATE YOUR FIRST SKILL"
echo "     See claude/skills/README.md for the skill format and starter ideas."
echo ""
