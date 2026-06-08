#!/usr/bin/env python3
"""Check DOCX template preservation and field-level structure.

This guard is intentionally lightweight and read-only. It complements
format_contract_guard.py: that script checks exact formatting values; this one
checks whether important Word structures survived template merging.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


@dataclass
class Finding:
    severity: str
    item: str
    expected: str
    actual: str


def qn(local: str) -> str:
    return W + local


def read_json(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def zip_names(path: Path) -> set[str]:
    with zipfile.ZipFile(path) as zf:
        return set(zf.namelist())


def read_part(path: Path, name: str) -> bytes | None:
    with zipfile.ZipFile(path) as zf:
        if name not in zf.namelist():
            return None
        return zf.read(name)


def parse_part(path: Path, name: str) -> ET.Element | None:
    data = read_part(path, name)
    if data is None:
        return None
    return ET.fromstring(data)


def text_from_docx(path: Path) -> str:
    parts = []
    for name in ("word/document.xml",):
        root = parse_part(path, name)
        if root is None:
            continue
        for node in root.iter():
            if node.tag in {qn("t"), qn("delText"), qn("instrText")} and node.text:
                parts.append(node.text)
            elif node.tag in {qn("p"), qn("br"), qn("cr")}:
                parts.append("\n")
    return "".join(parts)


def instr_text(path: Path) -> str:
    text_parts = []
    for name in zip_names(path):
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        root = parse_part(path, name)
        if root is None:
            continue
        for node in root.iter(qn("instrText")):
            if node.text:
                text_parts.append(node.text)
    return "\n".join(text_parts)


def count_nodes(path: Path, part: str, tag: str) -> int:
    root = parse_part(path, part)
    if root is None:
        return 0
    return sum(1 for _ in root.iter(qn(tag)))


def style_ids(path: Path) -> set[str]:
    root = parse_part(path, "word/styles.xml")
    if root is None:
        return set()
    out = set()
    for style in root.findall(qn("style")):
        sid = style.attrib.get(qn("styleId"))
        if sid:
            out.add(sid)
    return out


def content_controls(path: Path) -> int:
    return count_nodes(path, "word/document.xml", "sdt")


def part_group(names: set[str], pattern: str) -> set[str]:
    rx = re.compile(pattern)
    return {name for name in names if rx.match(name)}


def compare_template_parts(template: Path | None, final: Path) -> list[Finding]:
    if template is None:
        return []
    findings: list[Finding] = []
    template_names = zip_names(template)
    final_names = zip_names(final)

    required_patterns = {
        "headers": r"word/header\d+\.xml$",
        "footers": r"word/footer\d+\.xml$",
        "numbering": r"word/numbering\.xml$",
        "settings": r"word/settings\.xml$",
        "footnotes": r"word/footnotes\.xml$",
        "endnotes": r"word/endnotes\.xml$",
    }
    for label, pattern in required_patterns.items():
        before = part_group(template_names, pattern)
        if not before:
            continue
        after = part_group(final_names, pattern)
        missing = before - after
        if missing:
            findings.append(
                Finding("FAIL", f"template_parts.{label}", ", ".join(sorted(before)), ", ".join(sorted(after)) or "missing")
            )

    before_styles = style_ids(template)
    after_styles = style_ids(final)
    missing_styles = sorted(before_styles - after_styles)
    if missing_styles:
        findings.append(
            Finding("FAIL", "template_styles", f"{len(before_styles)} template styles preserved", "missing: " + ", ".join(missing_styles[:20]))
        )

    before_sdt = content_controls(template)
    after_sdt = content_controls(final)
    if before_sdt and after_sdt < before_sdt:
        findings.append(
            Finding("WARN", "content_controls", f">= {before_sdt}", str(after_sdt))
        )
    return findings


def bool_path(data: dict[str, Any], *keys: str) -> bool:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return False
        cur = cur.get(key)
    return bool(cur)


def check_field_requirements(final: Path, contract: dict[str, Any], merge_plan: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    instructions = instr_text(final)
    document_root = parse_part(final, "word/document.xml")
    if document_root is None:
        return [Finding("FAIL", "document_xml", "word/document.xml", "missing")]

    required = {
        "toc": bool_path(contract, "toc", "required") or bool_path(merge_plan, "required_fields", "toc"),
        "page_numbers": bool_path(contract, "page_numbers", "required") or bool_path(merge_plan, "required_fields", "page_numbers"),
        "figure_seq": bool_path(contract, "captions", "figure_seq_required") or bool_path(merge_plan, "required_fields", "figure_seq"),
        "table_seq": bool_path(contract, "captions", "table_seq_required") or bool_path(merge_plan, "required_fields", "table_seq"),
        "native_omml": bool_path(contract, "equations", "native_omml_required") or bool_path(merge_plan, "required_fields", "native_omml"),
    }
    if required["toc"] and "TOC" not in instructions.upper():
        findings.append(Finding("FAIL", "field.toc", "TOC field", "missing"))
    if required["page_numbers"] and "PAGE" not in instructions.upper():
        findings.append(Finding("FAIL", "field.page_numbers", "PAGE field", "missing"))
    if required["figure_seq"] and not re.search(r"\bSEQ\s+(Figure|figure|图|figure_c\d+)", instructions):
        findings.append(Finding("FAIL", "field.figure_seq", "figure SEQ field", "missing"))
    if required["table_seq"] and not re.search(r"\bSEQ\s+(Table|table|表|table_c\d+)", instructions):
        findings.append(Finding("FAIL", "field.table_seq", "table SEQ field", "missing"))
    if required["native_omml"] and not any(node.tag.endswith("oMath") for node in document_root.iter()):
        findings.append(Finding("FAIL", "field.native_omml", "native Word equation OMML", "missing"))
    return findings


def check_merge_plan(final: Path, template: Path | None, merge_plan: dict[str, Any]) -> list[Finding]:
    if not merge_plan:
        return []
    findings: list[Finding] = []
    final_text = text_from_docx(final)
    template_text = text_from_docx(template) if template else ""
    for key in ("body_start_anchor", "body_end_anchor"):
        anchor = merge_plan.get(key)
        if not anchor:
            continue
        if template and anchor not in template_text:
            findings.append(Finding("FAIL", f"merge_plan.template.{key}", str(anchor), "not found"))
        if anchor not in final_text:
            findings.append(Finding("FAIL", f"merge_plan.final.{key}", str(anchor), "not found"))

    required_text = merge_plan.get("must_preserve_text")
    if isinstance(required_text, list):
        for text in required_text:
            if text and str(text) not in final_text:
                findings.append(Finding("FAIL", "merge_plan.must_preserve_text", str(text), "not found"))
    return findings


def escape_md(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def build_report(final: Path, findings: list[Finding], template: Path | None, contract: Path | None, merge_plan: Path | None) -> tuple[str, str]:
    fail_count = sum(1 for f in findings if f.severity == "FAIL")
    warn_count = sum(1 for f in findings if f.severity == "WARN")
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    lines = [
        "# Word Structure Guard Report",
        "",
        f"Status: **{status}**",
        "",
        f"- Final DOCX: `{final}`",
    ]
    if template:
        lines.append(f"- Template DOCX: `{template}`")
    if contract:
        lines.append(f"- Format contract: `{contract}`")
    if merge_plan:
        lines.append(f"- Merge plan: `{merge_plan}`")
    lines.extend(["", f"- Failures: {fail_count}", f"- Warnings: {warn_count}", "", "## Findings", ""])
    if findings:
        lines.append("| Severity | Item | Expected | Actual |")
        lines.append("|---|---|---|---|")
        for finding in findings:
            lines.append(
                f"| {finding.severity} | `{finding.item}` | {escape_md(finding.expected)} | {escape_md(finding.actual)} |"
            )
    else:
        lines.append("No template-structure or required-field violations detected.")
    lines.append("")
    return status, "\n".join(lines)


def validate(final: Path, template: Path | None, contract_path: Path | None, merge_plan_path: Path | None) -> tuple[str, str]:
    contract = read_json(contract_path)
    merge_plan = read_json(merge_plan_path)
    findings: list[Finding] = []
    if "word/document.xml" not in zip_names(final):
        findings.append(Finding("FAIL", "docx", "word/document.xml", "missing"))
        return build_report(final, findings, template, contract_path, merge_plan_path)
    findings.extend(compare_template_parts(template, final))
    findings.extend(check_field_requirements(final, contract, merge_plan))
    findings.extend(check_merge_plan(final, template, merge_plan))
    return build_report(final, findings, template, contract_path, merge_plan_path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", required=True, help="Final DOCX to check.")
    parser.add_argument("--template", help="Original template DOCX, if available.")
    parser.add_argument("--contract", help="format_contract.json, if available.")
    parser.add_argument("--merge-plan", help="word_merge_plan.json, if available.")
    parser.add_argument("--output", help="Markdown report path.")
    parser.add_argument("--fail-on", choices=("fail", "warn", "never"), default="fail")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    final = Path(args.final)
    template = Path(args.template) if args.template else None
    contract = Path(args.contract) if args.contract else None
    merge_plan = Path(args.merge_plan) if args.merge_plan else None
    for path in (final, template, contract, merge_plan):
        if path is not None and not path.exists():
            raise FileNotFoundError(path)
    status, report = validate(final, template, contract, merge_plan)
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
