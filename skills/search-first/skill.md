---
name: search-first
description: Research-first development — systematizes searching for existing solutions before implementing
origin: ECC
---

# Search-First Development

Systematizes the "search for existing solutions before implementing" workflow.

## When to Activate

- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- Before creating a new utility, helper, or abstraction
- The user asks "add X functionality" and you're about to write code

## Workflow

```
1. NEED ANALYSIS — Define what functionality is needed
2. PARALLEL SEARCH — npm/PyPI, MCP/Skills, GitHub/Web
3. EVALUATE — Score candidates (functionality, maintenance, community, license)
4. DECIDE — Adopt as-is | Extend/Wrap | Build Custom
5. IMPLEMENT — Install package / Configure MCP / Write minimal custom code
```

## Decision Matrix

| Signal | Action |
|--------|--------|
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + write thin wrapper |
| Multiple weak matches | **Compose** — combine 2-3 small packages |
| Nothing suitable found | **Build** — write custom, informed by research |

## Quick Mode (inline)

0. Does this already exist in the repo? -> `rg` through relevant modules
1. Is this a common problem? -> Search npm/PyPI
2. Is there an MCP for this? -> Check `~/.claude/settings.json`
3. Is there a skill for this? -> Check `~/.claude/skills/`
4. Is there a GitHub implementation? -> GitHub code search

## Integration Points

- **With planner agent**: Researcher identifies available tools before architecture review
- **With architect agent**: Technology stack decisions, integration patterns
- **With iterative-retrieval**: Progressive discovery (broad -> evaluate -> test)

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **Ignoring MCP**: Not checking if an MCP server already provides the capability
- **Over-customizing**: Wrapping a library so heavily it loses its benefits
- **Dependency bloat**: Installing a massive package for one small feature
