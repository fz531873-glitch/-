---
name: paper-spine
description: Main PaperSpine dispatcher for papers, reports, coursework, course designs, engineering reports, and water/hydraulic writing. Use when Codex needs to decide whether a request is a local edit, section polish, report repair, or full paper/report build. Choose the smallest sufficient lane, delegate drafting/polishing to Nature skills and Word work to document skills, optionally route light lanes to lower-cost models such as gpt-5.4 when the host supports model overrides, and run the full PaperSpine research-writing workflow only for substantial builds or rewrites.
---

# PaperSpine Orchestrator

## Active-File Contract

When this skill is invoked, read this active `SKILL.md` from disk before
applying PaperSpine rules. Do not use memory, old backups, or archived copies as
the rule source. For water-related papers, reports, coursework, or Word/PDF
deliverables, obey `hydraulic-writing-router` when available: PaperSpine owns
workflow, sources, structure, calculations, repair, and artifact verification.

Use this skill as the suite entrypoint and lead dispatcher. Its first job is
to classify the request, then route the work to the smallest branch that can
finish it safely: local edit, section polish, report repair, or full
research-writing workflow.

**Update detection**: If the user asks to update, upgrade, check for updates,
or manage the PaperSpine installation, route immediately to
`paper-spine-update` without starting any writing workflow.

## Dispatch First

Before reading configuration, launching UI, creating PaperSpine artifacts, or
starting research, classify the task into one lane:

1. **Local patch**: one sentence, one paragraph, a small Word/Markdown edit,
   typo repair, wording choice, or narrow style polish. Edit directly or
   delegate to `nature-polishing` or `docx-editor-cn`. Do not create `paper_rewriting_output/`, run intake,
   launch the PaperSpine UI, or require a full configuration.
2. **Section polish**: one section or a small cluster of paragraphs where the
   structure is mostly fixed. Use `nature-polishing` for logic, academic
   clarity, expression density, and natural Chinese coursework tone,
   and the hydraulic core for water-engineering boundaries. Verify facts,
   numbers, encoding, and edited files.
3. **Report repair**: calculation/table closure, template repair, Word/PDF
   formatting, references, figure/CAD consistency, or targeted audit. Use
   local tools plus the relevant branch skill. Create only the lightweight
   notes needed for the repair; do not run full research unless the report's
   argument or structure must be rebuilt.
4. **Full workflow**: building a paper/report from materials, rewriting a
   whole manuscript, changing the controlling motivation, reorganizing many
   sections, producing LaTeX/PDF/Word deliverables, or any task the user
   explicitly calls a big project. Only this lane uses the full PaperSpine
   intake, research, citation, blueprint, write, LaTeX, translate, and audit
   route below.

Default to the smallest sufficient lane. Promote to a heavier lane when a
local edit exposes broken calculations, missing sources, unstable structure,
or cross-file consistency risk. If the user says the task is a big project,
use the full workflow.

Branch ownership is simple: `nature-writing` drafts or rebuilds prose;
`nature-polishing` restructures, polishes, and handles Chinese report voice;
`docx-editor-cn` owns Word files; spreadsheet,
presentation, citation, LaTeX, translation, and audit branch skills own their
respective artifacts.

## Model Delegation Policy

When the current Codex host exposes subagents or separate threads with model
overrides, the dispatcher may route light lanes to a smaller model. Use this
only when the user has asked for model routing, cost control, speed, or
delegation, or when there is a clear task-specific reason.

- Lane 1 local patch: `gpt-5.4` is suitable for one-sentence rewrites,
  small Word/Markdown edits, narrow style polish, and verification. Use
  `gpt-5.4-mini` only for mechanical checks such as typo scans, encoding
  scans, obvious formatting cleanup, or file-existence verification.
- Lane 2 section polish: `gpt-5.4` can handle small fixed-structure sections,
  first-pass Nature polish, and local wording alternatives. Keep the main
  model for final judgment when the section changes the argument, data
  boundary, or engineering conclusion.
