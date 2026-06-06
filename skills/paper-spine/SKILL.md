---
name: paper-spine
description: Main PaperSpine dispatcher for papers, reports, coursework, course designs, engineering reports, and water/hydraulic writing. Use when Codex needs to decide whether a request is a local edit, section polish, report repair, or full paper/report build. Choose the smallest sufficient lane, delegate drafting/polishing/humanizing/Word work to branch skills, optionally route light lanes to lower-cost models such as gpt-5.4 when the host supports model overrides, and run the full PaperSpine research-writing workflow only for substantial builds or rewrites.
---

# PaperSpine Orchestrator

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
   typo repair, wording choice, or narrow anti-AI rewrite. Edit directly or
   delegate to `nature-polishing`, `paper-spine-humanize`, `humanizer`, or
   `docx-editor-cn`. Do not create `paper_rewriting_output/`, run intake,
   launch the PaperSpine UI, or require a full configuration.
2. **Section polish**: one section or a small cluster of paragraphs where the
   structure is mostly fixed. Use `nature-polishing` for logic and academic
   clarity, `paper-spine-humanize` or `humanizer` for Chinese anti-AI tone,
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
`nature-polishing` restructures and polishes; `paper-spine-humanize` handles
Chinese report anti-AI tone; `docx-editor-cn` owns Word files; spreadsheet,
presentation, citation, LaTeX, translation, and audit branch skills own their
respective artifacts.

## Model Delegation Policy

When the current Codex host exposes subagents or separate threads with model
overrides, the dispatcher may route light lanes to a smaller model. Use this
only when the user has asked for model routing, cost control, speed, or
delegation, or when there is a clear task-specific reason.

- Lane 1 local patch: `gpt-5.4` is suitable for one-sentence rewrites,
  small Word/Markdown edits, narrow anti-AI polish, and verification. Use
  `gpt-5.4-mini` only for mechanical checks such as typo scans, encoding
  scans, obvious formatting cleanup, or file-existence verification.
- Lane 2 section polish: `gpt-5.4` can handle small fixed-structure sections,
  first-pass humanize work, and local wording alternatives. Keep the main
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

For water-conservancy, hydrology, hydraulic engineering, ecological revetment,
river engineering, drainage, urban flooding, ecological water engineering, or
water-resource topics, use the hydraulic core in Nature polishing/writing as
the domain guardrail. It owns water-specific checks such as table calculation
trace, elevation and geometry closure, layer-function precision, plant-zone
boundaries, figure/CAD consistency, and artifact verification.

Do not let internal planning language enter the report body. Sentences such as
`本报告先...`, `后文按照...展开`, `论证重点转向...`, and `避免把...处理成...`
belong in planning artifacts unless they are converted into a local engineering
judgment with data, formula, parameter source, design consequence, or boundary.
Actual polishing or humanize work must still be routed to the original
`nature-polishing`, `nature-writing`, `humanizer`, or `paper-spine-humanize`
skill as appropriate.
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
4. Water-expression pass: only after the audit issues are handled, run the
   Chinese hydraulic expression/humanize layer for rhythm, terminology, and
   anti-AI cleanup.
5. Artifact verification: reopen/read the actual Word/PDF/Markdown output and
   check paragraph/table counts, key numbers, old values, headings, encoding,
   and required template elements.


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
- for ecological revetment sentences that list `防冲、排水、护坡、生态` or quote
  principles such as `安全优先、生态兼容`, lower the AI tone by linking local
  hydrodynamic or seepage features to the design order, then state how ecology
  fits within flood-conveyance and slope-stability limits;
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
- Treat every numeric edit as a global data-closure task. When changing a
  water level, elevation, embedment depth, layer thickness, weighted score,
  plant-zone boundary or conclusion value, recompute the related
  geometry/formula and update all matching text, tables,
  plant zoning, and conclusions together. Search for old values afterward.
- For hydraulic geometry, explicitly close the arithmetic. Examples: toe
  bottom elevation = bed elevation - embedment depth; toe top elevation = toe
  bottom elevation + structure height; flood depth = design flood level - bed
  elevation; freeboard = crest elevation - control elevation.
- Spatial/plant zones must form adjacent non-overlapping intervals when
  elevations are known. Avoid vague descriptions such as "above the toe" when
  a design flood level, toe top, berm, or crest elevation can define the zone.
- Scheme-comparison tables must include weight basis, scoring scale, formula,
  and at least one substitution for the recommended scheme. After adding this,
  remove any conclusion sentence claiming the scoring process is still missing.
- Keep hydraulic layer functions precise: geotextile/filter fabric retains
  soil and blocks fine-particle loss; gravel or cushion layers mainly drain,
  level, and protect the filter layer. Do not blur these functions.
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

For Chinese hydraulic course-design reports, apply a hard-audit gate before any prose polish or final delivery. This gate must explicitly check: weighted-score arithmetic, duplicated calculation sections, blank cover fields, unsupported value or term drift across the same object and calculation basis, empirical toe/scour/filter parameters without defensible boundaries, geotextile laying/overlap details, nonstandard headings such as `水利理由`, and inconsistent GB/T 7714 reference punctuation. These are submission blockers, not style suggestions.
For hydraulic course-design reports, key calculations must be presented before final delivery. Require a visible formula, substitution, result, and design judgment for calculations that support scheme choice, weighted scores, elevations, dimensions, material parameters, or conclusions. Formatting is governed by the user's explicit requirements and the provided template; do not invent custom fonts, table styles, equation styles, margins, or captions. For Word outputs, render important formulas as standalone native Word equations generated from LaTeX/OMML whenever feasible.
For ecological revetment and typical-section course designs that already pass
the basic audit, run an optional engineering-depth diagnosis when the user asks
to raise the report standard. Look for the underlying failure pattern rather
than copying prior advice: parameters without mechanism, missing-data jumps,
undrawable geometry, mixed layer functions, unclear freeboard/safety-margin
bases, subjective scheme scores, unverified standard currency, construction
transfer gaps, and ambiguous quantity or left/right-bank scope. Treat these as
conditional upgrades. Add evidence or bounded assumptions only when the object
exists and the source basis is available; otherwise record the missing input
instead of inventing a parameter or standard.
Also guard against three execution failures: compute numeric substitutions with deterministic tools rather than language-model mental arithmetic; concentrate missing-input boundaries in the calculation-boundary and later verification sections instead of repeating defensive disclaimers; and when one bank refers to the controlling side, still close the reference side's absolute elevations, layer sequence, geometry, and drawing/quantity scope instead of physically omitting it.
