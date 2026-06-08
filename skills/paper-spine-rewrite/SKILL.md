---
name: paper-spine-rewrite
description: Rewrites an existing manuscript from confirmed motivation, research, paragraph-level rationale, and evidence. (internal /paperspine step)
---

# PaperSpine Rewrite

Use this skill when the user already has a draft and wants a substantive
manuscript improvement.

## Required Inputs

- `paper_rewriting_output/paper_spine_config.json`
- user draft from `draft_path` or the conversation. The draft must be the
  user's own text or a file the user explicitly asks to revise in place.
  Another student's report, a personal template, a sample answer, or a
  teacher-preferred model is a structure-only exemplar by default; route that
  case to `paper-spine-build` instead of rewriting the exemplar.
- `paper_rewriting_output/reference_materials/source_index.md`
- `paper_rewriting_output/research_dossier.md`
- `paper_rewriting_output/exemplar_learning_dossier.md`
- `paper_rewriting_output/style_profile.md`
- `paper_rewriting_output/sota_gap_map.md`
- `paper_rewriting_output/citation_support_bank.md`
- `paper_rewriting_output/confirmed_motivation.md` with user confirmation
- evidence from the user's draft, figures, tables, data, or notes

If research or confirmed motivation is missing, do not rewrite. Return to
`paper-spine-research` and ask the user to confirm the motivation after seeing
research-grounded options.

If `citation_support_bank.md` is missing or shallow, return to
`paper-spine-citation` before final writing. Introduction, background, related
work, and Discussion claims should draw from that bank when they need
literature support.

## Script Resolution

This branch has no local `scripts/` folder. Resolve shared guards such as
`template_leak_guard.py`, `integrity_audit.py`, and `structured_review.py`
under the active `paper-spine/scripts/` folder. Resolve rewrite-specific
audits such as `revision_audit.py` under `paper-spine-audit/scripts/`. Use
expanded absolute paths on Windows when running from the project directory.

## Required Outputs

- `paper_rewriting_output/original_logic_map.md`
- `paper_rewriting_output/evidence_bank.md`
- `paper_rewriting_output/section_blueprints.md`
- `paper_rewriting_output/writing_rationale_matrix.md`
- `paper_rewriting_output/rewrite_matrix.md`
- `paper_rewriting_output/logic_transfer_audit.md`
- `paper_rewriting_output/template_leak_report.md` when structure-only
  exemplars are present and a final artifact is produced
- `paper_rewriting_output/format_contract.json` when Word/PDF delivery has
  guidance, task-book, school, teacher, or template formatting requirements
- `paper_rewriting_output/word_format_contract_report.md` when a `.docx` final
  artifact is produced from that contract
- `paper_rewriting_output/word_merge_plan.json` and
  `paper_rewriting_output/word_structure_report.md` when final Word content is
  merged into an official template
- revised manuscript or revised sections
- `translation_zh/` package when `translation_package` is `zh` (via `paper-spine-translate`)

## Original Logic Map

Before rewriting, map the existing manuscript in order:

| Original Unit | Current Text Role | Evidence Used | Motivation Link | Problem | Keep / Move / Rewrite / Delete |
|---|---|---|---|---|---|

This is required so the rewrite can be compared against the original logic, not
only against surface wording.

If supporting files include templates or examples, mark their units as
structure-only exemplars. They may influence the "Current Text Role" or the
planned section duty, but they are not evidence. Any original unit whose only
support is an exemplar formula, exemplar number, exemplar object, or exemplar
conclusion must be rewritten from the user's evidence or moved to a missing
input/assumption note.

## Writing Rationale Matrix

Before final prose, create `writing_rationale_matrix.md` and read
`references/writing-rationale-matrix.md`. The matrix is the rewrite plan. It
must be ordered by the manuscript's actual writing units, not by a fixed IMRaD
or journal-paper template.

Use this table:

| Row ID | Manuscript Unit | Original Problem or Planned Function | Motivation Link | Reference/SOTA Pattern Learned | Target Scene or Venue Norm | User Evidence or Citation Anchor | Planned Change | Final Text Check |
|---|---|---|---|---|---|---|---|---|