- Lane 3 report repair: use `gpt-5.4` for bounded side tasks such as table
  arithmetic checks, old-value searches, reference-format scans, or isolated
  Word/XML inspections. Keep risky edits, cross-table data closure, large Word
  rebuilds, CAD/figure consistency decisions, and final integration with the
  main model.
- Lane 4 full workflow: keep the controlling motivation, structure, final
  synthesis, and delivery audit on the main model. Lower models may support
  sidecar inventory, extraction, first-pass checks, or candidate wording, but
  they do not own the final argument.

Do not delegate a task if spawning an agent is slower than doing the local
patch directly. Every delegated task must have a bounded file scope and a
clear expected output. The main model remains responsible for reviewing the
subagent result, protecting user edits, and running the final verification.

## Operating Principle

For full builds and whole-manuscript rewrites, PaperSpine is a research-writing
workflow: learn the target scene and strong examples first, force a
user-confirmed motivation, design the paper row by row, and only then write or
rebuild the manuscript. For local patches and section polish, act as a
dispatcher and send the task to the appropriate branch without pretending a
full research workflow is needed.

Never fabricate data, metrics, p-values, datasets, citations, figures, or
experimental claims. User materials are authoritative for this paper's results.
External examples teach structure and rhetoric only.

## Report And Hydraulic Writing Hook

Use PaperSpine as the default entrypoint and dispatcher for Chinese reports,
course reports, course designs, course papers, undergraduate homework reports,
engineering design reports, and water/hydraulic reports. Do not revive a
separate course-report skill; delegate to the existing branch skills.

For medium and full report tasks, treat the output as a structured report by
default. Before writing visible prose, create or verify a chapter-duty or
writing-rationale matrix with: engineering/research question, required basis,
calculation/table/data link, and final-text gate. The final report should be
driven by control conditions, local data, formulas or labelled assumptions,
scheme comparison, section parameters, construction/maintenance controls, and
bounded conclusions. For local patches, keep this matrix implicit and verify
only the edited scope plus any affected numbers or file artifacts.

For water-conservancy, hydrology, hydraulic engineering, river engineering,
drainage, urban flooding, water-environment, water-governance, or water-resource
topics, use the hydraulic core in Nature polishing/writing as the general domain
guardrail. It owns water-specific checks such as data-source trace, table
calculation trace, parameter/source boundaries, scenario and scale clarity,
data-scope consistency, table/figure evidence closure, and artifact
verification. Object-specific checks apply only when the current materials
contain those objects.

When the user provides a local folder of water-conservancy papers, use it as the
exemplar corpus for the final output. Before writing visible prose for medium or
full tasks, extract a style profile from multiple papers: chapter organization,
paragraph rhythm, method-detail level, result/table explanation, engineering-use
sentences, conclusion pattern, and reference style. The corpus teaches writing
form and water-paper rhythm; it does not supply facts for the user's project
unless the user explicitly cites a paper as evidence.

For the user's `论文搭建` corpus specifically, prioritize normative expression:
object first, pressure second, method/index/model third, result grade/range/
distribution/trend fourth, engineering use and boundary last. The learned
standard is plain, evidence-dense, and reproducible; do not turn it into ornate
journal prose or topic-specific constraints.

Do not let internal planning language enter the report body. Sentences such as
`本报告先...`, `后文按照...展开`, `论证重点转向...`, and `避免把...处理成...`
belong in planning artifacts unless they are converted into a local engineering
judgment with data, formula, parameter source, design consequence, or boundary.
Actual writing or polishing work must still be routed to `nature-writing` or
`nature-polishing` as appropriate.
For long Chinese hydraulic course-design reports, avoid a single-pass rewrite
that tries to solve calculation, structure, wording, references, and formatting
at once. Use a staged agentic loop:

1. Source and template map: identify the task book, school template, required
   headings, section data, tables, and deliverables.
