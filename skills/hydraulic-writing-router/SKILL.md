---
name: hydraulic-writing-router
description: Personal top-level router for water-related writing. Use when the request explicitly concerns water-conservancy, hydrology, hydraulic engineering, rivers, drainage, water resources, water environment/governance, Chinese water coursework, course reports/designs, engineering reports, or LaTeX/PDF water deliverables; Chinese triggers include 水利, 水文, 水资源, 水工, 河流, 排水, 城市内涝, 水环境, 水治理, 课程报告, 课程设计, 工程报告. Also use when the user asks to coordinate PaperSpine and Nature for water-related writing. Do not use for generic non-water academic writing unless the materials contain a water/hydraulic object.
---

# Hydraulic Writing Router

Personal entrypoint for water-related papers, reports, coursework, and LaTeX/PDF-first deliverables. It decides ownership first, then loads only the downstream skill files needed for the task.

## Live-Read Rule

When invoked, read this active `SKILL.md` from disk first. Do not work from memory, old chat, backups, or archived copies.

Load downstream files only as needed:

- `paper-spine/SKILL.md`: sources, task books, templates, structure, calculations, tables, references, report repair, full/medium workflow, or final writing deliverables. Content-stage report drafts may be written and reviewed in Markdown for speed; final delivery source is assembled in LaTeX. PaperSpine keeps `final_paper/main.tex` as the final source artifact; PDF is default when compilable.
- `nature-writing/SKILL.md`: drafting or rebuilding sections from confirmed materials and chapter duties. For Chinese water course reports, course designs, engineering reports, and full report builds, load it after PaperSpine has closed source roles, chapter duties, calculation boundaries, and required tables; Nature writing owns the report body prose.
- `nature-polishing/SKILL.md`, then its `manifest.yaml` and `always_load`: polish, paragraph logic, Chinese report voice, expression density, or anti-AI regularity. For full water reports, run it after Nature writing and before final LaTeX/PDF assembly unless the user explicitly asks for a mechanical formatting-only task.
- `nature-polishing/static/core/hydraulic-engineering.md`: water-domain guardrail for drafting, polishing, and audit. Load it when the task needs object/scale checks, formula chains, parameter basis, scenario boundaries, table/figure evidence, engineering judgment, or Chinese hydraulic-report voice. This file is installed as an on-demand resource; do not rely on Nature `always_load` to bring it in.
- `paper-spine-latex/SKILL.md`: final LaTeX project assembly, source-format requirements, template integration, figure/table/equation/citation placement, compile checks, and PDF output. For water reports, use only its LaTeX/PDF rules and ignore optional conversion-to-other-format instructions.

Default water-writing deliverables keep LaTeX source as the PaperSpine final
artifact and compile PDF when a TeX engine is available. Reuse the existing
PaperSpine/Nature LaTeX rules before adding new local rules. During content
development, review Markdown or source text directly; do not run generic
document rendering, LibreOffice/soffice rendering, or format-conversion output
just to inspect whether the report content is good.
This is an output-stage preference, not a replacement for the original workflow:
PaperSpine still owns source mapping, chapter duties, audits, calculations,
template constraints, and final artifact verification. Nature writing and
Nature polishing own the report body prose after the content boundary is
stable; for full water course reports and engineering reports, this Nature
content pass is required before final artifact assembly unless the task is
explicitly mechanical. The reason for preferring direct LaTeX-to-PDF in
water reports is to reduce formatting drift and avoid a fragile final conversion
step.
The water workflow is a division-of-labor layer over Nature and PaperSpine, not
a fork of them. Do not override their original intent: for writing deliverables,
PaperSpine's final source artifact remains `final_paper/main.tex`.

## Water Output Gate

Apply this gate as a routing and completion check for water-report tasks. Do not
patch Nature or PaperSpine core skill files just to enforce this preference.

- Content review artifact: Markdown is acceptable and preferred for fast review before final formatting.
- Content review rule: do not convert to another document format just to inspect whether the writing is complete or correct.
- Confirmed content artifact: after the user confirms the report content, save or mark the confirmed Markdown as `confirmed_content.md`. Final LaTeX assembly must use this file as the content source of truth.
- Final source artifact: `paper_rewriting_output/final_paper/main.tex`.
- Final compiled artifact when possible: `paper_rewriting_output/final_paper/paper.pdf`.
- Final assembly rule: after the user confirms the content, assemble `confirmed_content.md` into LaTeX, use native `\tableofcontents`, run the LaTeX guard when available, and compile PDF when a TeX engine exists.
- Cover rule: defer native school cover integration until after content confirmation. Ask the user to upload the cover image/PDF or provide the exact file path when final formatting begins. Do not hand-imitate a cover from memory.
- Do not call the generic Documents render workflow or LibreOffice/soffice for Chinese water-report content review or final rendering.

