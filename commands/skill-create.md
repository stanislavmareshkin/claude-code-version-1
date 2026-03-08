---
name: skill-create
description: Analyze local git history to extract coding patterns and generate skill files
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# Skill Create

Analyze git history to detect and document coding patterns.

## Usage

- `/skill-create` — analyze current repo
- `/skill-create --commits 100` — last 100 commits
- `/skill-create --output ./skills` — custom output directory

## Analysis Steps

1. **Gather Git Data** — Recent commits with file changes, frequency, message patterns
2. **Detect Patterns** — Commit conventions, file co-changes, workflow sequences, architecture, testing
3. **Generate Skill File** — Markdown with frontmatter (name, description, version, source)
4. **Sections**: Commit Conventions, Code Architecture, Workflows, Testing Patterns