2. Audit report: compute/check numbers with tools, list data/geometry/table
   issues, template conflicts, missing inputs, and artifact risks. Do not
   rewrite prose yet.
3. Engineering repair: fix calculations, data closure, geometry, scheme scoring,
   and required structure while preserving the template.
4. Nature expression pass: only after the audit issues are handled, run
   `nature-polishing` with the hydraulic core for rhythm, terminology, and
   natural coursework expression.
5. Artifact verification: reopen/read the actual Word/PDF/Markdown output and
   check paragraph/table counts, key numbers, old values, headings, encoding,
   and required template elements.

When the user provides an official school or teacher Word template, treat that
template as the base artifact, not as loose visual inspiration. Start the report
from the template when possible; if a polished report already exists, merge the
report body into the template while preserving the native cover, section
properties, page setup, headers/footers, styles, numbering, and real TOC fields.
Do not rebuild the cover by manually typing an imitation unless the template is
unavailable or corrupted. Fill required cover fields minimally, then verify that
the final `.docx` still contains the template's cover structure and updateable
directory/outline fields.


## Chinese Coursework Voice Pass

After the report's structure, data closure, and engineering boundaries are
stable, run a light student-voice pass when the user asks to reduce AI traces,
make the tone more natural, or polish a Chinese undergraduate coursework
report. This pass should:

- shorten overlong sentences where the meaning does not require the length;
- reduce repeated sentence openings such as `本报告...`, `本文...`, and
  `通过...可知...`;
- replace catalogue prose such as `包括四项`, `第一...第二...第三...第四...`
  with concrete engineering duties, design decisions, or verification items;
- replace broad catalogue sentences with the actual water object, data basis,
  method, result, decision consequence, or boundary. Do not make a paragraph
  sound more natural while leaving it unsupported.
- keep the report formal enough for submission, but avoid over-polished journal
  rhetoric that no longer sounds like undergraduate coursework;
- preserve all facts, numbers, tables, equations, section labels, template
  fields, and engineering conclusions.

Do not apply this as a cosmetic pass before the evidence and parameter checks
are stable. After the rewrite, verify that key numeric claims and table counts
still match the source artifact.

## Chinese Coursework Template And Regression Guardrails

For Chinese undergraduate reports and course-design documents, apply these
guardrails before declaring the artifact final:

- If the user provides another student's template, assignment example, or
  teacher-preferred sample, treat it as the primary style and structure model.
  First extract its chapter order, paragraph duties, calculation sequence,
  table style, reference style, formatting habits, and conclusion pattern.
  Then write the user's content by following that template's method and
  granularity, without copying its wording or fabricating data.
- Do not put process, self-audit, or planning language in the final body. Keep
  such language in `writing_rationale_matrix.md`, audit notes, or the chat.
  Before final delivery, scan the artifact for phrases such as `本报告先`,
  `后文`, `论证重点`, `技术路线`, `主线`, `展开`, `避免把`, `若继续完善`,
  `自查`, and `还需补足`; delete them or convert them into local engineering
  judgments with data, formula, consequence, or boundary.
- Treat teacher-facing prompts and self-check instructions as submission
  blockers, even when they sound reasonable. Phrases such as `涉及权重、评分和参数取值
  的表格，均需...`, `避免表格数据脱离计算过程`, `应优先补足...`, or similar
  checklist language must be rewritten as formal report prose that states the
  adopted source, formula, assumption, standard basis, or exact chapter/table
  where the basis is provided.
- Treat every numeric edit as a global data-closure task. When changing a water
  level, discharge, rainfall, elevation, storage, pollutant load, risk index,
  weighted score, parameter, threshold, or conclusion value, recompute the
  related formula/table and update all matching text, figures, tables, and
  conclusions together. Search for old values afterward.
- When hydraulic or geometric arithmetic is present, explicitly close it with
  the correct basis, datum, unit, object, and scenario. Examples include water
  depth, freeboard, stage difference, storage change, runoff coefficient,
  pollutant-load reduction, and weighted evaluation scores.
