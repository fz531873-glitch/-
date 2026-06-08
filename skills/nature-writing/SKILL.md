---
name: nature-writing
description: Draft, restructure, or plan Nature-style manuscript sections from author-provided claims, results, figures, notes, or Chinese drafts. Use when the user wants to write or rebuild an abstract, introduction, related-work, method, experiments, discussion, conclusion, title, or full manuscript argument rather than only polish finished prose. Also trigger on general academic-writing requests even without the word "Nature", such as writing a paper from scratch, drafting a manuscript/section, structuring a paper, course report, course design, course paper, engineering report, and Chinese phrasings like 学术写作、科研写作、论文写作、写论文、写paper、SCI写作、帮我写论文、搭论文框架、起草论文、写引言/摘要/讨论、课程报告、课程设计、课程论文、设计报告. For water-conservancy, hydrology, hydraulic engineering, water resources, river, drainage, urban flooding, and water-environment topics, use the hydraulic-engineering core as the domain guardrail.
version: 1.0.0
author: Community contribution, refactored into static/dynamic layers
---

# Nature-Style Scientific Writing — Router

## Active-File Contract

When this skill is invoked, read this active `SKILL.md` from disk before
drafting. Do not apply Nature writing rules from memory alone. Then read
`manifest.yaml` and every path listed under `always_load`; load only the
additional fragments required by the detected axes. For water-conservancy,
hydrology, hydraulic engineering, river, drainage, water-resource,
water-environment, or Chinese water coursework tasks, coordinate through
`hydraulic-writing-router` when available. Nature writing owns drafting or
rebuilding prose from confirmed materials and chapter duties; PaperSpine owns
workflow, calculations, data closure, template conflicts, and final artifact
verification.

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core stance + workflow, paper-type playbooks, per-section drafting guidance, language-specific rules, per-journal style).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the drafting logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, writing workflow, and output format that apply to every drafting job.

If the request is for a Chinese report, course report, course design, course
paper, undergraduate homework report, engineering report, or contains `课程报告`,
`课程设计`, `课程论文`, `设计报告`, `本科作业`, `工程报告`, `水利`, `水文`, `水资源`, or `水工`, keep the
work inside this skill's original drafting workflow. Do not call a separate
course-report skill. If the user wants an end-to-end Word/PDF/LaTeX report,
route the whole deliverable through PaperSpine; use this skill for drafting or
restructuring sections.

For water-conservancy, hydrology, hydraulic engineering, river engineering,
drainage, urban flooding, water-environment, water-governance, or water-resource
topics, also read `../nature-polishing/static/core/hydraulic-engineering.md` as
the domain guardrail before drafting. Use it to plan report rhythm, information
density, data-closure checks, table/figure consistency, and engineering
boundaries, then use this skill's original claim/evidence, paragraph-flow, and
boundary rules. Object-specific checks are conditional and apply only when the
current materials contain that object.

If the user provides a local folder of water papers as style samples, read enough
of that corpus to extract a style profile before final drafting. Use the corpus
to match water-paper structure, paragraph rhythm, method/result wording, and
engineering-use expression; do not copy text or import unsupported claims.
### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `paper_type` — research / methods / hypothesis / algorithmic / review. Default: research.
- `section` — abstract / intro / related-work / method / experiments / discussion / conclusion / title. May be multiple. Ask the user if it is ambiguous and matters for the draft.
- `language` — en or zh-to-en. Detect from the user's notes themselves.
- `journal` — nature / nat-comms / generic. Default: generic. If the user names a Nature subjournal, treat it as `nature`.

State the detected axis values in one short line to the user before drafting, so they can correct you cheaply.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis only when the user has explicitly asked for a free-floating argument paragraph with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Draft using the loaded material

Apply the loaded fragments in this priority order:

1. Core stance + intake (`core/stance.md`) — surface missing claim / evidence / boundary before drafting.
2. Paper-type playbook — argument chain, drafting order.
3. Section-specific drafting rules and structure.
4. Journal-specific framing and constraints.
5. Language-specific sentence and paragraph rules (apply last).

Run the 8-step workflow in `core/workflow.md` end-to-end. Do not skip steps 1-3 (planning) just because the user asked for prose immediately — write the one-sentence argument first.

If essential evidence or boundary is missing, write a placeholder and list it under `Assumptions or missing inputs:` instead of inventing content.

### 5. Reach for references only when needed

The files under `references/` are deep references and the example library, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user asks for a concrete example or template → `references/examples/index.md`.
- A section's draft has structural problems that the section fragment alone does not explain → the matching `references/<section>.md`.
- The user needs a broad-audience `Nature` abstract opening or asks about a `summary paragraph` → `references/nature-summary-paragraph.md`.
- The user asks "does this paragraph flow?" → `references/paragraph-flow.md`.
- The user asks for a self-review or rejection-risk audit → `references/paper-review.md`.

## Why this split

- The static layer is versioned and reviewable. Adding a new journal style, paper type, or section is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context, instead of the full multi-thousand-line reference set.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.
- This structure mirrors `nature-polishing` so shared content can later be lifted into a `_shared/` layer used by both skills.
