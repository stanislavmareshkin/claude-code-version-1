# Development Workflow

## Feature Implementation Workflow

0. **Research & Reuse** (mandatory before any new implementation)
   - Search codebase first for existing implementations and patterns
   - Check package registries before writing utility code
   - Prefer battle-tested libraries over hand-rolled solutions
   - Look for open-source projects that solve 80%+ of the problem

1. **Plan First**
   - Use **planner** agent to create implementation plan
   - Identify dependencies and risks
   - Break down into phases

2. **TDD Approach**
   - Use **tdd-guide** agent
   - Write tests first (RED)
   - Implement to pass tests (GREEN)
   - Refactor (IMPROVE)
   - Verify 80%+ coverage

3. **Code Review**
   - Use **code-reviewer** agent immediately after writing code
   - Address CRITICAL and HIGH issues
   - Fix MEDIUM issues when possible

4. **Commit & Push**
   - Detailed commit messages
   - Follow conventional commits format
   - See git-workflow.md for commit message format and PR process
