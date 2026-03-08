---
name: checkpoint
description: Create or verify a checkpoint in your workflow
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# Checkpoint

Save and compare progress snapshots.

## Usage

- `/checkpoint create <name>` — Run verify, create git stash/commit, log checkpoint
- `/checkpoint verify <name>` — Compare current state with checkpoint
- `/checkpoint list` — Show all checkpoints with name, timestamp, SHA, status
- `/checkpoint clear` — Remove old checkpoints (keeps last 5)

## Typical Flow

```
/checkpoint create "feature-start"
→ Implement
/checkpoint create "core-done"
→ Test
/checkpoint verify "core-done"
→ Refactor
/checkpoint create "refactor-done"
→ PR
/checkpoint verify "feature-start"
```
