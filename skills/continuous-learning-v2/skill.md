---
name: continuous-learning-v2
description: Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts.
origin: ECC
version: 2.1.0
---

# Continuous Learning v2.1 - Instinct-Based Architecture

An advanced learning system that turns Claude Code sessions into reusable knowledge through atomic "instincts" — small learned behaviors with confidence scoring.

**v2.1** adds **project-scoped instincts** — React patterns stay in React projects, Python conventions stay in Python projects, universal patterns are shared globally.

## When to Activate

- Setting up automatic learning from Claude Code sessions
- Configuring instinct-based behavior extraction via hooks
- Tuning confidence thresholds for learned behaviors
- Reviewing, exporting, or importing instinct libraries
- Evolving instincts into full skills, commands, or agents

## The Instinct Model

An instinct is a small learned behavior:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional
```

**Properties:**
- **Atomic** — one trigger, one action
- **Confidence-weighted** — 0.3 = tentative, 0.9 = near certain
- **Domain-tagged** — code-style, testing, git, debugging, workflow
- **Evidence-backed** — tracks observations
- **Scope-aware** — `project` (default) or `global`

## How It Works

```
Session Activity → Hooks capture tool use → observations.jsonl
    → Pattern Detection (corrections, resolutions, workflows)
    → Creates/updates instincts (project-scoped or global)
    → /evolve clusters into skills/commands/agents
```

## Confidence Scoring

| Score | Meaning | Behavior |
|-------|---------|----------|
| 0.3 | Tentative | Suggested but not enforced |
| 0.5 | Moderate | Applied when relevant |
| 0.7 | Strong | Auto-approved for application |
| 0.9 | Near-certain | Core behavior |

**Increases**: pattern repeatedly observed, user doesn't correct
**Decreases**: user explicitly corrects, pattern not seen for long time

## Scope Decision Guide

| Pattern Type | Scope | Examples |
|-------------|-------|---------|
| Language/framework conventions | **project** | "Use React hooks", "Follow Django patterns" |
| Security practices | **global** | "Validate user input", "Sanitize SQL" |
| General best practices | **global** | "Write tests first", "Handle errors" |
| Git practices | **global** | "Conventional commits" |

## Commands

```bash
/instinct-status     # Show learned instincts
/evolve              # Cluster instincts into skills/commands
/instinct-export     # Export instincts to file
/instinct-import     # Import instincts from others
/promote             # Promote project instincts to global
/projects            # List projects and instinct counts
```

## File Structure

```
~/.claude/homunculus/
├── identity.json
├── projects.json
├── observations.jsonl
├── instincts/
│   ├── personal/
│   └── inherited/
├── evolved/
│   ├── agents/
│   ├── skills/
│   └── commands/
└── projects/
    └── <project-hash>/
        ├── observations.jsonl
        ├── instincts/personal/
        └── evolved/
```

## Why Hooks vs Skills for Observation?

Hooks fire **100% of the time**, deterministically. Every tool call is observed, no patterns are missed. Skills are probabilistic (~50-80% activation).

## Privacy

- Observations stay local on your machine
- Project-scoped instincts are isolated per project
- Only instincts (patterns) can be exported — not raw observations
- No code or conversation content is shared
