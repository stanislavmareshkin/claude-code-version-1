---
name: eval-harness
description: Evaluation harness — measure and improve AI agent performance
origin: ECC
---

# Eval Harness

Framework for evaluating and improving AI agent performance.

## When to Activate

- Measuring agent task completion quality
- Comparing different prompt strategies
- Benchmarking tool usage patterns
- Optimizing cost/quality tradeoffs

## Components

1. **Test Cases** — Defined tasks with expected outcomes
2. **Metrics** — Success rate, token usage, time to completion
3. **Baselines** — Known-good results for comparison
4. **Reports** — Aggregate results with trends

## Metrics

- **Task Success Rate** — % of tasks completed correctly
- **Token Efficiency** — Tokens used per successful task
- **Tool Call Efficiency** — Number of tool calls per task
- **Error Rate** — % of tasks with errors
- **Cost per Task** — Dollar cost per successful completion

## Process

1. Define test cases with clear pass/fail criteria
2. Run evaluation suite
3. Compare against baseline
4. Identify areas for improvement
5. Iterate on prompts/workflows
6. Re-evaluate to confirm improvement
