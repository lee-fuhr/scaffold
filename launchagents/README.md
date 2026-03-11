# LaunchAgents

## What are LaunchAgents?

LaunchAgents are macOS's built-in job scheduler for user-level background tasks. They are
plist (XML) files that tell macOS to run a script on a schedule or in response to events.

Think of them as cron jobs with better macOS integration — they survive reboots, can run
on login, and integrate with macOS's logging infrastructure.

**Where they live:** `~/Library/LaunchAgents/`

## When to use LaunchAgents vs. cron

| Use case | Recommendation |
|----------|---------------|
| Scheduled tasks on macOS | LaunchAgents (native, survives sleep/wake) |
| Scheduled tasks on Linux | cron or systemd timers |
| Cross-platform scripts | cron (universal) |
| Tasks that need macOS integration | LaunchAgents (Console.app logging, launchctl management) |
| One-off delayed execution | `at` command or just run it manually |

**Key advantage of LaunchAgents:** If the Mac is asleep when a job was scheduled to run,
macOS will run it when the machine wakes up. Cron silently skips missed jobs.

## How to install

1. Copy the plist file to `~/Library/LaunchAgents/`:
   ```bash
   cp com.you.daily-digest.plist ~/Library/LaunchAgents/
   ```

2. Load the agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.you.daily-digest.plist
   ```

3. Verify it is loaded:
   ```bash
   launchctl list | grep com.you
   ```

## How to manage

```bash
# Load (register and start watching schedule)
launchctl load ~/Library/LaunchAgents/com.you.daily-digest.plist

# Unload (stop watching schedule)
launchctl unload ~/Library/LaunchAgents/com.you.daily-digest.plist

# Run immediately (for testing)
launchctl start com.you.daily-digest

# Check status (exit code of last run: 0 = success)
launchctl list | grep com.you

# Remove entirely
launchctl unload ~/Library/LaunchAgents/com.you.daily-digest.plist
rm ~/Library/LaunchAgents/com.you.daily-digest.plist
```

## How to debug

1. **Check launchctl list** — The third column shows the last exit code (0 = OK)
   ```bash
   launchctl list | grep com.you
   ```

2. **Check log files** — If your plist specifies `StandardOutPath` and `StandardErrorPath`,
   check those files for output and errors.

3. **Check Console.app** — Open Console.app, filter by your label (e.g., "com.you").
   macOS logs launchd events here.

4. **Common issues:**
   - Script path wrong or not executable
   - Python not found (use full path: `/usr/bin/python3` or venv path)
   - Working directory not set (`WorkingDirectory` key)
   - Permission denied (check file permissions on the script)
   - Plist syntax error (validate with `plutil -lint your.plist`)

## Naming convention

Use reverse-domain notation: `com.[yourname].[job-name].plist`

Examples:
- `com.you.daily-digest.plist`
- `com.you.session-indexer.plist`
- `com.you.memory-consolidation.plist`

## Templates

See `templates/` for ready-to-customize plist files:
- `daily-digest.plist.template` — Runs a script daily at a configurable time
