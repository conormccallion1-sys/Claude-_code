---
name: ponytail-audit
description: >
  Whole-repo audit for over-engineering. Like ponytail-review but scans the
  entire codebase instead of a diff: produces a ranked list of what to delete,
  simplify, or replace with stdlib/native equivalents. Use when asked to audit
  the whole repo for bloat, complexity, or over-engineering. One-shot,
  read-only.
license: MIT
---

# Ponytail Audit

Whole-repo over-engineering audit. Same philosophy as ponytail-review, broader
scope.

## Tags

| Tag | Meaning |
|-----|---------|
| `delete` | Unused or speculative code |
| `stdlib` | Hand-rolled duplicates of standard library functions |
| `native` | Redundant dependencies or platform features |
| `yagni` | Over-abstracted code with single implementations |
| `shrink` | Logic that can be condensed |

## Output format

Ranked by estimated impact (highest first):

```
<tag> <what to cut>. <replacement>. [path:line]
```

Summary at the end:

```
total: ~-<N> lines · <D> dependencies removable
```

## Rules

- Ranked list, highest impact first.
- Read-only: findings only, no fixes applied.
- Correctness bugs, security, performance → out of scope.
- `ponytail:` comments are deliberate shortcuts — skip them.
- Minimal tests and assertions are never flagged.
