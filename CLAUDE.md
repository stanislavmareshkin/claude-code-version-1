# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

AI Social Media Post Automation system with Claude Code integration. Features battle-tested workflows from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) (v1.8.0).

## Architecture

- **ai-social-media-post-automation/** - Main application (Make.com automation, platform adapters)
- **agents/** - Specialized subagents for delegation (planner, code-reviewer, tdd-guide, etc.)
- **skills/** - Workflow definitions and domain knowledge (coding standards, patterns, testing)
- **commands/** - Slash commands invoked by users (/tdd, /plan, /e2e, etc.)
- **hooks/** - Trigger-based automations (session persistence, pre/post-tool hooks)
- **rules/** - Always-follow guidelines (security, coding style, testing requirements)
- **mcp-configs/** - MCP server configurations for external integrations

## Key Commands

- `/tdd` - Test-driven development workflow
- `/plan` - Implementation planning
- `/e2e` - Generate and run E2E tests
- `/code-review` - Quality review
- `/build-fix` - Fix build errors
- `/learn` - Extract patterns from sessions
- `/skill-create` - Generate skills from git history
- `/verify` - Run verification loop
- `/quality-gate` - Quality gate checks
- `/checkpoint` - Save progress checkpoint

## Running the App

```bash
cd ai-social-media-post-automation
pip install -r requirements.txt
python main.py
```

## Development Notes

- Python project — follow rules in rules/python/
- Security rules in rules/common/security.md
- Git workflow in rules/common/git-workflow.md
- MCP servers config in mcp-configs/mcp-servers.json (copy needed servers to ~/.claude.json)
