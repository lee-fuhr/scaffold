# Hooks

## What are hooks?

Hooks are event-driven scripts that Claude Code triggers automatically during a session.
They run outside Claude's context — they can read input, perform side effects (log to a
file, call an API, set a status), and optionally inject content back into the conversation.

Hooks are the most powerful extension point in Claude Code. They are also the most
dangerous — they run automatically, without confirmation, every time their event fires.

## The 7 event types

| Event | Fires when... | Common uses |
|-------|--------------|-------------|
| **PreToolUse** | Before Claude calls a tool (Read, Write, Bash, etc.) | Intercept dangerous commands, inject warnings |
| **PostToolUse** | After a tool call completes | Log tool usage, capture outputs |
| **UserPromptSubmit** | When the user submits a prompt | Inject context, capture topics, route requests |
| **AssistantResponse** | When Claude produces a response | Log responses, extract metadata |
| **SessionStart** | When a new session begins | Set up environment, load context |
| **SessionEnd** | When a session ends normally | Clean up, save state, index session |
| **Stop** | When Claude stops generating (including mid-turn) | Update status indicators, log completion |

## How hooks receive data

Hooks receive a JSON object on **stdin** with event-specific fields. The exact schema
depends on the event type. Example for `UserPromptSubmit`:

```json
{
  "type": "UserPromptSubmit",
  "prompt": "Fix the failing test in auth.py",
  "session_id": "abc123",
  "cwd": "/Users/you/project"
}
```

## How hooks respond

Hooks write a JSON object to **stdout** to influence the session:

```json
{
  "continue": true,
  "message": "Optional message to inject into Claude's context"
}
```

- `"continue": true` — proceed normally (default if no output)
- `"continue": false` — block the action (PreToolUse only)
- `"message"` — inject text into Claude's context

If a hook produces no stdout, Claude Code treats it as `{"continue": true}`.

## Installing hooks

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "python3 ~/.claude/hooks/topic-capture.py",
        "timeout": 5000
      }
    ],
    "Stop": [
      {
        "command": "python3 ~/.claude/hooks/session-rename.py",
        "timeout": 5000
      }
    ]
  }
}
```

**Key fields:**
- `command` — the shell command to run (must be executable)
- `timeout` — maximum runtime in milliseconds (hooks that hang block the session)

## Security considerations

Hooks run automatically. That means:

1. **Audit before installing.** Read every line of a hook script before adding it.
   A malicious hook on `PreToolUse` could intercept every file read and write.

2. **Minimize permissions.** Hooks should do the minimum necessary. A logging hook
   should not also modify files.

3. **Set timeouts.** A hook without a timeout that hangs will freeze your session.
   5000ms (5 seconds) is a reasonable default for most hooks.

4. **Test in isolation first.** Run the hook script manually with sample JSON input
   before installing it as a live hook.

5. **Version control your hooks.** Keep them in a repo so you can review changes.

## Included templates

- `session-rename.py` — Demonstrates the Stop event; renames session based on topic
- `topic-capture.py` — Demonstrates UserPromptSubmit; extracts topics from prompts

These are templates with placeholder logic. Customize them for your workflow.

## Debugging hooks

If a hook is not working:

1. **Check stderr** — Hook errors go to stderr (visible in Claude Code's debug output)
2. **Run manually** — `echo '{"type":"Stop","session_id":"test"}' | python3 your-hook.py`
3. **Check JSON output** — Must be valid JSON on stdout, or empty
4. **Check timeout** — If the hook takes longer than the timeout, it gets killed
5. **Check permissions** — The script must be executable or called via an interpreter
