# Suite Map

PaperSpine is split into task-focused skills:

| Skill | Responsibility |
|---|---|
| `paper-spine` | route the workflow |
| `paper-spine-ui` | launch external terminal configuration UI |
| `paper-spine-intake` | collect configuration |
| `paper-spine-research` | index local references, research target scene, and learn examples |
| `paper-spine-citation` | build citation support candidates |
| `paper-spine-rewrite` | rewrite an existing draft |
| `paper-spine-build` | build from a materials folder |
| `paper-spine-latex` | assemble and guard LaTeX |
| `paper-spine-translate` | produce complete translation_zh/ with row-by-row translation |
| `paper-spine-audit` | check completeness, integrity audit, structured review, and translation coverage |
| `paper-spine-update` | check and update local PaperSpine installs |

Use the orchestrator for end-to-end tasks. Use a child skill directly when the
user asks for that stage only.

## Script Resolution

When a child skill references `scripts/...`, use that child skill's local script
first. If the file is absent, resolve shared guards from `paper-spine/scripts/`
and branch-specific guards from the owning child skill. Examples:
`template_leak_guard.py`, `integrity_audit.py`, `structured_review.py`, and the
suite compatibility `word_guard.py` live under `paper-spine/scripts/`;
`translate_guard.py` lives under `paper-spine-translate/scripts/`;
`citation_quality_audit.py` lives under `paper-spine-citation/scripts/`;
`revision_audit.py` lives under `paper-spine-audit/scripts/`.
