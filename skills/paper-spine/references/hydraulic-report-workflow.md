# Hydraulic Report Workflow

Load this reference only for Chinese water/course/engineering reports, report
repair, template merge, Word/PDF delivery, or multi-file tasks that include task
books, guidance documents, group tables, user data, official templates, or
another person's report/sample.

## Source Roles

Classify every file before drafting or formatting. Record the classification in
`source_map.md` for full workflows, or in repair notes for smaller lanes:

- **Requirement source**: task books, teacher instructions, grading rubrics,
  formatting requirements, official school templates, and required headings.
- **User evidence source**: the user's data, group table, measurements,
  calculations, notes, figures, drafts, and confirmed conclusions.
- **Structure-only exemplar**: another student's report, a personal template,
  a sample answer, a strong paper, or a teacher-preferred model used to learn
  chapter order, method sequence, table style, formula placement, paragraph
  duty, and conclusion rhythm.
- **Reference source**: standards, papers, manuals, and citations used to
  support background, methods, parameters, or discussion.
- **Unknown or unsafe source**: any file whose role is unclear. Do not use it
  for final claims until its role is resolved.

Structure-only exemplars are quarantined. They may teach path and granularity,
but they must not enter `evidence_bank.md` or `claim_register.md` as support for
facts, numbers, formulas, parameters, object names, locations, conclusions, or
recommendations. A formula, constant, threshold, score, or conclusion seen only
in an exemplar must be re-derived from the task book, a standard, user data, or
an explicitly labelled course-design assumption.

If the only long "draft" is another student's template or sample and the user
wants their own report, select `build_from_materials` with that file marked as a
structure-only exemplar. Use `rewrite_existing` only for text that is truly the
user's own draft or a file the user explicitly asks to revise in place.

Before final delivery, run a template-leak check whenever structure-only
exemplars exist. Use `scripts/template_leak_guard.py` when feasible, saving the
result as `paper_rewriting_output/template_leak_report.md` or an equivalent
repair note. Treat copied exemplar sentences, exemplar-only formulas, and
exemplar-only numbers in the final artifact as submission blockers.

## Report Flow

For medium and full report tasks, treat the output as a structured report by
default. Before writing visible prose, create or verify a chapter-duty or
writing-rationale matrix with: engineering/research question, required basis,
calculation/table/data link, and final-text gate.

The final report should be driven by control conditions, local data, formulas or
labelled assumptions, scheme comparison, section parameters,
construction/maintenance controls, and bounded conclusions. For local patches,
keep this matrix implicit and verify only the edited scope plus affected numbers
or artifacts.

For long Chinese hydraulic course-design reports, use a staged loop:

1. Source and template map: identify task book, school template, required
   headings, section data, tables, and deliverables.
2. Audit report: compute/check numbers with tools, list data/geometry/table
   issues, template conflicts, missing inputs, and artifact risks. Do not
   rewrite prose yet.
3. Engineering repair: fix calculations, data closure, geometry, scheme scoring,
   and required structure while preserving the template.
4. Nature expression pass: only after audit issues are handled, run
   `nature-polishing` with the hydraulic core for rhythm, terminology, and
   natural coursework expression.
5. Artifact verification: reopen/read the actual Word/PDF/Markdown output and
   check paragraph/table counts, key numbers, old values, headings, encoding,
   and required template elements.

## Hydraulic Writing Boundary

For water-conservancy, hydrology, hydraulic engineering, river engineering,
drainage, urban flooding, water-environment, water-governance, or water-resource
topics, use the hydraulic core in Nature polishing/writing as the domain
guardrail. It owns water-specific checks such as data-source trace, table
calculation trace, parameter/source boundaries, scenario and scale clarity,
data-scope consistency, table/figure evidence closure, and artifact
verification. Object-specific checks apply only when the current materials
contain those objects.

When the user provides a local folder of water-conservancy papers, use it as a
style corpus. Extract a style profile from multiple papers: chapter
organization, paragraph rhythm, method-detail level, result/table explanation,
engineering-use sentences, conclusion pattern, and reference style. The corpus
teaches writing form and water-paper rhythm; it does not supply facts for the
user's project unless the user explicitly cites a paper as evidence.

For the user's `论文搭建` corpus specifically, prioritize normative expression:
object first, pressure second, method/index/model third, result
grade/range/distribution/trend fourth, engineering use and boundary last.

