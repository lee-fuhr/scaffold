#!/usr/bin/env python3
"""
Hook: session-rename.py
Event: Stop (fires when Claude stops generating)

Purpose:
    Demonstrates the hook interface by reading session data on Stop events.
    Template logic: extracts the session topic and could rename/tag the session.

Install in ~/.claude/settings.json:
    {
      "hooks": {
        "Stop": [
          {
            "command": "python3 ~/.claude/hooks/session-rename.py",
            "timeout": 5000
          }
        ]
      }
    }

Input (stdin JSON):
    {
      "type": "Stop",
      "session_id": "abc123",
      "cwd": "/Users/you/project",
      "reason": "end_turn"
    }

Output (stdout JSON):
    {
      "continue": true
    }

Customize:
    - Replace the placeholder topic extraction with your own logic
    - Write to a session index, database, or rename a log file
    - Add filtering (e.g., only process sessions longer than N turns)
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def extract_topic(session_data: dict) -> str:
    """
    Extract a topic/title from the session data.

    PLACEHOLDER: Replace this with your own logic. Examples:
    - Parse the first user prompt from a session transcript
    - Use the working directory name as the topic
    - Call an LLM to summarize the session
    """
    cwd = session_data.get("cwd", "")
    if cwd:
        return Path(cwd).name
    return "untitled"


def save_session_record(session_id: str, topic: str) -> None:
    """
    Save a record of this session.

    PLACEHOLDER: Replace with your preferred storage. Examples:
    - Append to a JSONL index file
    - Insert into a SQLite database
    - Write to a session-metadata directory
    """
    # Example: append to a JSONL log file
    log_path = Path.home() / ".claude" / "session-log.jsonl"

    record = {
        "session_id": session_id,
        "topic": topic,
        "ended_at": datetime.now().isoformat(),
    }

    # Atomic write: append mode is safe for single-line JSONL entries
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def main():
    # Read event data from stdin
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            # No input — exit silently
            return
        event = json.loads(raw)
    except (json.JSONDecodeError, IOError):
        # If we cannot parse input, exit without disrupting the session
        return

    # Only process Stop events (defensive check)
    if event.get("type") != "Stop":
        return

    session_id = event.get("session_id", "unknown")
    topic = extract_topic(event)

    # Save the session record
    try:
        save_session_record(session_id, topic)
    except IOError as e:
        # Log to stderr (visible in debug mode, does not affect the session)
        print(f"session-rename: failed to save record: {e}", file=sys.stderr)

    # Output: continue normally, no message to inject
    output = {"continue": True}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
