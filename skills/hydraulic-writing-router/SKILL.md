---
name: hydraulic-writing-router
description: Personal top-level router for water-related writing. Use when the request explicitly concerns water-conservancy, hydrology, hydraulic engineering, rivers, drainage, water resources, water environment/governance, Chinese water coursework, course reports/designs, engineering reports, or water-related Word/PDF deliverables; Chinese triggers include 水利, 水文, 水资源, 水工, 河流, 排水, 城市内涝, 水环境, 水治理, 课程报告, 课程设计, 工程报告. Also use when the user asks to coordinate PaperSpine and Nature for water-related writing. Do not use for generic non-water academic writing unless the materials contain a water/hydraulic object.
---

# Hydraulic Writing Router

Personal entrypoint for water-related papers, reports, coursework, and Word/PDF deliverables. It decides ownership first, then loads only the downstream skill files needed for the task.

## Live-Read Rule

When invoked, read this active `SKILL.md` from disk first. Do not work from memory, old chat, backups, or archived copies.

Load downstream files only as needed:

- `paper-spine/SKILL.md`: sources, task books, templates, structure, calculations, tables, references, report repair, full/medium workflow, or final writing deliverables. PaperSpine keeps `final_paper/main.tex` as the source artifact; PDF is default when compilable, and Word is added only when explicitly required.
- `nature-writing/SKILL.md`: drafting or rebuilding sections from confirmed materials and chapter duties. For Chinese water course reports, course designs, engineering reports, and full report builds, load it after PaperSpine has closed source roles, chapter duties, calculation boundaries, and required tables; Nature writing owns the report body prose.
- `nature-polishing/SKILL.md`, then its `manifest.yaml` and `always_load`: polish, paragraph logic, Chinese report voice, expression density, or anti-AI regularity. For full water reports, run it after Nature writing and before final Word/PDF/LaTeX assembly unless the user explicitly asks for a mechanical formatting-only task.
- `paper-spine-latex/SKILL.md`: final LaTeX project assembly, source-format requirements, template integration, figure/table/equation/citation placement, compile checks, and PDF output.
- `docx-editor-cn/SKILL.md` or document tools: only when the user explicitly requests `.docx` or the submission requirement forces Word output. Use it for `.docx` templates, styles, headings, TOC fields, tables, equations, and file verification.
  For Chinese school/course/engineering Word templates, prefer `docx-editor-cn`
  over the generic Documents render workflow.

Default water-writing deliverables keep LaTeX source as the PaperSpine final
artifact and compile PDF when a TeX engine is available. Reuse the existing
PaperSpine/Nature LaTeX rules before adding new local rules. Do not run a final
LaTeX-to-Word conversion unless the user explicitly asks for `.docx` or the
requirement source makes `.docx` mandatory.

This is an output-stage preference, not a replacement for the original workflow:
PaperSpine still owns source mapping, chapter duties, audits, calculations,
template constraints, and final artifact verification. Nature writing and
Nature polishing own the report body prose after the content boundary is
stable; for full water course reports and engineering reports, this Nature
content pass is required before final artifact assembly unless the task is
explicitly mechanical. The reason for preferring direct LaTeX-to-PDF in water
reports is to reduce formatting drift and avoid a fragile final conversion step.

The water workflow is a division-of-labor layer over Nature and PaperSpine, not
a fork of them. Do not override their original intent: for writing deliverables,
PaperSpine's final source artifact remains `final_paper/main.tex`; Word is an
explicit or requirement-driven companion artifact, not the default endpoint.

## Routing Table

| Request signal | Owner | Rule |
|---|---|---|
| One sentence, one paragraph, narrow wording | Nature polishing | Use hydraulic core if water-related; verify affected facts only. |
| Draft or rebuild a section | Nature writing | Use only after object, evidence, and section duty are clear. |
| Section polish with stable structure | PaperSpine light check -> Nature polishing | Confirm duty/data boundary first, then polish. |
| Calculation, table, parameter, template, reference, LaTeX/PDF/Word, figure/CAD issue | PaperSpine report repair | Do not smooth prose before the defect is closed. |
| Full report/paper/course design, many sections, structure rebuild, deliverable package | PaperSpine workflow + Nature content ownership | PaperSpine closes sources, calculations, template constraints, and artifact verification; Nature writing drafts/rebuilds body prose and Nature polishing finalizes paragraph logic and Chinese report voice before delivery. |

## Boundary Rules

- PaperSpine owns workflow, source mapping, task-book/template constraints, chapter duties, calculation/table closure, citation/evidence planning, report repair, full builds, the final LaTeX source artifact, and artifact verification. It does not own the final body prose once the content boundary is stable. When `.docx` is explicitly required, Word is an additional branch owned by `docx-editor-cn`, not a replacement for `final_paper/main.tex`.
- Nature writing owns prose drafting or rebuilding after materials, calculation boundaries, and chapter duties are confirmed. In full Chinese water course reports, course designs, and engineering reports, Nature writing must draft or rebuild the body sections rather than leaving body prose to PaperSpine or ad hoc script text.
- Nature polishing owns paragraph logic, clarity, rhythm, expression density, and natural Chinese coursework voice after content is stable. In full water reports, this polish pass runs before final Word/PDF/LaTeX assembly unless the user explicitly asks for formatting only.
- Hydraulic core owns object/scale, data source, formula chain, parameter basis, scenario boundary, table/figure evidence, engineering judgment, and consistency by same object + same stage + same basis.
- Teacher instructions, task books, official templates, and user drafts outrank generic Nature style.
- If the visible submission path is LaTeX/PDF and a source document provides formatting requirements, convert those requirements into the PaperSpine LaTeX format contract and follow it in `final_paper/main.tex`. If `.docx` is mandatory, also use the Word format contract owned by `docx-editor-cn` while keeping `final_paper/main.tex` as the PaperSpine source artifact.
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
- Hand-imitating a Word cover or TOC when an official template or real field exists.
- Converting a LaTeX-first water report to Word at the end when neither the user nor the requirement source asked for `.docx`.
- Reporting completion without artifact, encoding, or calculation verification when the task edited files or numbers.
- Routing Chinese official-template `.docx` verification through automated
  rendering instead of `docx-editor-cn` structural guards.

## Completion Gate

- Markdown/config: UTF-8 readback, no replacement characters.
- LaTeX/PDF: inspect `final_paper/main.tex`, run the LaTeX guard when available, compile PDF when a TeX engine exists, and confirm source-format requirements from the materials are reflected or explicitly recorded as unmappable.
- Word/PPT/Excel/PDF: inspect the actual artifact structure, not just file existence.
  For Chinese `.docx` templates, require `docx-editor-cn` structural checks;
  use Microsoft Word or WPS outside the automated path when visual opening/export
  is required.
- Calculations/tables: recompute when numbers support conclusions.
- Water decisions: keep `formula -> substitution -> result -> design judgment` visible when a calculation drives the judgment.
