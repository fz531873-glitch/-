---
name: paper-spine-build
description: Builds a paper or report from materials using the shared PaperSpine research, motivation, and rationale workflow. (internal /paperspine step)
---

# PaperSpine Build From Materials

Use this skill when the user does not have a real manuscript draft yet and
instead provides a materials folder with experiment settings, results, figures,
notes, PDFs, Word files, TXT/Markdown reports, or partial drafts.

This workflow shares the same research, motivation confirmation, evidence bank,
section blueprint, and writing rationale matrix logic as `paper-spine-rewrite`.
It is not a separate shortcut.

## Required Inputs

- `paper_rewriting_output/paper_spine_config.json`
- `materials_dir`
- target scene and output language
- `paper_rewriting_output/reference_materials/source_index.md`
- `paper_rewriting_output/research_dossier.md`
- `paper_rewriting_output/exemplar_learning_dossier.md`
- `paper_rewriting_output/style_profile.md`
- `paper_rewriting_output/sota_gap_map.md`
- `paper_rewriting_output/citation_support_bank.md`
- `paper_rewriting_output/confirmed_motivation.md` with user confirmation

If research or confirmed motivation is missing, do not draft. Return to
`paper-spine-research` and ask the user to confirm the motivation after seeing
research-grounded options.

If `citation_support_bank.md` is missing or shallow, return to
`paper-spine-citation`. From-zero writing still needs literature support for
background, Introduction/overview, Discussion, limitations, and applications.

## First Pass

Run or emulate:

```bash
python scripts/material_inventory.py <materials_dir> --output-dir paper_rewriting_output
```

Create `source_inventory.md` before making claims.

## Required Outputs

- `paper_rewriting_output/source_inventory.md`
- `paper_rewriting_output/evidence_bank.md`
- `paper_rewriting_output/figure_asset_map.md`
- `paper_rewriting_output/claim_register.md`
- `paper_rewriting_output/section_blueprints.md`
- `paper_rewriting_output/writing_rationale_matrix.md`
- manuscript draft as an intermediate artifact
- `paper_rewriting_output/final_paper/main.tex`
- `paper_rewriting_output/final_paper/paper.pdf` when a TeX engine is available
- `paper_rewriting_output/latex_report.md`
- `paper_rewriting_output/final_artifact_manifest.md`
- `paper_rewriting_output/translation_zh/` when `translation_package` is `zh` (via `paper-spine-translate`)

## Writing Rationale Matrix

Before final prose, create `writing_rationale_matrix.md` and read
`references/writing-rationale-matrix.md`. The matrix is the build plan. It must
be ordered by the target document's actual writing units, not by a fixed paper
template.

Use this table:

| Row ID | Manuscript Unit | Planned Function | Motivation Link | Reference/SOTA Pattern Learned | Target Scene or Venue Norm | User Evidence or Citation Anchor | Planned Text Move | Final Text Check |
|---|---|---|---|---|---|---|---|---|

The first data row must deeply justify the whole-work framework or throughline:
why this controlling structure is chosen, how SOTA/target examples informed it,
how it follows the confirmed motivation, which user evidence anchors it, and how
the final manuscript/report will be checked against it. After that, split the
work into the smallest useful units for the selected scene:
abstract/summary moves, problem restatement, assumptions, model design, methods
choices, result/claim units, review synthesis blocks, validation blocks,
recommendations, headings, captions, or other argument-bearing fragments.

No row may be generic. Each row must state why that unit exists and how it is
connected to the confirmed motivation, learned examples, target-scene norms, or
user evidence. If a paragraph or figure claim needs a separate writing decision,
it needs its own row.

## Natural Voice Tier

If `paper_spine_config.json` has `humanize_tier` set to `light`, `medium`, or
`heavy`, keep the build inside PaperSpine and apply `nature-polishing` after the
content, calculation, evidence, and template gates are stable. Nature polishing
owns Chinese naturalness, anti-AI regularity checks, paragraph rhythm, and
expression density. Do not route to a separate naturalization skill.

## Report And Hydraulic Build Gate

If the target is a Chinese report, course report, course design, design report,
engineering report, water/hydraulic report, or the config/user request contains
`课程报告`, `课程设计`, `课程论文`, `设计报告`, `本科作业`, `工程报告`, `水利`, `水文`, `水资源`, or
`水工`, keep the build inside PaperSpine. Do not call a separate
course-report skill.

In that mode, do not treat the report plan as a visible outline. Create a
chapter-duty or writing-rationale matrix before drafting. Each row must specify:

- question to be answered;
- required basis, such as task-book data, formula, code/standard basis,
  literature support, engineering analogy, or labelled course-design assumption;
- calculation, table, or data link;
- final-text gate that prevents planning language from entering the body.

The rationale matrix must encode the report as duties rather than writing
order: problem/object definition, local data and risk, method or calculation
path, table/figure evidence, result interpretation, scheme or management
decision, parameter/source boundary, and bounded verification. Background stays
short; data, methods, tables, results, decision logic, and quality control get
the most detail.

For water-conservancy and hydraulic topics, apply the hydraulic core from Nature
polishing/writing as the general domain guardrail: data-source trace, table
calculation trace, parameter/source boundaries, scenario and scale clarity,
data-scope consistency, table/figure evidence closure, and Word/PDF artifact
verification. Object-specific checks apply only when the current materials
contain that object.

