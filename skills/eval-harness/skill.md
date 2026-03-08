---
name: eval-harness
description: Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles.
origin: ECC
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Eval Harness Skill

A formal evaluation framework implementing eval-driven development (EDD) principles.

## When to Activate

- Setting up eval-driven development for AI-assisted workflows
- Defining pass/fail criteria for task completion
- Measuring agent reliability with pass@k metrics
- Creating regression test suites for prompt or agent changes
- Benchmarking performance across model versions

## Philosophy

Eval-Driven Development treats evals as the "unit tests of AI development":
- Define expected behavior BEFORE implementation
- Run evals continuously during development
- Track regressions with each change
- Use pass@k metrics for reliability measurement

## Eval Types

### Capability Evals
Test if Claude can do something it couldn't before:
```markdown
[CAPABILITY EVAL: feature-name]
Task: Description
Success Criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
Expected Output: Description
```

### Regression Evals
Ensure changes don't break existing functionality:
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHA or checkpoint
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
Result: X/Y passed
```

## Grader Types

1. **Code-Based Grader** — Deterministic assertions (grep, tests, build)
2. **Model-Based Grader** — LLM-as-judge rubric scoring
3. **Human Grader** — Manual review for ambiguous outputs

## Metrics

### pass@k
"At least one success in k attempts"
- pass@1: First attempt success rate
- pass@3: Success within 3 attempts (target: > 90%)

### pass^k
"All k trials succeed"
- pass^3: 3 consecutive successes (for critical paths)

## Eval Workflow

1. **Define** (before coding) — Capability + regression evals
2. **Implement** — Write code to pass evals
3. **Evaluate** — Run evals, record PASS/FAIL
4. **Report** — Summary with pass@k metrics

## Report Format

```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  Overall:         2/2 passed

Regression Evals:
  login-flow:      PASS
  Overall:         1/1 passed

Metrics:
  pass@1: 50% (1/2)
  pass@3: 100% (2/2)

Status: READY FOR REVIEW
```

## Best Practices

1. Define evals BEFORE coding
2. Run evals frequently
3. Track pass@k over time
4. Use code graders when possible (deterministic > probabilistic)
5. Human review for security
6. Keep evals fast
7. Version evals with code

## Recommended Thresholds

- Capability evals: pass@3 >= 0.90
- Regression evals: pass^3 = 1.00 for release-critical paths