## Routing Table

| Request signal | Owner | Rule |
|---|---|---|
| One sentence, one paragraph, narrow wording | Nature polishing | Use hydraulic core if water-related; verify affected facts only. |
| Draft or rebuild a section | Nature writing | Use only after object, evidence, and section duty are clear. |
| Section polish with stable structure | PaperSpine light check -> Nature polishing | Confirm duty/data boundary first, then polish. |
| Calculation, table, parameter, template, reference, LaTeX/PDF, figure/CAD issue | PaperSpine report repair | Do not smooth prose before the defect is closed. |
| Full report/paper/course design, many sections, structure rebuild, deliverable package | PaperSpine workflow + Nature content ownership | PaperSpine closes sources, calculations, template constraints, and artifact verification; Nature writing drafts/rebuilds body prose and Nature polishing finalizes paragraph logic and Chinese report voice before delivery. |

## Boundary Rules

- PaperSpine owns workflow, source mapping, task-book/template constraints, chapter duties, calculation/table closure, citation/evidence planning, report repair, full builds, the final LaTeX source artifact, and artifact verification. It does not own the final body prose once the content boundary is stable.
- Nature writing owns prose drafting or rebuilding after materials, calculation boundaries, and chapter duties are confirmed. In full Chinese water course reports, course designs, and engineering reports, Nature writing must draft or rebuild the body sections rather than leaving body prose to PaperSpine or ad hoc script text.
- Nature polishing owns paragraph logic, clarity, rhythm, expression density, and natural Chinese coursework voice after content is stable. In full water reports, this polish pass runs before final LaTeX/PDF assembly unless the user explicitly asks for formatting only.
- Hydraulic core owns object/scale, data source, formula chain, parameter basis, scenario boundary, table/figure evidence, engineering judgment, and consistency by same object + same stage + same basis.
- Teacher instructions, task books, official templates, and user drafts outrank generic Nature style.
- If a source document provides formatting requirements, record those requirements during content work, but apply them only during final LaTeX/PDF assembly after content confirmation. Do not infer another output route from a template file extension alone.
- When a report request includes task books, guidance files, group tables,
  official templates, and another person's report/template/sample, route to
  PaperSpine source mapping first. Classify each file as requirement source,
  user evidence source, structure-only exemplar, reference source, or
  unknown/unsafe source. Structure-only exemplars may teach chapter order,
  calculation sequence, table/formula placement, and formatting habits, but
  they must not supply final data, formulas, parameters, wording, conclusions,
  or recommendations.

## Failure Modes

Treat these as defects:

- Starting work without reading the active `SKILL.md`.
- Triggering this router for generic non-water writing with no water/hydraulic object.
- Running full PaperSpine for a small local wording patch.
- Treating missing calculation/source/template evidence as a polish problem.
- Skipping Nature writing/polishing on a full Chinese water course report after the calculations and chapter duties are stable.
- Letting Nature style override a course task book, teacher template, or user data.
- Treating a content-review Markdown draft as final delivery.
- Starting final LaTeX assembly before `confirmed_content.md` exists or before the user has confirmed it.
- Running format conversion repeatedly to inspect content quality.
- Delivering any full report after final assembly without `final_paper/main.tex`.
- Treating converted documents or LibreOffice output as the final report source.
- Hand-imitating a cover or TOC when an official template or real field exists.
- Hand-typing a LaTeX/PDF table of contents instead of using native `\tableofcontents`.
- Converting the report to another format before the user confirms the content.
- Triggering generic Documents rendering, LibreOffice, or any non-LaTeX final-output tool only because a template file was present.
- Reporting completion without artifact, encoding, or calculation verification when the task edited files or numbers.

## Completion Gate

- Markdown/config: UTF-8 readback, no replacement characters.
- Content review: inspect the Markdown/source text directly and confirm chapter logic, calculations, tables, conclusions, and missing inputs before final formatting. Once confirmed, create or mark `confirmed_content.md`.
- LaTeX/PDF: after `confirmed_content.md` exists, inspect `final_paper/main.tex`, require a native `\tableofcontents` when a table of contents is needed, run the LaTeX guard when available, compile PDF when a TeX engine exists, and confirm source-format requirements from the materials are reflected or explicitly recorded as unmappable.
- PPT/Excel/PDF: inspect the actual artifact structure, not just file existence.
- Calculations/tables: recompute when numbers support conclusions.
- Water decisions: keep `formula -> substitution -> result -> design judgment` visible when a calculation drives the judgment.
