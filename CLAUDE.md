# CLAUDE.md - AI Assistant Guide

## Project Overview

This repository is a **Claude Code skills and tooling collection** containing reusable skill templates for Claude Code. It provides backend development utilities and UI design system tools organized as Claude skills under the `.claude/skills/` directory.

The project is Python-based with no application runtime -- it is a library of standalone scripts and reference documentation that Claude Code uses to augment its capabilities.

## Repository Structure

```
.claude/
  skills/
    creative-design/
      ui-design-system/          # UI design token generation toolkit
        SKILL.md                 # Skill manifest and documentation
        scripts/
          design_token_generator.py  # Generates color, typography, spacing tokens
    development/
      senior-backend/            # Backend development toolkit
        SKILL.md                 # Skill manifest and documentation
        references/
          api_design_patterns.md       # API design patterns and practices
          backend_security_practices.md # Security implementation guide
          database_optimization_guide.md # DB optimization strategies
        scripts/
          api_scaffolder.py        # API project scaffolding tool
          api_load_tester.py       # API load testing tool
          database_migration_tool.py # Database migration utility
```

## Skills System

### How Skills Work

Each skill lives under `.claude/skills/<category>/<skill-name>/` and contains:

- **`SKILL.md`** -- The skill manifest with YAML frontmatter (`name`, `description`) and usage documentation. This is what Claude Code reads to understand the skill's capabilities.
- **`scripts/`** -- Executable Python scripts that implement the skill's functionality.
- **`references/`** -- (Optional) Markdown documentation with patterns, practices, and guidelines.

### Available Skills

#### 1. UI Design System (`creative-design/ui-design-system`)

Generates comprehensive design system tokens from a brand color. Outputs color palettes, typography scales, spacing systems, shadows, animations, and breakpoints.

```bash
python .claude/skills/creative-design/ui-design-system/scripts/design_token_generator.py [brand_color] [style] [format]
```

- **brand_color**: Hex color (default: `#0066CC`)
- **style**: `modern` | `classic` | `playful`
- **format**: `json` | `css` | `scss` | `summary`

#### 2. Senior Backend (`development/senior-backend`)

Backend development toolkit with three scripts:

```bash
# Scaffold a new API project
python .claude/skills/development/senior-backend/scripts/api_scaffolder.py <target-path> [--verbose] [--json] [--output file]

# Run database migrations
python .claude/skills/development/senior-backend/scripts/database_migration_tool.py <target-path> [--verbose] [--json] [--output file]

# Load test an API
python .claude/skills/development/senior-backend/scripts/api_load_tester.py <target-path> [--verbose] [--json] [--output file]
```

All three scripts share a common interface: a positional `target` path argument, `--verbose`/`-v` for detailed output, `--json` for JSON output, and `--output`/`-o` to write results to a file.

## Tech Stack

- **Language**: Python 3 (standard library only -- no external dependencies)
- **Key modules used**: `json`, `argparse`, `pathlib`, `colorsys`, `sys`, `os`

## Development Conventions

### Code Style

- Python scripts use class-based architecture with a `main()` entry point
- Each script class follows the pattern: `__init__` -> `run()` -> `validate_target()` -> `analyze()` -> `generate_report()`
- Scripts are invoked via `python scripts/<script_name>.py` with argparse-based CLI interfaces
- All scripts are standalone -- they do not import from each other

### SKILL.md Format

Skill manifests use YAML frontmatter with two required fields:

```yaml
---
name: skill-name
description: One-line description of what the skill does and when to use it.
---
```

The body contains Markdown documentation for the skill's capabilities and usage.

### Adding New Skills

1. Create a directory under `.claude/skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`)
3. Place executable scripts in a `scripts/` subdirectory
4. Optionally add reference docs in a `references/` subdirectory
5. Ensure scripts are self-contained with no external dependencies

### File Naming

- Skill directories: `kebab-case` (e.g., `ui-design-system`)
- Python scripts: `snake_case` (e.g., `design_token_generator.py`)
- Reference docs: `snake_case` with `.md` extension
- Categories: `kebab-case` (e.g., `creative-design`, `development`)

## Running Scripts

No build step or dependency installation is required. All scripts use the Python standard library:

```bash
# Example: generate design tokens as CSS variables
python .claude/skills/creative-design/ui-design-system/scripts/design_token_generator.py "#FF6600" modern css

# Example: scaffold an API project
python .claude/skills/development/senior-backend/scripts/api_scaffolder.py ./my-project --verbose

# Example: run database migration tool with JSON output
python .claude/skills/development/senior-backend/scripts/database_migration_tool.py ./db-dir --json --output results.json
```

## Git Workflow

- Feature branches follow the pattern `claude/<description>-<id>`
- Commits should have clear, descriptive messages
- No CI/CD pipeline is currently configured
- No pre-commit hooks are configured
