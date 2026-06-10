# Changelog

## 2026-06-10 content-first LaTeX/PDF route

- Make Markdown/source-text review the default content stage for Chinese water
  reports and course designs.
- Require confirmed content to be saved or marked as `confirmed_content.md`
  before final formatting begins.
- Keep the final report source at
  `paper_rewriting_output/final_paper/main.tex`; compile
  `paper_rewriting_output/final_paper/paper.pdf` when a TeX engine is
  available.
- Defer native school cover integration until after content confirmation, then
  ask the user for the exact image, PDF, or file path.
- Remove unused repository overlays so the package no longer installs patched
  PaperSpine or Nature entrypoints.
- Keep the hydraulic engineering core as an on-demand resource loaded by the
  router, not by Nature's global `always_load`.
- Keep the installer minimal: router, router UI metadata, and the hydraulic
  engineering core only.
