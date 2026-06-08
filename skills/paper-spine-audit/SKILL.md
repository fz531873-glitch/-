---
name: paper-spine-audit
description: Audits PaperSpine outputs for missing artifacts, shallow revisions, logic transfer, unsupported claims, and translation coverage. (internal /paperspine step)
---

# PaperSpine Audit

Use this skill before calling a PaperSpine rewrite or build complete.

## Script Resolution

Use local `paper-spine-audit/scripts/` guards when they exist. Citation quality
verification is owned by `paper-spine-citation/scripts/citation_quality_audit.py`.
If a command is run from the project directory on Windows, pass the expanded
absolute script path and prefer `D:\python\python.exe` when available.

## Required Checks

1. Artifact completeness.
2. Reference material workspace exists and has a source index.
3. Motivation was confirmed by the user after research, not invented before
   research.
4. `writing_rationale_matrix.md` exists, is ordered, and covers the whole-work
   framework plus the task-specific writing units for the selected scene. It
   should split the paper/report into paragraph-sized, claim-sized, evidence,
   model, synthesis, heading, caption, or competition-solution units as needed;
   it must not be a fixed IMRaD checklist when the task is not an IMRaD paper.
   The first row must deeply justify the whole-work framework, and each row must
   include concrete motivation, reference/SOTA, target-scene, evidence, and
   planned text-move anchors rather than short labels.
   For Chinese water-conservancy course reports, this matrix must include or
   reference a chapter-duty matrix: engineering question, required basis,
   calculation/table/data link, and final-text gate. A generic writing rhythm
   or chapter outline is not enough.
5. No append-only or shallow revision for substantive rewrite tasks.
6. Logic transfer from original draft or materials to final manuscript.
7. Claim support from user evidence.
8. LaTeX citation, label, and figure safety when a LaTeX project exists.
9. `citation_support_bank.md` count, recency, and per-paper support-sentence
   quality before citations are selected for Introduction/Discussion.
9. Final LaTeX source exists; compiled PDF exists when a TeX engine is
   available.
10. Word output is structurally valid when a `.docx` is requested or generated.
11. Translation coverage is complete when `translation_package` is `zh`,
    including `full_paper_translation.zh.md` for the complete final paper text
    and row-by-row translation of large intermediate artifacts such as
    `writing_rationale_matrix.md`.
12. Chinese water-conservancy course-report gate when applicable:
    - final body does not contain planning-language sentences such as
      `本报告先...`, `后文按照...展开`, `论证重点转向...`, or
      `避免把...处理成...` unless they have been converted into local
      engineering judgments with data, formula, parameter source, design
      consequence, or boundary;
    - paragraphs that carry design decisions name an engineering object and at
      least one basis, consequence, or boundary;
    - ambiguous terms are labelled by basis, datum, scenario, object, time
      period, or formula when multiple meanings exist;
    - scheme-comparison tables show weight basis, scoring scale,
      weighted-score formula, and one worked substitution;
    - parameter tables and method text state source/formula/assumption for key
      values, thresholds, scores, model settings, or engineering parameters;
    - data closure has been checked across the final body, tables, figures,
      conclusions, and generated Word/PDF artifacts;
    - weighted scores are recomputed from the stated weights and scores, and
      the table, formula expansion, and prose agree;
    - relevant arithmetic is closed with the correct basis, datum, object,
      scenario, unit, and period;
    - after any numeric change, old values no longer occur in the final text,
      parameter tables, conclusions, or verification lists;
    - technical-function wording is precise: materials, models, indicators,
      parameters, or management measures are tied to the process or decision
      they affect;
    - final prose does not contain self-checking instructions such as "tables
      must explain their source"; it states the adopted formula, assumption,
      standard basis, or local chapter where the calculation appears;
    - weighted-score arithmetic has been independently recomputed, including every row of scheme-comparison tables, and formula expansions agree with table values;
    - repeated calculation sections have been collapsed or justified, so later chapters do not restate earlier crest/freeboard arithmetic without a new design consequence;
    - cover fields required by the school template, such as student ID and name, are completed or explicitly listed as missing user input;
    - data-scope consistency is checked by object, design stage and calculation basis; the audit does not force different objects or validly different bases to share one value, but it flags unsupported drift for the same object and basis;
    - empirical or preliminary parameters are paired with source/assumption
      wording and later verification items;
    - headings avoid loose labels such as `水利理由`, and references use one GB/T 7714-style punctuation pattern;
    - key calculations that support design decisions show formula, substitution, result and design judgment; repeated formulas are cross-referenced rather than silently omitted;
    - visible formatting follows the user's supplied requirements or the source template; no custom fonts, table styles, equation styles, margins or captions were invented;
    - Word formulas that matter to the report are rendered as standalone native equations when feasible, with any fallback explicitly noted;
    - fixable gaps are repaired in their local chapters rather than left as
      future-work confessions in the conclusion.

## Scripts

Run when available:

```bash
python scripts/integrity_audit.py paper_rewriting_output --markdown --write
python scripts/artifact_check.py paper_rewriting_output --markdown --write
python scripts/revision_audit.py <original> <revised> --markdown
python scripts/structured_review.py paper_rewriting_output --dispatch
# Then: launch three parallel sub-agents per review_prompts/dispatch.md
# After sub-agents complete: python scripts/structured_review.py paper_rewriting_output --validate review_prompts
python <paper-spine-citation>/scripts/citation_quality_audit.py paper_rewriting_output --write
python scripts/latex_guard.py <main.tex> --bib <references.bib> --markdown
python scripts/word_guard.py paper_rewriting_output/final_paper/paper.docx --markdown --output paper_rewriting_output/word_report.md
```

## Multi-Agent Review Flow

The structured review uses independent sub-agents for genuine reviewer
independence:

1. Run `structured_review.py --dispatch` to generate three isolated reviewer
   prompts under `review_prompts/`.
2. Read `review_prompts/dispatch.md` and launch three Agent calls in parallel.
   Each agent reads ONLY its own prompt file and the manuscript.
3. After all three agents write their output files, run `structured_review.py
   --validate review_prompts` to check independence (cross-contamination
   detection via text similarity).
4. Produce Editor Synthesis merging the three independent reviews.

## Required Outputs

- `paper_rewriting_output/integrity_audit.md`
- `paper_rewriting_output/artifact_check.md`
- `paper_rewriting_output/revision_audit.md` for rewrite tasks
- `paper_rewriting_output/structured_review.md`
- `paper_rewriting_output/citation_quality_audit.md`
- `paper_rewriting_output/logic_transfer_audit.md`
- unresolved risks and user decisions

Do not mark the task complete if required artifacts are missing, if the final
manuscript contains unsupported claims, if translation is partial, or if the
rationale matrix is generic.