## Student Voice And Regression Guardrails

Do not let internal planning language enter the report body. Sentences such as
`本报告先...`, `后文按照...展开`, `论证重点转向...`, and `避免把...处理成...`
belong in planning artifacts unless converted into a local engineering judgment
with data, formula, parameter source, design consequence, or boundary.

After structure, data closure, and engineering boundaries are stable, run a
light student-voice pass when the user asks to reduce AI traces, make the tone
more natural, or polish a Chinese undergraduate coursework report:

- shorten overlong sentences where meaning allows;
- reduce repeated openings such as `本报告...`, `本文...`, and `通过...可知...`;
- replace catalogue prose with concrete engineering duties, design decisions,
  or verification items;
- preserve all facts, numbers, tables, equations, section labels, template
  fields, and engineering conclusions.

Before final delivery, scan for planning/self-check phrases such as `本报告先`,
`后文`, `论证重点`, `技术路线`, `主线`, `展开`, `避免把`, `若继续完善`, `自查`,
and `还需补足`; delete them or convert them into local engineering judgments.

Treat teacher-facing prompts and self-check instructions as submission
blockers. Phrases such as `涉及权重、评分和参数取值的表格，均需...`,
`避免表格数据脱离计算过程`, `应优先补足...`, or similar checklist language must
be rewritten as formal report prose stating the adopted source, formula,
assumption, standard basis, or exact chapter/table where the basis is provided.

## Calculation And Reference Closure

Treat every numeric edit as a global data-closure task. When changing a water
level, discharge, rainfall, elevation, storage, pollutant load, risk index,
weighted score, parameter, threshold, or conclusion value, recompute the related
formula/table and update all matching text, figures, tables, and conclusions.
Search for old values afterward.

When hydraulic or geometric arithmetic is present, explicitly close it with the
correct basis, datum, unit, object, and scenario. Important calculations should
show formula, substitution, result, and judgment when they support scheme
choice, weighted scores, water levels, discharges, rainfall/runoff quantities,
storage, pollutant loads, risk grades, parameters, or conclusions.

Spatial zones, scenarios, evaluation units, or periods must be labelled and
non-conflicting when they support a result or recommendation.

Scheme-comparison tables must include weight basis, scoring scale, formula, and
at least one substitution for the recommended scheme. After adding this, remove
any conclusion sentence claiming the scoring process is still missing.

Format Chinese references, especially standards, as complete GB/T 7714-style
entries when possible: responsible organization, standard number, title `[S]`,
place, publisher, and year. References to course task books, school formatting
requirements, teacher handouts, templates, and local design briefs must also be
completed before delivery.

## Word Template And Format Contract

When the user provides an official school or teacher Word template, treat that
template as the base artifact. Start the report from the template when possible;
if a polished report already exists, merge the report body into the template
while preserving native cover, section properties, page setup, headers/footers,
styles, numbering, and real TOC fields. Do not rebuild the cover by manually
typing an imitation unless the template is unavailable or corrupted.

For Word/PDF deliverables, create a separate formatting contract from
requirement sources before final Word work. Extract the contract from guidance
documents, task books, teacher instructions, school formatting requirements, or
official templates, with the source recorded for each rule. Cover every
specified submission-appearance item: page size, orientation, margins,
header/footer distance, normal-text Chinese and English fonts,字号/point size,
line spacing, paragraph before/after spacing, first-line indent, heading levels,
table captions, figure captions, references, equation style, page numbers, and
TOC requirements.

Do not use default academic formats when a guidance file states a different
requirement. If guidance is missing or ambiguous, record the missing item and
either preserve the official template style or ask for the rule before claiming
exact compliance.

For Chinese official-template Word outputs, use structural `.docx` checks and
Microsoft Word/WPS visual opening when visual QA is required. Do not route this
path through automated document conversion. Prefer `docx-editor-cn` guards:
`word_guard.py`, `format_contract_guard.py`, `word_structure_guard.py`, and
actual `.docx` read-back.

For Chinese deliverables on Windows, avoid writing Chinese正文 through PowerShell
heredocs or inline command strings. Use UTF-8 files, base64 payloads, or
structured XML/zip editing, then reopen/read back the artifact and check for
mojibake, question-mark corruption, old values, and table count.
