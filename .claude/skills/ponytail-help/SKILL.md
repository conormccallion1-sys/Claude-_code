---
name: ponytail-help
description: >
  Quick-reference card for all ponytail modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /ponytail-help,
  "ponytail help", "what ponytail commands", "how do I use ponytail".
license: MIT
---

# Ponytail Help

Display this reference card when invoked. One-shot, do NOT change mode or
persist anything.

## Levels

| Level | Trigger | What changes |
|-------|---------|-------------|
| **Lite** | `/ponytail lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/ponytail` | The ladder enforced: YAGNI → stdlib → native → one line → minimum. Default. |
| **Ultra** | `/ponytail ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ponytail** | `/ponytail` | Lazy mode itself. Simplest solution that works. |
| **ponytail-review** | `/ponytail-review` | Over-engineering review: `L42: yagni: factory, one product. Inline.` |
| **ponytail-audit** | `/ponytail-audit` | Whole-repo ranked list of what to cut. |
| **ponytail-debt** | `/ponytail-debt` | Harvest `ponytail:` comments into a debt ledger. |
| **ponytail-gain** | `/ponytail-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **ponytail-help** | `/ponytail-help` | This card. |

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `/ponytail`.
`/ponytail off` also works.

## Configure default mode

Default = `full`. Change it:

```bash
export PONYTAIL_DEFAULT_MODE=ultra   # env var (highest priority)
```

Or `~/.config/ponytail/config.json`:

```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation; activate manually with `/ponytail`.

## More

Full docs + examples: https://github.com/DietrichGebert/ponytail
