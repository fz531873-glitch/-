# Hydro Writing Core

`hydro-writing-core` is a small Codex skill overlay for Chinese water-related
writing. It routes hydraulic, hydrology, water-resources, drainage, river,
water-environment, course-report, course-design, and engineering-report tasks
without replacing the base PaperSpine or Nature skills.

The package exists to enforce one output policy for water reports:

- develop and review content in Markdown or source text;
- after the user confirms content, save or mark it as `confirmed_content.md`;
- assemble the final report as LaTeX in
  `paper_rewriting_output/final_paper/main.tex`;
- compile `paper_rewriting_output/final_paper/paper.pdf` when a TeX engine is
  available;
- defer native school cover integration until final formatting, then ask the
  user for the exact cover image, PDF, or file path.

It should not run document conversion or external rendering just to inspect
whether the writing is good. Content quality is checked directly from Markdown,
LaTeX source, calculations, tables, and evidence.

## What It Installs

Only three files are installed into the active Codex skill tree:

```text
skills/
  hydraulic-writing-router/
    SKILL.md
    agents/openai.yaml
  nature-polishing/
    static/core/hydraulic-engineering.md
```

The router loads the base skills on demand:

- `paper-spine/SKILL.md` for source mapping, task requirements, calculation
  closure, section duties, final artifact verification, and report repair.
- `nature-writing/SKILL.md` for body prose after PaperSpine has closed source
  roles, chapter duties, calculation boundaries, and required tables.
- `nature-polishing/SKILL.md` for paragraph logic, Chinese report voice, and
  expression density after the content is stable.
- `nature-polishing/static/core/hydraulic-engineering.md` for water-domain
  checks such as object scale, formula chain, parameter basis, scenario
  boundary, table/figure evidence, and engineering judgment.
- `paper-spine-latex/SKILL.md` for final LaTeX assembly and PDF compile checks.

This repository does not install patched PaperSpine or Nature entrypoints. That
keeps their original flow and loading performance intact.

## Install

Prerequisites in the target Codex skill tree:

```text
%USERPROFILE%\.codex\skills\paper-spine\SKILL.md
%USERPROFILE%\.codex\skills\paper-spine-latex\SKILL.md
%USERPROFILE%\.codex\skills\nature-writing\manifest.yaml
%USERPROFILE%\.codex\skills\nature-polishing\manifest.yaml
```

Install from Windows PowerShell:

```powershell
iwr -UseB https://raw.githubusercontent.com/fz531873-glitch/hydro-writing-core/master/install.ps1 -OutFile "$env:TEMP\install-hydro-writing-core.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-hydro-writing-core.ps1"
```

Preview changes first:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-hydro-writing-core.ps1" -DryRun
```

The installer backs up overwritten files by default. Use `-NoBackup` only when
you intentionally want a direct overwrite.

## Current Workflow

For a full Chinese water report or course design, the intended flow is:

1. PaperSpine reads task books, guidance files, templates, tables, data, and
   examples, then classifies each source as requirement, user evidence,
   structure-only exemplar, reference, or unsafe/unknown.
2. PaperSpine closes chapter duties, calculation boundaries, required tables,
   format requirements, and missing-input notes.
3. Nature writing drafts or rebuilds the body sections from the confirmed
   evidence boundary.
4. Nature polishing improves paragraph logic, density, and Chinese coursework
   voice while keeping the hydraulic engineering guardrails active.
5. The user reviews content in Markdown or source text. No format conversion is
   used for content inspection.
6. After confirmation, the accepted content becomes `confirmed_content.md`.
7. PaperSpine LaTeX assembly turns `confirmed_content.md` into
   `paper_rewriting_output/final_paper/main.tex`, uses native
   `\tableofcontents`, integrates the real school cover when provided, and
   compiles PDF when possible.

## Validation

Before release, check:

- PowerShell installer parses and `-DryRun` completes.
- Markdown, YAML, and PowerShell files read back as UTF-8 without replacement
  characters.
- The router mentions `confirmed_content.md`,
  `paper_rewriting_output/final_paper/main.tex`, native `\tableofcontents`,
  and the ban on conversion/rendering for content inspection.
- The repository contains no unused skill overlays that could override base
  PaperSpine or Nature behavior.
