---
name: hydraulic-writing-router
description: Personal top-level router for water-related writing. Use when the request explicitly concerns water-conservancy, hydrology, hydraulic engineering, rivers, drainage, water resources, water environment/governance, Chinese water coursework, course reports/designs, engineering reports, or water-related Word/PDF deliverables; Chinese triggers include 水利, 水文, 水资源, 水工, 河流, 排水, 城市内涝, 水环境, 水治理, 课程报告, 课程设计, 工程报告. Also use when the user asks to coordinate PaperSpine and Nature for water-related writing. Do not use for generic non-water academic writing unless the materials contain a water/hydraulic object.
---

# Hydraulic Writing Router

Personal entrypoint for water-related papers, reports, coursework, and Word/PDF deliverables. It decides ownership first, then loads only the downstream skill files needed for the task.

## Live-Read Rule

When invoked, read this active `SKILL.md` from disk first. Do not work from memory, old chat, backups, or archived copies.

Load downstream files only as needed:

- `paper-spine/SKILL.md`: sources, task books, templates, structure, calculations, tables, references, report repair, full/medium workflow, or final deliverables.
- `nature-writing/SKILL.md`: drafting or rebuilding sections from confirmed materials and chapter duties.
- `nature-polishing/SKILL.md`, then its `manifest.yaml` and `always_load`: polish, paragraph logic, Chinese report voice, expression density, or anti-AI regularity.
- `docx-editor-cn/SKILL.md` or document tools: `.docx` templates, styles, headings, TOC fields, tables, equations, and file verification.

## Routing Table

| Request signal | Owner | Rule |
|---|---|---|
| One sentence, one paragraph, narrow wording | Nature polishing | Use hydraulic core if water-related; verify affected facts only. |
| Draft or rebuild a section | Nature writing | Use only after object, evidence, and section duty are clear. |
| Section polish with stable structure | PaperSpine light check -> Nature polishing | Confirm duty/data boundary first, then polish. |
| Calculation, table, parameter, template, reference, Word/PDF, figure/CAD issue | PaperSpine report repair | Do not smooth prose before the defect is closed. |
| Full report/paper/course design, many sections, structure rebuild, deliverable package | PaperSpine full workflow | Nature writing/polishing are branch passes, not workflow owners. |

## Boundary Rules

- PaperSpine owns workflow, source mapping, task-book/template constraints, chapter duties, calculation/table closure, citation/evidence planning, report repair, full builds, and artifact verification.
- Nature writing owns prose drafting or rebuilding after materials and chapter duties are confirmed.
- Nature polishing owns paragraph logic, clarity, rhythm, expression density, and natural Chinese coursework voice after content is stable.
- Hydraulic core owns object/scale, data source, formula chain, parameter basis, scenario boundary, table/figure evidence, engineering judgment, and consistency by same object + same stage + same basis.
- Teacher instructions, task books, official templates, and user drafts outrank generic Nature style.

## Failure Modes

Treat these as defects:

- Starting work without reading the active `SKILL.md`.
- Triggering this router for generic non-water writing with no water/hydraulic object.
- Running full PaperSpine for a small local wording patch.
- Treating missing calculation/source/template evidence as a polish problem.
- Letting Nature style override a course task book, teacher template, or user data.
- Hand-imitating a Word cover or TOC when an official template or real field exists.
- Reporting completion without artifact, encoding, or calculation verification when the task edited files or numbers.

## Completion Gate

- Markdown/config: UTF-8 readback, no replacement characters.
- Word/PPT/Excel/PDF: inspect the actual artifact structure, not just file existence.
- Calculations/tables: recompute when numbers support conclusions.
- Water decisions: keep `formula -> substitution -> result -> design judgment` visible when a calculation drives the judgment.
