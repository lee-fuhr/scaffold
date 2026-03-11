#!/usr/bin/env python3
"""
Hook: topic-capture.py
Event: UserPromptSubmit (fires when the user submits a prompt)

Purpose:
    Demonstrates reading the user's prompt from stdin on every submission.
    Template logic: extracts keywords/topics and could inject context or log them.

Install in ~/.claude/settings.json:
    {
      "hooks": {
        "UserPromptSubmit": [
          {
            "command": "python3 ~/.claude/hooks/topic-capture.py",
            "timeout": 5000
          }
        ]
      }
    }

Input (stdin JSON):
    {
      "type": "UserPromptSubmit",
      "prompt": "Fix the failing test in auth.py",
      "session_id": "abc123",
      "cwd": "/Users/you/project"
    }

Output (stdout JSON):
    {
      "continue": true,
      "message": "Optional context to inject into Claude's view"
    }

Customize:
    - Extract topics and inject relevant context (e.g., "this file was changed recently")
    - Route prompts to different workflows based on keywords
    - Log all prompts for session indexing
    - Inject reminders (e.g., "remember: this project uses pytest, not unittest")
"""

import json
import sys
from pathlib import Path


def extract_keywords(prompt: str) -> list[str]:
    """
    Extract notable keywords from the user's prompt.

    PLACEHOLDER: Replace with your own logic. Examples:
    - NLP-based topic extraction
    - Regex for file paths, function names, error codes
    - Match against a project glossary
    """
    keywords = []

    # Simple example: detect file extensions mentioned in the prompt
    extensions = [".py", ".ts", ".js", ".md", ".json", ".yaml", ".toml"]
    for ext in extensions:
        if ext in prompt:
            keywords.append(f"file-type:{ext}")

    # Simple example: detect common task verbs
    task_verbs = ["fix", "add", "remove", "refactor", "test", "debug", "deploy", "review"]
    prompt_lower = prompt.lower()
    for verb in task_verbs:
        if verb in prompt_lower.split():
            keywords.append(f"task:{verb}")

    return keywords


def build_context_injection(keywords: list[str], cwd: str) -> str | None:
    """
    Optionally build a context message to inject into Claude's view.

    PLACEHOLDER: Replace with your own logic. Examples:
    - If "test" keyword detected, inject "This project uses pytest with fixtures in conftest.py"
    - If a specific file is mentioned, inject its recent git history
    - If a known pattern is detected, inject the relevant skill recommendation
    """
    # Example: return None to inject nothing (most common case)
    # Uncomment and customize to inject context:
    #
    # if "task:debug" in keywords:
    #     return "Reminder: use the debugging skill for structured diagnosis."
    #
    # if "task:test" in keywords:
    #     return "Reminder: this project uses pytest. Run with: pytest -x -v"

    return None


def log_prompt(session_id: str, prompt: str, keywords: list[str]) -> None:
    """
    Log the prompt and extracted keywords.

    PLACEHOLDER: Write to your preferred storage.
    """
    log_path = Path.home() / ".claude" / "prompt-log.jsonl"

    record = {
        "session_id": session_id,
        "prompt_preview": prompt[:200],  # First 200 chars only
        "keywords": keywords,
    }

    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(record) + "\n")
    except IOError:
        pass  # Logging failure should never block the session


def main():
    # Read event data from stdin
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        event = json.loads(raw)
    except (json.JSONDecodeError, IOError):
        return

    if event.get("type") != "UserPromptSubmit":
        return

    prompt = event.get("prompt", "")
    session_id = event.get("session_id", "unknown")
    cwd = event.get("cwd", "")

    # Extract keywords from the prompt
    keywords = extract_keywords(prompt)

    # Log the prompt (optional — comment out if you do not want logging)
    log_prompt(session_id, prompt, keywords)

    # Build optional context injection
    context = build_context_injection(keywords, cwd)

    # Output response
    output = {"continue": True}
    if context:
        output["message"] = context

    print(json.dumps(output))


if __name__ == "__main__":
    main()
