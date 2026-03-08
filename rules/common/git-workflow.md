# Git Workflow

## Commit Messages

- Use conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- Keep subject line under 72 characters
- Use imperative mood: "Add feature" not "Added feature"
- Reference issue numbers when applicable

## Branching

- `main` / `master` — production-ready code
- `feature/*` — new features
- `fix/*` — bug fixes
- `claude/*` — Claude Code automated changes

## Best Practices

- Commit early, commit often
- Each commit should be a logical unit of work
- Don't mix refactoring with feature changes in one commit
- Never commit secrets or credentials
- Review diff before committing
- Keep commits atomic — one change per commit

## Pull Requests

- Keep PRs focused and small (under 400 lines when possible)
- Write descriptive PR titles and descriptions
- Link related issues
- Request reviews from relevant team members
