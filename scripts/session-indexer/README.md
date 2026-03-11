# Session indexer

## What this does

A session indexer makes your Claude Code sessions searchable. Without one, finding
"that conversation where I fixed the auth bug" means scrolling through dozens of
session files. With one, you search by keyword, date, project, or topic.

## The pattern

```
Claude Code sessions (JSONL transcripts)
    |
    v
Parser (extract metadata: topics, files touched, duration, summary)
    |
    v
Storage (SQLite database or search-friendly index)
    |
    v
Query interface (CLI or script to search sessions)
```

### Step 1: Parse session transcripts

Claude Code stores session data as JSONL. A parser script reads each session and
extracts:
- Session ID and timestamps
- Working directory / project
- User prompts (first prompt = likely topic)
- Files read and written
- Tools used
- Duration

### Step 2: Store in a searchable format

SQLite is a good default — single file, no server, full-text search support.

```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    started_at TEXT,
    ended_at TEXT,
    project TEXT,
    topic TEXT,
    first_prompt TEXT,
    files_touched TEXT,  -- JSON array
    duration_seconds INTEGER
);

-- Full-text search on topics and prompts
CREATE VIRTUAL TABLE sessions_fts USING fts5(
    topic, first_prompt, content=sessions
);
```

### Step 3: Query

```bash
# Find sessions about auth
python3 search-sessions.py "auth"

# Find sessions in a specific project
python3 search-sessions.py --project my-app

# Find sessions from last week
python3 search-sessions.py --since 2026-02-27
```

## This is a placeholder

This directory contains the concept and pattern, not a full implementation.
For a production-grade session indexer with FSRS-based spaced repetition and
memory consolidation, see the **Memeta** memory system:

https://github.com/lee-fuhr/memeta

## Building your own

If you want to build a simple version:

1. Write a parser that reads Claude Code session JSONL files
2. Extract the fields listed above
3. Store in SQLite with FTS5
4. Write a CLI search script
5. (Optional) Run the parser via a LaunchAgent on a schedule

Estimated effort: a few hours for a basic version that covers 80% of use cases.
