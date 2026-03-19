# Skills directory

## What are skills?

Skills are on-demand capabilities for Claude Code. Each skill is a directory containing
a `SKILL.md` file that Claude reads when you invoke it. Unlike rules (which auto-load
every session), skills load only when requested — keeping your context window clean.

**Key difference from rules:**
- Rules (`~/.claude/rules/`) = always active, auto-loaded every session
- Skills (`~/.claude/skills/` or project-level) = loaded on demand when you ask for them

## How skills work

1. You ask Claude to do something (e.g., "debug this test failure")
2. Claude checks for relevant skills
3. If found, it reads the `SKILL.md` file to learn the procedure
4. It follows the skill's instructions to complete the task

A skill is just a markdown file with structured instructions. No code, no plugins —
just a document that teaches Claude a procedure.

## Skill structure

```
~/.claude/skills/
  debugging/
    SKILL.md          # The skill instructions
  code-quality/
    SKILL.md
  tdd/
    SKILL.md
```

Each `SKILL.md` typically contains:
- **When to use** — trigger conditions
- **Procedure** — step-by-step instructions
- **Examples** — concrete demonstrations
- **Checklist** — verification steps before declaring done

## Creating your own skill

1. Create a directory under `~/.claude/skills/` (or in your project)
2. Write a `SKILL.md` with clear instructions
3. Test by asking Claude to use it: "use the [skill-name] skill for this"

### Template

```markdown
# [Skill name]

## When to use
[Describe trigger conditions — when should Claude reach for this skill?]

## Procedure
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Checklist
- [ ] [Verification step 1]
- [ ] [Verification step 2]
```

## Recommended starter skills

These are good skills to build first:

| Skill | Purpose |
|-------|---------|
| **debugging** | Structured approach to diagnosing failures (reproduce, isolate, fix, verify) |
| **code-quality** | Checklist-driven code review (types, errors, naming, file size, dead code) |
| **tdd** | Red-green-refactor workflow enforcement |
| **personal-voice** | Your communication style guide (for drafting emails, messages) |
| **git-workflow** | Your branching/commit/PR conventions |

## Where to find community skills

- The Claude Code documentation: https://docs.anthropic.com/en/docs/claude-code
- Community repositories (search GitHub for "claude code skills")
- The scaffold repo you are reading now

## Tips

- Keep skills focused — one skill per capability, not mega-skills
- Include concrete examples in your SKILL.md — Claude learns better from examples
- Test your skill a few times and refine the instructions based on what Claude gets wrong
- Skills can reference other files (e.g., "read the voice guide at [path]")