The first data row must deeply justify the whole-work framework or throughline:
why this controlling structure is chosen, how SOTA/target examples informed it,
how it follows the confirmed motivation, which user evidence anchors it, and how
the final manuscript will be checked against it. After that, split the draft
into the smallest useful units for this target scene:
paragraphs, paragraph groups, result/claim units, model steps, assumptions,
review synthesis blocks, competition solution blocks, headings, captions, or
other argument-bearing fragments. Do not force reports, reviews, or competition
papers into Abstract/Introduction/Methods/Results/Discussion if that is not the
right structure.

Each row must explain concrete anchors across multiple dimensions. Acceptable
reasons include: confirms or narrows the central motivation, transfers a
structural move from a strong example without copying wording, matches
target-scene expectation, moves evidence next to the claim, fixes a weak
transition, creates a front/back echo, or constrains a claim to available
evidence. If a row cannot teach the user why this writing move is better, it is
too shallow.

## Natural Voice Tier

If `paper_spine_config.json` has `humanize_tier` set to `light`, `medium`, or
`heavy`, keep the rewrite inside PaperSpine and apply `nature-polishing` after
the content, calculation, evidence, and template gates are stable. Nature
polishing owns Chinese naturalness, anti-AI regularity checks, paragraph rhythm,
and expression density. Do not route to a separate naturalization skill.

## Report And Hydraulic Rewrite Gate

If the draft is a Chinese report, course report, course design, design report,
engineering report, water/hydraulic report, or the config/user request contains
`课程报告`, `课程设计`, `课程论文`, `设计报告`, `本科作业`, `工程报告`, `水利`, `水文`, `水资源`, or
`水工`, keep the rewrite inside PaperSpine. Do not call a separate
course-report skill.

In that mode, the original logic map must remap each unit to a report-duty
matrix:

- question answered by the unit;
- required basis, such as task-book data, formula, code/standard basis,
  literature support, engineering analogy, or labelled course-design assumption;
- calculation, table, or data link;
- final-text gate that prevents planning language from entering the body.

Rewrite by moving evidence next to judgments, compressing generic background,
making scheme comparison or evaluation logic explicit, and tying parameters,
figures, and tables to their evidence basis. For water-conservancy and hydraulic
topics, apply the hydraulic core from Nature polishing/writing as the general
domain guardrail: data-source trace, table calculation trace, parameter/source
boundaries, scenario and scale clarity, data-scope consistency, table/figure
evidence closure, and Word/PDF artifact verification. Object-specific checks
apply only when the current materials contain that object.

If `reference_paths`, `materials_dir`, or the user message provides a local
folder of water-conservancy papers, rewrite against that corpus. Before final
prose, `style_profile.md`, `exemplar_learning_dossier.md`, and the
`writing_rationale_matrix.md` must show how multiple papers informed the
chapter order, paragraph rhythm, method/result wording, table/figure
explanation, engineering-use sentences, conclusion style, and reference pattern.
Transfer writing moves, not facts or sentences.

For the user's `论文搭建` corpus, the rewrite should emphasize normative
expression: object first, pressure second, method/index/model third, result
grade/range/distribution/trend fourth, engineering use and boundary last. This
should guide paragraph repair and anti-AI polishing before sentence beautifying.

Final prose for this mode must pass a body admission test: each paragraph should
name a real object, method, dataset, water level, elevation, layer, structure,
figure, table, or maintenance object, and also provide a basis, consequence, or
boundary. Delete or rewrite sentences such as `本报告先...`, `后文按照...展开`,
`论证重点转向...`, or `避免把...处理成...` when they merely expose the author planning
process.

The original logic map must also flag tables whose key numbers lack a visible
source or calculation path. For weights, scores, parameters, and calculated
values, preserve them only when the draft, task book, code, formula, user notes,
or evidence support them. Otherwise add a planned change to supply the weight
basis, scoring rule, formula/substitution, parameter source, or a clear
course-design/report-stage limitation.

