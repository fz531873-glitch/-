# LaTeX-First Course Design Workflow

This example documents the expected workflow for Chinese hydraulic course
design reports when the user wants a stable LaTeX source first and does not ask
for Word output.

## Goal

Produce a complete water-engineering course design report with:

- PaperSpine controlling source roles, task requirements, calculation
  boundaries, chapter duties, format constraints, and artifact verification.
- Nature writing controlling the report body prose after the content boundary
  is stable.
- Nature polishing controlling paragraph logic and Chinese coursework voice.
- `final_paper/main.tex` as the final source artifact.
- PDF only as a compile/check artifact when a TeX engine is available.
- Word only when explicitly requested or required by the task source.

## Source Intake

Classify every local file before writing:

| Source type | Examples | How to use |
|---|---|---|
| Requirement source | task book, guidance file, grading rubric | Required chapters, deliverables, formulas, calculation cases, formatting rules |
| User evidence source | student number, group table, measurements, confirmed data | Final facts, numbers, tables, calculations, conclusions |
| Format source | school cover, report-writing format, template | LaTeX cover fields, TOC, headings, captions, page style |
| Reference source | standards, manuals, textbooks | Method basis, parameter boundary, engineering judgement |
| Structure-only exemplar | another student's report, sample report | Chapter order and table rhythm only; never facts or wording |

## Required PaperSpine Artifacts

Create or verify these before drafting:

- `paper_rewriting_output/source_inventory.md`
- `paper_rewriting_output/calculation_boundary.md`
- `paper_rewriting_output/evidence_bank.md`
- `paper_rewriting_output/section_blueprints.md`
- `paper_rewriting_output/writing_rationale_matrix.md`
- `paper_rewriting_output/latex_report.md`
- `paper_rewriting_output/final_artifact_manifest.md`

## Content Pass

Use Nature writing only after PaperSpine has closed:

- source roles;
- chapter duties;
- calculation boundaries;
- required tables;
- formula and parameter bases;
- missing-input notes.

For each body section, write from evidence outward:

1. State the local engineering problem.
2. Give the method or formula.
3. Substitute the project-specific values.
4. Report the result.
5. State the design judgement and boundary.

Important calculations should visibly follow:

```text
formula -> substitution -> result -> design judgement
```

## LaTeX Assembly

Convert format requirements into LaTeX:

- cover fields become a `titlepage`;
- table of contents uses native `\tableofcontents`;
- chapters and sections follow the school hierarchy;
- equations, tables, and figures use native numbering;
- headers and page numbers follow the format contract;
- references are written in a consistent Chinese standard style.

Compile PDF when possible. If compilation is unavailable or fails, keep
`final_paper/main.tex`, record the reason, and do not claim the PDF check
passes.

## Completion Checks

Before delivery:

- read `main.tex` as UTF-8;
- search for leftover placeholders such as `@@` or template prompts;
- search for mojibake and replacement characters;
- recompute key values that support conclusions;
- compile PDF when possible;
- extract or inspect PDF text for cover, TOC, headings, and key values;
- record all final artifacts in `final_artifact_manifest.md`.

## Non-goals

- Do not upload or publish task books, private templates, student reports, or
  generated course-design answers as part of this core workflow package.
- Do not convert LaTeX to Word unless Word output is explicitly requested or
  required by the source materials.
