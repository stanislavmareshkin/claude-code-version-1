---
name: quality-gate
description: Run ECC quality pipeline on demand for a file or project scope
allowed_tools: ["Bash", "Read", "Grep", "Glob"]
---

# Quality Gate

Run the quality pipeline on demand.

## Usage

`/quality-gate [path|.] [--fix] [--strict]`

- Default target: current directory (`.`)
- `--fix`: allow auto-format/fix where configured
- `--strict`: fail on warnings where supported

## Pipeline

1. Detect language/tooling for target
2. Run formatter checks
3. Run lint/type checks when available
4. Produce a concise remediation list