If `materials_dir`, `reference_paths`, or the user message provides a local
folder of water-conservancy papers, build the draft against that corpus. Before
drafting, `style_profile.md` and `exemplar_learning_dossier.md` must summarize
what was learned from multiple papers: section order, paragraph rhythm,
method/result wording, table/figure explanation, engineering-use statements,
conclusion style, and reference pattern. Use those patterns to shape the final
output without copying wording or importing unsupported claims.

For the user's `论文搭建` corpus, the build should emphasize normative
expression: name the object early, connect pressure to method, make the method
or index/model path reproducible, report results as grade/range/distribution/
trend or scenario difference, and close with engineering use plus boundary.

Final prose for this mode must pass a body admission test: each paragraph should
name a real object, method, dataset, water level, elevation, layer, structure,
figure, table, or maintenance object, and also provide a basis, consequence, or
boundary. Do not place sentences such as `本报告先...`, `后文按照...展开`,
`论证重点转向...`, or `避免把...处理成...` in the final report body. Keep those only in
planning artifacts.

Tables and parameters must also be traceable. For any table that affects a
design, evaluation, management, or report conclusion, include a matrix row or
evidence-bank entry for its data source, formula or scoring rule,
substitution/calculation process, and consequence. Do not let weights, scores,
thresholds, water levels, discharges, rainfall/runoff values, storage,
pollutant loads, risk grades, or key parameters appear only inside a table
without prose explanation.

For Chinese water-engineering reports, the matrix and final artifact must
include these general checks as separate rows or audit items:

- arithmetic: recompute important scheme scores, indexes, water quantities, or
  table values from stated data and formulas, then synchronize tables, formula
  expansions, prose, and conclusions;
- calculation deduplication: avoid repeating the same calculation in multiple
  chapters; later chapters should state the consequence of the earlier result;
- template completion: flag blank required cover, identity, date, or submission
  fields as missing user input;
- data-scope closure: lock the same object under the same stage, period,
  scenario, datum, and calculation basis. Valid differences must be labelled by
  object or basis;
- parameter boundary: important parameters must name data source, code/formula,
  literature, course/report assumption, engineering analogy, or later
  verification input;
- reference and heading normalization: use standard engineering headings and one
  consistent reference style.
Before final output, run a report gap-closure pass:

- calculation presentation: for each calculation that affects a design decision or conclusion, show formula, substitution, result and design judgment. Repeated formulas may be fully shown once and referenced later, but table values must still be recomputed and checked;
- formatting contract: follow user-provided font, table, heading, caption, margin, reference and equation requirements exactly. If the user has not specified a visible formatting rule, preserve the source/template style rather than inventing a new one;
- Word equation rendering: important formulas in `.docx` outputs should be standalone native Word equations generated from LaTeX/OMML. Plain text formulas are acceptable only as a marked fallback when equation rendering is unavailable;

- precision: ambiguous terms must be labelled by basis, datum, scenario, object,
  time period, or formula;
- formula basis: preliminary values, thresholds, scores, model parameters, and
  engineering parameters must state the intended formula/code/criterion or the
  missing inputs for later verification;
- scheme comparison: weight basis, scoring scale, weighted-score formula and at
  least one worked substitution must appear in the comparison section;
- data closure: recompute weighted scores, index values, or water quantities
  from the stated data and formulas; after any numeric change, search the whole
  final artifact so old values do not remain in text, parameter tables, figures,
  notes, conclusions, or verification lists;
- artifact verification: when a Word/PDF output is generated, verify the actual
  file exists and parses/opens, old values are absent, new values occur in the
  expected places, and obvious encoding damage such as `????` is absent;
- conclusion discipline: fixable gaps must be repaired in their local chapters,
  not left as future-work confessions in the conclusion.

## Build Rules

- `materials_dir` and the output path may contain spaces or non-ASCII characters
  (e.g. `exp_lab_en - 副本`). Always quote paths and avoid shell globbing such as
  `cp materials/* ...`; copy or read files with explicitly quoted paths, prefer
  Python `pathlib` or (on Windows) PowerShell for file operations. Unquoted
  globs silently break on such directories.
- Treat images as potential figure assets, not as verified evidence unless the
  user explains what they show.
- Use existing document/PDF skills for complex PDF, DOCX, or scanned material
  extraction when available.
- Do not fabricate missing experiments or results.
- Copy user-approved figure assets into the final LaTeX project's `figures/`
  folder and reference them with labels and captions.
- Follow `output_language`: `en` or `zh`.
- Use `citation_support_bank.md` to select citations sentence by sentence; do
  not treat citation candidates as user evidence or insert all candidates.
- Before routing through `paper-spine-latex`, run `python scripts/integrity_audit.py paper_rewriting_output --markdown --write` and `python scripts/structured_review.py paper_rewriting_output --dispatch`. After dispatch, launch three parallel review sub-agents per `review_prompts/dispatch.md`, then validate independence. Only proceed when all dimensions PASS.
- Always finish by routing through `paper-spine-latex`. A Markdown draft is not
  a final deliverable for this workflow.
- Build the final LaTeX project under `paper_rewriting_output/final_paper/`.
- If `word_output` is `docx`, generate `final_paper/paper.docx` and run
  `scripts/word_guard.py`, saving `paper_rewriting_output/word_report.md`.
- If `output_language` is `en` and `translation_package` is `zh`, create a full
  `paper_rewriting_output/translation_zh/` package. This includes complete
  row-by-row translation of large intermediate files such as
  `writing_rationale_matrix.md`; partial translation or summary translation is
  a failure.

Read `references/build-from-materials.md` and
`references/writing-rationale-matrix.md` before building the manuscript.
