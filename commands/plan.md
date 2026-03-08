---
name: plan
description: Implementation planning — analyze requirements and create step-by-step plan before coding
allowed_tools: ["Read", "Grep", "Glob", "Agent"]
---

# Plan

Invoke the planner agent to establish an implementation strategy before coding begins.

## When to Use

- New features
- Substantial architecture modifications
- Involved refactoring
- Multi-file changes
- Ambiguous specifications

## Process

1. **Clarify Requirements** — Ask questions if anything is unclear
2. **Identify Risks** — Flag potential issues, breaking changes, edge cases
3. **Step-by-Step Breakdown** — Create ordered list of implementation steps
4. **User Confirmation** — Wait for explicit approval before proceeding

## Important

The planner will **NOT** write any code until you explicitly confirm the plan.

You may:
- Approve the plan as-is
- Propose modifications
- Suggest alternatives
- Restructure phase ordering
