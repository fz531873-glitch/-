#!/usr/bin/env python3
"""Lightweight DOCX sanity guard for PaperSpine Word outputs.

This is a compatibility guard for the PaperSpine suite. It performs fast,
read-only checks that a generated DOCX is a usable Word document and records
basic structure counts. Exact school formatting is handled by
docx-editor-cn/scripts/format_contract_guard.py; template preservation is
handled by docx-editor-cn/scripts/word_structure_guard.py.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


@dataclass
class Finding:
    severity: str
    item: str
    detail: str


def qn(local: str) -> str:
    return W + local


def read_part(docx: Path, name: str) -> bytes | None:
    with zipfile.ZipFile(docx) as zf:
        if name not in zf.namelist():
            return None
        return zf.read(name)


def parse_part(docx: Path, name: str) -> ET.Element | None:
    data = read_part(docx, name)
    if data is None:
        return None
    return ET.fromstring(data)


def zip_names(docx: Path) -> set[str]:
    with zipfile.ZipFile(docx) as zf:
        return set(zf.namelist())


def collect_text(root: ET.Element) -> str:
    chunks: list[str] = []
    for node in root.iter():
        if node.tag in {qn("t"), qn("delText"), qn("instrText")} and node.text:
            chunks.append(node.text)
        elif node.tag in {qn("p"), qn("br"), qn("cr")}:
            chunks.append("\n")
    return "".join(chunks)


def count(root: ET.Element, local: str) -> int:
    return sum(1 for _ in root.iter(qn(local)))


def validate(docx: Path) -> tuple[str, str]:
    findings: list[Finding] = []
    metrics: dict[str, int | str] = {}

    if not docx.exists():
        findings.append(Finding("FAIL", "file", f"missing: {docx}"))
        return build_report(docx, findings, metrics)
    if docx.suffix.lower() != ".docx":
        findings.append(Finding("FAIL", "extension", "expected .docx"))
        return build_report(docx, findings, metrics)

    try:
        names = zip_names(docx)
    except zipfile.BadZipFile:
        findings.append(Finding("FAIL", "zip", "not a valid Office ZIP package"))
        return build_report(docx, findings, metrics)

    required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
    missing = sorted(required - names)
    if missing:
        findings.append(Finding("FAIL", "package_parts", "missing: " + ", ".join(missing)))
        return build_report(docx, findings, metrics)

    root = parse_part(docx, "word/document.xml")
    if root is None:
        findings.append(Finding("FAIL", "document_xml", "word/document.xml missing or unreadable"))
        return build_report(docx, findings, metrics)

    text = collect_text(root)
    paragraphs = count(root, "p")
    tables = count(root, "tbl")
    equations = count(root, "oMath")
    drawings = count(root, "drawing")
    fields = count(root, "instrText")
    metrics.update(
        {
            "size_bytes": docx.stat().st_size,
            "paragraphs": paragraphs,
            "tables": tables,
            "equations": equations,
            "drawings": drawings,
            "field_runs": fields,
            "text_chars": len(text.strip()),
        }
    )

    if paragraphs == 0:
        findings.append(Finding("FAIL", "paragraphs", "0 paragraphs found"))
    if len(text.strip()) == 0 and drawings == 0:
        findings.append(Finding("FAIL", "content", "no text or drawings found"))
    if "\ufffd" in text or "????" in text:
        findings.append(Finding("FAIL", "encoding", "replacement characters or question-mark corruption found"))
    if re.search(r"\\(?:cite|ref|autoref|includegraphics|begin|end)\b", text):
        findings.append(Finding("WARN", "raw_latex", "raw LaTeX command appears in Word text"))

    return build_report(docx, findings, metrics)


def build_report(docx: Path, findings: list[Finding], metrics: dict[str, int | str]) -> tuple[str, str]:
    fail_count = sum(1 for f in findings if f.severity == "FAIL")
    warn_count = sum(1 for f in findings if f.severity == "WARN")
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    lines = [
        "# Word Guard Report",
        "",
        f"Status: **{status}**",
        "",
        f"- DOCX: `{docx}`",
        f"- Failures: {fail_count}",
        f"- Warnings: {warn_count}",
        "",
        "## Metrics",
        "",
    ]
    if metrics:
        lines.extend(f"- `{key}`: {value}" for key, value in metrics.items())
    else:
        lines.append("No metrics available.")
    lines.extend(["", "## Findings", ""])
    if findings:
        lines.append("| Severity | Item | Detail |")
        lines.append("|---|---|---|")
        for finding in findings:
            lines.append(f"| {finding.severity} | `{finding.item}` | {escape_md(finding.detail)} |")
    else:
        lines.append("No basic DOCX validity issues detected.")
    lines.append("")
    return status, "\n".join(lines)


def escape_md(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", help="DOCX file to inspect.")
    parser.add_argument("--output", help="Markdown report path.")
    parser.add_argument("--markdown", action="store_true", help="Accepted for compatibility; output is always Markdown.")
    parser.add_argument("--fail-on", choices=("fail", "warn", "never"), default="fail")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    status, report = validate(Path(args.docx))
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.fail_on == "never":
        return 0
    if status == "FAIL" and args.fail_on in {"fail", "warn"}:
        return 2
    if status == "WARN" and args.fail_on == "warn":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