- Spatial zones, scenarios, evaluation units, or periods must be labelled and
  non-conflicting when they are used to support a result or recommendation.
- Scheme-comparison tables must include weight basis, scoring scale, formula,
  and at least one substitution for the recommended scheme. After adding this,
  remove any conclusion sentence claiming the scoring process is still missing.
- Keep technical functions precise. A material, model, index, parameter, or
  management measure should be tied to the water process or decision it affects,
  not described as a generic improvement.
- Format Chinese references, especially standards, as complete GB/T 7714-style
  entries when possible: responsible organization, standard number, title
  `[S]`, place, publisher, and year.
- References to course task books, school formatting requirements, teacher
  handouts, templates, and local design briefs must also be completed before
  delivery, not only national standards. Prefer: responsible organization,
  document title, document type such as `[R]`, and year, with normal spacing
  after punctuation. Do not leave entries like `学院.题名[R].2026.` when the
  template or task material identifies the issuing unit.
- If the user says to revise the final/current/original report in place, edit
  that file directly and verify it after saving. Create a new version only when
  the user asks for a separate copy or the edit is high-risk enough to require a
  clearly named backup.
- For Chinese deliverables on Windows, avoid writing Chinese正文 through
  PowerShell heredocs or inline command strings. Use UTF-8 files, base64
  payloads, or structured XML/zip editing, then reopen/read back the artifact
  and check for mojibake, question-mark corruption, old values, and table count.

## Required Configuration

This configuration is required only for the full workflow lane. Local patch,
section polish, and report repair lanes must not launch intake or require a
PaperSpine config unless they are promoted to full workflow.

For full workflow, prefer reading `paper_rewriting_output/paper_spine_config.json`.
If it is missing, route to `paper-spine-intake` or ask the same fields directly.

Required fields:

| Field | Allowed Values |
|---|---|
| `workflow` | `rewrite_existing`, `build_from_materials` |
| `scene` | `journal`, `conference`, `report_review`, `competition` |
| `tier` | `flash`, `pro` |
| `output_language` | `en`, `zh` |
| `target_name` | free text |
| `materials_dir` | path or empty |
| `draft_path` | path or empty |
| `user_motivation` | free text or empty |
| `official_urls` | list |
| `special_requirements` | list |
| `word_output` | `none`, `docx` |
| `translation_package` | `none`, `zh` |
| `reference_mode` | `local_first`, `specified_paths`, `web` |
| `reference_paths` | list of local reference folders/files; default `["."]` |
| `citation_target_count` | integer; default `20` |

## Full Workflow Route

Use this route only after the dispatcher selects Lane 4. The steps below are
non-negotiable for substantial builds and whole-document rewrites, but they
must not be triggered by a local sentence edit, small polish request, or
targeted Word repair.

1. If configuration is missing or incomplete, run the terminal wizard from
   `paper-spine-ui`, then `paper-spine-intake`; do not ask the user to
   hand-write JSON or answer a long plain chat checklist when a terminal is
   available. The wizard is the supported Claude Code/Codex command-line UI.
   In Claude Code, `/paperspine` is the preferred entry: it launches the
   external intake window automatically when configuration is missing.

   **Codex full-workflow constraint:** when Lane 4 has been selected and
   `paper_rewriting_output/paper_spine_config.json` is missing, the first full
   workflow tool action should be to run the absolute
   `launch_paperspine_ui.ps1` (resolve under `~/.codex/skills/...` or
   `~/.claude/skills/...`) with `sandbox_permissions: require_escalated` so the
   window can open. Do not inspect materials, infer defaults, create config
   files, or continue the full workflow before the UI has launched or
   explicitly failed. Only fall back to numbered/chat intake if the launch
   returns an error. This constraint does not apply to Lanes 1-3.
