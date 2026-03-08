---
name: e2e
description: Generate, maintain, and execute end-to-end tests using Playwright
allowed_tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob"]
---

# E2E Testing

Generate and run end-to-end tests with Playwright.

## Capabilities

- **Test Generation** — Playwright tests modeling user workflows
- **Test Execution** — Across Chrome, Firefox, Safari
- **Artifact Capture** — Screenshots, videos, traces during failures
- **Flaky Test Detection** — Identifies and quarantines unstable tests

## Best Practices

- Use Page Object Model architecture
- Use `data-testid` selectors
- Wait for API responses (not arbitrary delays)
- Test genuine user journeys
- E2E tests involving real money MUST run on testnet/staging only

## Avoid

- Brittle selectors
- Implementation-detail testing
- Production environments
- Flaky test acceptance
