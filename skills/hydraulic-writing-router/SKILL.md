---
name: hydraulic-writing-router
description: Personal top-level router for the user's water-conservancy, hydrology, hydraulic engineering, river, drainage, water-resource, water-environment, and Chinese coursework paper/report writing. Use when the user asks to write, polish, repair, audit, format, or build water-related papers, course reports, course designs, engineering reports, Word/PDF deliverables, or when the user wants PaperSpine and Nature writing skills coordinated with clear boundaries.
---

# Hydraulic Writing Router

This is the user's personal entrypoint for water-related academic and coursework writing. It coordinates PaperSpine, Nature writing/polishing, the hydraulic core, and document tools without letting them compete for ownership.

## Mandatory Live-Read Rule

When this skill is invoked, do not work from memory. First read this `SKILL.md` from disk, then read only the active downstream skill files needed for the task:

- `C:\Users\26632\.codex\skills\paper-spine\SKILL.md` when the task involves source mapping, report structure, calculations, tables, references, full/medium workflow, file repair, or final deliverables.
- `C:\Users\26632\.codex\skills\nature-polishing\SKILL.md` plus its `manifest.yaml` and `always_load` files when the task involves prose polishing, paragraph logic, academic clarity, Chinese report voice, or anti-AI expression.
- `C:\Users\26632\.codex\skills\nature-writing\SKILL.md` when the task asks to draft or rebuild sections before polish.
- `C:\Users\26632\.codex\skills\docx-editor-cn\SKILL.md` or the document plugin when the task edits Word files.

Do not rely on cached memory, previous chat behavior, or inactive duplicate skill copies. Memory can remind you that a rule exists; the active file on disk is the rule source.

## Boundary Contract

Use this ownership split:

- PaperSpine owns workflow classification, task-book/template reading, source mapping, chapter duties, calculation/table closure, citation/evidence planning, report repair, full manuscript/report builds, and final artifact verification.
- Nature writing owns drafting or rebuilding prose from confirmed materials and chapter duties.
- Nature polishing owns paragraph logic, academic clarity, sentence rhythm, water-engineering expression density, and Chinese coursework naturalness after the content gate is stable.
- The hydraulic core owns domain checks: object/scale, data source, formula chain, parameter basis, scenario boundary, table/figure evidence, engineering judgment, and consistency by same object plus same stage plus same calculation basis.
- Word/document tools own `.docx` structure, template preservation, styles, headings, real TOC fields, tables, equations, and file-level verification.

If a polish request exposes missing calculations, unsupported parameters, template conflict, broken table logic, or uncertain source data, pause the prose polish and route back to PaperSpine report-repair. Do not smooth over a content defect.

## Routing

Choose the smallest sufficient path:

1. Small wording or one-paragraph patch: use Nature polishing with the hydraulic core if water-related; verify only affected facts and files.
2. Section polish: use PaperSpine only to confirm section duty and data boundary, then Nature polishing for expression.
3. Report repair: use PaperSpine as owner; call Nature polishing only after calculations, sources, and template issues are stable.
4. Full paper/report/course-design build: PaperSpine is the owner from intake/source map to audit; Nature writing/polishing are branch passes, not workflow owners.

For Chinese water-coursework deliverables, teacher instructions, task books, official templates, and user-provided drafts outrank generic Nature style. Nature raises clarity and density; it must not invent data, citations, or a journal-style structure that conflicts with the course requirement.

## Conflict Handling

Instruction priority is:

1. System/developer instructions.
2. User's current request and local `AGENTS.md`.
3. This router.
4. Active downstream skill files opened from disk.
5. Memory and prior chat summaries.

When a downstream skill asks for behavior blocked by a higher-level rule, follow the higher-level rule and state the conflict briefly. In this environment, do not spawn subagents unless the user explicitly asks for subagents, delegation, or parallel agent work.

## Completion Gate

Before reporting completion on any edited file, run a real verification appropriate to the artifact:

- Markdown/config: UTF-8 readback and no replacement characters.
- Word/PPT/Excel/PDF: reopen or inspect the actual artifact structure, not only file existence.
- Calculations/tables: deterministic recomputation when numbers support a conclusion.
- Water writing: check `formula -> substitution -> result -> design judgment` when a calculation drives a decision.