For Chinese water-engineering reports, the original logic map must also detect
these general defects before rewriting:

- arithmetic mismatch between formulas, tables, figures, and prose;
- repeated calculation or explanation sections that should become a consequence
  statement;
- blank required cover, identity, date, or submission fields;
- unsupported value or term drift across tables, prose, figures, and conclusions
  for the same object under the same stage, period, scenario, datum, and
  calculation basis; valid differences must be labelled by object or basis;
- important parameters, thresholds, scores, or model settings without source,
  formula, assumption, literature support, or later verification boundary;
- loose engineering headings and inconsistent reference punctuation.

Repair these in the local chapter, table, heading, reference list or artifact manifest before applying student-voice or anti-AI edits.
Before final output, run a report gap-closure pass:

- calculation presentation: for each calculation that affects a design decision or conclusion, show formula, substitution, result and design judgment. Repeated formulas may be fully shown once and referenced later, but table values must still be recomputed and checked;
- formatting contract: follow user-provided font, table, heading, caption, margin, reference and equation requirements exactly. If the user has not specified a visible formatting rule, preserve the source/template style rather than inventing a new one;
- format-contract extraction: before Word delivery, extract all specified
  formatting rules from requirement sources into
  `paper_rewriting_output/format_contract.json`, with evidence/source text for
  each rule. Include page size/orientation, margins, header/footer distances,
  body and heading fonts,字号/point sizes, line spacing, paragraph spacing,
  first-line indent, captions, references, equations, page numbers, and TOC
  rules when specified. Unknown items must remain explicit gaps, not defaults;
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
  expected places, and obvious question-mark encoding damage is absent;
- conclusion discipline: fixable gaps must be repaired in their local chapters,
  not left as future-work confessions in the conclusion.

## Rewrite Rules

- Rewrite from `writing_rationale_matrix.md`, not by appending sentences to old
  paragraphs.
- Do not rewrite a structure-only exemplar paragraph by paragraph. If the
  source draft is not the user's own text, stop and route to build-from-
  materials. If exemplars are present only as support files, use them for
  structural moves and granularity only.
- Keep structure-only exemplars out of `evidence_bank.md`. Do not preserve an
  exemplar-only formula, constant, threshold, score, object name, place name, or
  conclusion unless a requirement source, user evidence source, reference
  source, or labelled course-design assumption independently supports it.
- A paragraph should survive unchanged only if the matrix explicitly says why it
  already serves the confirmed motivation.
- Preserve user claims only when supported by user evidence.
- Preserve LaTeX commands, labels, citations, equations, figures, and tables
  unless the user asks to change structure.
- Use `output_language` from config: `en` for English, `zh` for Chinese.
- Select citations from `citation_support_bank.md` only when they support a
  specific sentence. Do not add citation clusters without a clear claim.
- Keep target-scene style subordinate to the confirmed motivation.
- `rewrite_matrix.md` must map original units to final units and state whether
  each change is structural, rhetorical, evidence-related, or only language.
- When structure-only exemplars are present, run
  the shared `paper-spine/scripts/template_leak_guard.py` or an equivalent comparison before final
  delivery. Resolve copied exemplar passages, exemplar-only formulas, and
  exemplar-only numbers before routing to Word, PDF, or LaTeX.

## Pre-LaTeX Gate

Before routing output to `paper-spine-latex`, run:

```bash
python <paper-spine>/scripts/integrity_audit.py paper_rewriting_output --markdown --write
python <paper-spine>/scripts/structured_review.py paper_rewriting_output --dispatch
```

`integrity_audit.md` must show no BLOCKED findings. After dispatch, launch
three parallel review sub-agents per `review_prompts/dispatch.md`. Validate
independence with `structured_review.py --validate review_prompts`.

Read `references/writing-rationale-matrix.md`,
`references/motivation-thread-writing.md`, `references/deep-imitation-protocol.md`,
and `references/rewrite-matrix.md` when doing substantive rewriting.
