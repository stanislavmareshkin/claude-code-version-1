# CLAUDE.md - AI Assistant Guide

## Project Overview

This repository is a **Claude Code skills and tooling collection** containing reusable skill templates, reference documentation, and plugin configurations for Claude Code. It provides backend development utilities, UI design system tools, and a full suite of Anthropic's knowledge-work plugins organized for AI-augmented workflows.

The project is Python-based with no application runtime -- it is a library of standalone scripts and reference documentation that Claude Code uses to augment its capabilities.

## Repository Structure

```
.claude/
  settings.json                  # Plugin configuration (knowledge-work-plugins)
  skills/
    creative-design/
      ui-design-system/          # UI design token generation toolkit
        SKILL.md
        scripts/
          design_token_generator.py
    development/
      senior-backend/            # Backend development toolkit
        SKILL.md
        references/
          api_design_patterns.md
          backend_security_practices.md
          database_optimization_guide.md
        scripts/
          api_scaffolder.py
          api_load_tester.py
          database_migration_tool.py
CLAUDE.md                        # This file
```

## Installed Plugins

All 11 plugins from `anthropics/knowledge-work-plugins` are installed at project scope:

| Plugin | Purpose |
|--------|---------|
| **productivity** | Task management, calendars, daily workflows |
| **sales** | Prospect research, call prep, pipeline review, outreach |
| **customer-support** | Ticket triage, draft responses, escalations |
| **product-management** | Specs, roadmaps, research synthesis, competitor tracking |
| **marketing** | Content drafting, campaigns, brand voice, competitor briefs |
| **legal** | Contract review, NDA triage, compliance, risk assessment |
| **finance** | Journal entries, reconciliation, financial statements |
| **data** | SQL queries, data exploration, visualization, dashboards |
| **enterprise-search** | Cross-platform search (email, chat, docs, wikis) |
| **bio-research** | Literature search, genomics analysis, drug discovery |
| **cowork-plugin-management** | Create and customize plugins |

Plugins are configured in `.claude/settings.json`. Each plugin provides:
- **Skills** -- domain expertise that activates automatically when relevant
- **Slash commands** -- explicitly invoked via `/<plugin>:<command>` (e.g., `/sales:call-prep`, `/data:write-query`)
- **Connectors** -- MCP server integrations for external tools (Slack, Jira, Notion, etc.)

## Skills System

### How Skills Work

Each skill lives under `.claude/skills/<category>/<skill-name>/` and contains:

- **`SKILL.md`** -- Skill manifest with YAML frontmatter (`name`, `description`) and usage documentation
- **`scripts/`** -- Executable Python scripts implementing the skill's functionality
- **`references/`** -- (Optional) Markdown documentation with patterns, practices, and guidelines

### Available Skills

#### 1. UI Design System (`creative-design/ui-design-system`)

Generates design system tokens (colors, typography, spacing, shadows, animations, breakpoints) from a brand color.

```bash
python .claude/skills/creative-design/ui-design-system/scripts/design_token_generator.py [brand_color] [style] [format]
```

- **brand_color**: Hex color (default: `#0066CC`)
- **style**: `modern` | `classic` | `playful`
- **format**: `json` | `css` | `scss` | `summary`

#### 2. Senior Backend (`development/senior-backend`)

Backend development toolkit with three scripts sharing a common CLI interface:

```bash
# Scaffold a new API project
python .claude/skills/development/senior-backend/scripts/api_scaffolder.py <target-path> [--verbose] [--json] [--output file]

# Run database migrations
python .claude/skills/development/senior-backend/scripts/database_migration_tool.py <target-path> [--verbose] [--json] [--output file]

# Load test an API
python .claude/skills/development/senior-backend/scripts/api_load_tester.py <target-path> [--verbose] [--json] [--output file]
```

## Tech Stack

- **Language**: Python 3 (standard library only -- no external dependencies)
- **Key modules**: `json`, `argparse`, `pathlib`, `colorsys`, `sys`, `os`
- **Plugins**: Anthropic knowledge-work-plugins (11 plugins)

## Development Conventions

### Code Style

- Python scripts use class-based architecture with a `main()` entry point
- Class pattern: `__init__` -> `run()` -> `validate_target()` -> `analyze()` -> `generate_report()`
- Scripts are standalone with argparse-based CLI interfaces -- no cross-imports
- Type hints used throughout (`Dict`, `List`, `Optional`)

### SKILL.md Format

```yaml
---
name: skill-name
description: One-line description of what the skill does and when to use it.
---
```

Body contains Markdown documentation for capabilities and usage.

### Adding New Skills

1. Create directory under `.claude/skills/<category>/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter (`name`, `description`)
3. Place executable scripts in `scripts/` subdirectory
4. Optionally add reference docs in `references/` subdirectory
5. Keep scripts self-contained with no external dependencies

### File Naming

- Skill directories: `kebab-case` (e.g., `ui-design-system`)
- Python scripts: `snake_case` (e.g., `design_token_generator.py`)
- Reference docs: `snake_case.md`
- Categories: `kebab-case` (e.g., `creative-design`, `development`)

## Git Workflow

- Feature branches: `claude/<description>-<id>`
- Commits should have clear, descriptive messages
- Push with: `git push -u origin <branch-name>`
