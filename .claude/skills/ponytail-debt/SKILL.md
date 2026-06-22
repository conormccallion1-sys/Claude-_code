---
name: ponytail-debt
description: >
  Harvests ponytail: comments from the codebase into a debt ledger. Prevents
  deliberate shortcuts from silently becoming permanent. Use when asked about
  "ponytail debt", "what did ponytail defer", "list the shortcuts",
  "ponytail ledger", or "what did we mark to do later".
license: MIT
---

# Ponytail Debt

Scan the repo for `ponytail:` comments and produce a consolidated debt ledger.

## How to scan

```bash
grep -rn "ponytail:" . --include="*.py" --include="*.js" --include="*.ts" \
  --include="*.tsx" --include="*.jsx" --include="*.go" --include="*.rs" \
  --include="*.rb" --include="*.java" --include="*.kt" --include="*.swift" \
  --include="*.cs" --include="*.cpp" --include="*.c" --include="*.sh" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
  --exclude-dir=build --exclude-dir=__pycache__
```

## Output format

Group by file. One row per marker:

| File:Line | What was simplified | Ceiling | Upgrade trigger |
|-----------|---------------------|---------|-----------------|
| `auth.py:42` | global lock | contention under load | per-account locks if throughput matters |

Flag markers with no upgrade path with `[no-trigger]` — these are the ones
most likely to become permanent debt.

Summary at the end:

```
total: <N> shortcuts · <M> no-trigger (review these)
```

## Convention

The standard comment form is:

```
# ponytail: <ceiling>, <upgrade path>
// ponytail: <ceiling>, <upgrade path>
```

Example: `# ponytail: global lock, per-account locks if throughput matters`

## Boundaries

Read-only by default. Can persist findings to `PONYTAIL-DEBT.md` if asked.
"stop ponytail-debt" or "normal mode" to deactivate.
