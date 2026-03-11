<!-- Auto-loaded rule: how we build -->
<!-- Lives at: ~/.claude/rules/how-we-build.md -->
<!-- Customize this with YOUR principles from YOUR build bible. -->
<!-- This is a SUMMARY — the full bible lives in your build-bible document. -->
<!-- See: https://github.com/lee-fuhr/build-bible for the full reference. -->

## How we build (rules summary)

**Full bible:** `[YOUR_WORKSPACE]/how-we-build.md`
**Load when:** Starting a project, making architecture decisions, reviewing code.

### Critical rules (always active)

<!-- These are universal engineering principles. Keep, remove, or add your own.
     Each rule should be one line — detailed rationale lives in the full bible. -->

1. **Orchestrate, don't execute** — Delegate to specialist agents. Solo execution only for single atomic actions.
2. **TDD: red, green, refactor** — Write a failing test first. Make it pass. Clean up. No exceptions.
3. **Simplicity wins** — Delete what is not earning its complexity. No file over 500 lines.
4. **Single source of truth** — One canonical store per data domain. No sync jobs, no drift.
5. **Atomic operations** — Temp file + rename. Never leave partial state on disk.
6. **Prevent, don't recover** — Validate inputs before acting. Do not rely on try/catch for flow control.
7. **Config-driven** — Scale with data files, not code changes. Hard-coded values are tech debt.
8. **Document when fresh** — Capture decisions during work, not after. Memory decays fast.
9. **Unhappy path first** — Test error paths and edge cases before happy paths.
10. **Speed hides debt** — Fast shipping without verification creates invisible debt. Slow down to verify.

### Anti-patterns to catch

<!-- Train Claude to recognize and flag these when it sees them in your codebase. -->

| Name | Signal | Response |
|------|--------|----------|
| The retrospective test | Tests written after implementation | Rewrite test-first |
| Multiple sources of truth | Sync jobs between data stores | Consolidate to one store |
| The god file | Any file approaching 500 lines | Extract and split |
| Validate-then-pray | Try/catch instead of pre-validation | Add input validation |
| Silent failure | Errors caught but not logged | Add structured logging |
| Solo execution | Conductor writing code instead of delegating | Delegate to agent |

### When to consult the full bible

<!-- Point these to YOUR build bible sections. Adjust section numbers to match. -->

- Starting a new project — playbook phases
- Choosing patterns — reusable pattern catalog
- Architecture decisions — layer model, integration map
- Agent routing — routing table, sequencing dependencies
- Fixing technical debt — debt inventory
- Updating the bible itself — evolution protocol
