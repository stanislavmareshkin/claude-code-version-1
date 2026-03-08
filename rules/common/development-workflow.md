# Development Workflow

## Before Starting

1. Understand the requirement fully before coding
2. Check existing code for similar patterns
3. Plan the approach — use `/plan` for complex changes
4. Create a checkpoint: `/checkpoint create "before-feature"`

## During Development

1. Work in small, incremental steps
2. Commit frequently with descriptive messages
3. Run tests after every change
4. Keep the build green at all times

## Before Committing

1. Run `/verify` to check build, types, lint, tests
2. Review your own diff: `git diff`
3. Run `/code-review` for quality checks
4. Remove debug statements (console.log, print, etc.)

## Before PR

1. Run `/verify pre-pr` for full verification
2. Ensure all tests pass
3. Update documentation if needed
4. Create descriptive PR title and description