2. Always create or verify `source_map.md`.
3. Always use `paper-spine-research` before choosing the final motivation.
   Research must first index local/default references according to
   `reference_mode` and `reference_paths`; web collection supplements this
   index but does not replace it.
4. Research must create `reference_materials/`, `research_dossier.md`,
   `exemplar_learning_dossier.md`, `style_profile.md`, `sota_gap_map.md`, and
   `motivation_options_after_research.md`.
5. Use `paper-spine-citation` to create `citation_support_bank.md`. This bank
   is separate from exemplar learning: it supports Introduction, Related Work,
   Discussion, background, limitation, and application claims. Generate at
   least `citation_target_count * 3` candidates; default target is 20, so the
   default candidate pool is 60. About 80% should be recent, using
   `current_year - 3` as the simple threshold.
6. Stop for user confirmation of the controlling motivation. Do not write or
   rewrite until `confirmed_motivation.md` records the user's chosen motivation.
   The final motivation should be concise and specific. Do not inflate one
   narrow contribution into a multi-claim motivation.
7. If `workflow` is `rewrite_existing`, use `paper-spine-rewrite`.
8. If `workflow` is `build_from_materials`, use `paper-spine-build`.
9. Before drafting, both workflows must create `section_blueprints.md` and
   `writing_rationale_matrix.md`. The matrix is the execution plan, not a
   post-hoc summary.
10. Run the integrity audit: `python scripts/integrity_audit.py paper_rewriting_output --markdown --write`.
    This produces `integrity_audit.md` — a teaching report where every finding
    includes root cause, fix action, downstream impact, and a teaching note.
    The report must show no BLOCKED findings before LaTeX compilation can proceed.
11. Use `paper-spine-latex` for final LaTeX structure, figure placement,
   citation safety, and compile-oriented cleanup.
12. Always produce final LaTeX source. Compile PDF when a TeX engine is
    available. Markdown alone is not a final PaperSpine output.
13. If `word_output` is `docx`, produce and check a Word version.
14. If `output_language` is `en` and `translation_package` is `zh`, use
    `paper-spine-translate` to produce the complete `translation_zh/` package.
    Run `python scripts/translate_guard.py paper_rewriting_output --markdown --write`
    and require PASS. The translation package must cover every required
    intermediate and final artifact with row-by-row translation of large
    tabular files. Summaries are not acceptable.
15. Use `paper-spine-audit` before declaring the work complete.

If another skill is unavailable, follow the referenced workflow locally and
produce the same artifacts.

## Standard Artifacts

Write workflow artifacts under `paper_rewriting_output/` unless the user asks
otherwise.

Common required artifacts:

- `paper_spine_config.json`
- `paper_spine_config.md`
- `source_map.md`
- `reference_materials/source_index.md`
- `research_dossier.md`
- `exemplar_learning_dossier.md`
- `style_profile.md`
- `sota_gap_map.md`
- `motivation_options_after_research.md`
- `citation_support_bank.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`

Rewrite existing:

- `original_logic_map.md`
- `evidence_bank.md`
- `rewrite_matrix.md`
- `logic_transfer_audit.md`
- revised manuscript

Build from materials:

- `source_inventory.md`
- `evidence_bank.md`
- `figure_asset_map.md`
- `claim_register.md`
- manuscript draft as an intermediate artifact

Final artifacts:

- `latex_report.md`
- `final_artifact_manifest.md`
- `final_paper/main.tex`
- `final_paper/paper.pdf` when a TeX compiler is available
- `final_paper/paper.docx` and `word_report.md` when Word output is requested
- `translation_zh/` when English output requests a Chinese translation package

## Writing Rationale Matrix Requirement

`writing_rationale_matrix.md` must be created before final writing in both
`rewrite_existing` and `build_from_materials`. It must be a Markdown table used
as the execution plan:

| Row ID | Manuscript Unit | Current/Planned Function | Motivation Link | Reference/SOTA Pattern Learned | Target Scene or Venue Norm | User Evidence or Citation Anchor | Planned Change | Final Text Check |
|---|---|---|---|---|---|---|---|---|

The first data row must justify the whole-work framework, structure, or main
throughline in depth: why this controlling structure is chosen, how SOTA/target
examples informed it, how it follows the confirmed motivation, which user
evidence anchors it, and how the final manuscript will be checked against it.
Subsequent rows must follow the target document in order and split it into the
smallest useful writing units: paragraph-level moves, paragraph
groups, model steps, assumptions, result/claim units, review synthesis units,
competition solution blocks, headings, captions, and other argument-bearing
fragments.

This is flexible by scene. A journal paper may naturally use abstract,
introduction, methods, results, and discussion units. A competition paper may
use problem restatement, assumptions, model construction, solving process,
validation, sensitivity, strengths/weaknesses, and recommendations. A report or
review may use executive summary, background, taxonomy, comparison, synthesis,
and recommendation units. Do not force all tasks into a fixed IMRaD template.

Each row must explain concrete anchors across multiple dimensions: it advances
or narrows the confirmed motivation, transfers a structural pattern learned from
SOTA/example work, matches a target-scene norm, uses a user-provided evidence
item, creates a front/back echo, fixes an original logic failure, and/or
constrains a claim to available evidence. For important rows, write enough
reasoning that the user can learn why this writing move is better.

A shallow matrix is a failure. If most rows say only "improve clarity" or
"polish wording", stop and redo the research/blueprint stage.

## Branch Map

Read `references/orchestrator-branch-map.md` when the workflow needs to be
debugged or when a branch output fails audit. The rule is simple: route back to
the branch that owns the weak artifact instead of patching the final paper
directly.

## Command-Line UI

Claude Code and Codex do not guarantee a native graphical picker for skills.
The supported UI is the bundled terminal wizard for the full workflow lane.
When Lane 4 configuration is missing, run `paper-spine-intake`. In Claude Code,
`/paperspine` must launch the intake
UI automatically; do not ask the user to call a separate UI command. The launcher
opens the bundled terminal TUI, which supports Up/Down for option values,
Left/Right for fields, Enter for edit or confirm, and `S` to save. Claude Code
does not currently provide third-party skills with an API for embedding a custom
keyboard UI directly inside the chat input box, so the real terminal TUI is the
supported interactive path. Use native structured questions only when the host
exposes them reliably in the current session. Use chat fallback only when
terminal execution is impossible.

For Chinese water-engineering reports, apply a general audit gate before any
prose polish or final delivery. This gate must explicitly check: important
table arithmetic, duplicated calculation or explanation sections, blank required
template fields, unsupported value or term drift across the same object and
basis, parameter/source boundaries, nonstandard headings, inconsistent reference
formatting, and artifact validity. These are submission blockers, not style
suggestions.
Key calculations must be presented before final delivery. Require a visible
formula, substitution, result, and judgment for calculations that support scheme
choice, weighted scores, water levels, discharges, rainfall/runoff quantities,
storage, pollutant loads, risk grades, parameters, or conclusions. Formatting is
governed by the user's explicit requirements and the provided template; do not
invent custom fonts, table styles, equation styles, margins, or captions. For
Word outputs, render important formulas as standalone native Word equations
generated from LaTeX/OMML whenever feasible.
When the user asks to raise the report standard, run an optional engineering
depth diagnosis. Look for the underlying failure pattern: object not named,
method without data source, result without range/grade/baseline, parameter
without basis, missing-data jumps, subjective scoring, inconsistent units or
datums, unverified standards, weak transfer boundary, and recommendations
without a decision target. Add evidence or bounded assumptions only when the
object exists and the source basis is available; otherwise record the missing
input instead of inventing a parameter or standard.
Also guard against two execution failures: compute numeric substitutions with
deterministic tools rather than language-model mental arithmetic, and
concentrate missing-input boundaries in the calculation-boundary and later
verification sections instead of repeating defensive disclaimers.
