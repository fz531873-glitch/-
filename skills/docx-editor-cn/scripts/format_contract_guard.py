#!/usr/bin/env python3
"""Validate a DOCX file against a guidance-derived formatting contract.

The contract must be extracted from the task book, guidance document, school
requirements, or official template before Word delivery. This guard checks the
final DOCX package against that contract without modifying the file.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
TWIPS_PER_CM = 567.0
TWIPS_PER_PT = 20.0

FONT_ALIASES = {
    "宋体": {"宋体", "SimSun"},
    "simsun": {"宋体", "SimSun"},
    "黑体": {"黑体", "SimHei"},
    "simhei": {"黑体", "SimHei"},
    "楷体": {"楷体", "KaiTi", "楷体_GB2312"},
    "kaiti": {"楷体", "KaiTi", "楷体_GB2312"},
    "仿宋": {"仿宋", "FangSong", "仿宋_GB2312"},
    "fangsong": {"仿宋", "FangSong", "仿宋_GB2312"},
    "times new roman": {"Times New Roman"},
    "cambria math": {"Cambria Math"},
}


@dataclass
class Finding:
    severity: str
    item: str
    expected: str
    actual: str
    evidence: str = ""


def qn(local: str) -> str:
    return W + local


def wattr(node: ET.Element, local: str) -> str | None:
    return node.attrib.get(qn(local))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_docx_xml(docx_path: Path, name: str) -> ET.Element | None:
    with zipfile.ZipFile(docx_path) as zf:
        if name not in zf.namelist():
            return None
        return ET.fromstring(zf.read(name))


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def almost_equal(actual: float | None, expected: float | None, tolerance: float) -> bool:
    if actual is None or expected is None:
        return False
    return math.isclose(actual, expected, abs_tol=tolerance)


def bool_from_onoff(value: str | None) -> bool:
    if value is None:
        return True
    return value not in {"0", "false", "False", "off"}


def font_set(value: str | None) -> set[str]:
    if not value:
        return set()
    key = value.strip().lower()
    return FONT_ALIASES.get(key, {value.strip()})


def font_matches(actual: str | None, expected: str) -> bool:
    if not actual:
        return False
    return bool(font_set(actual) & font_set(expected))


def evidence_for(spec: dict[str, Any], key: str) -> str:
    evidence = spec.get("evidence")
    if isinstance(evidence, dict):
        return str(evidence.get(key, ""))
    if isinstance(evidence, str):
        return evidence
    return ""


def collect_section_props(document_root: ET.Element) -> list[ET.Element]:
    sects = list(document_root.iter(qn("sectPr")))
    # Word may place the final sectPr under body; duplicates are harmless for checking.
    unique: list[ET.Element] = []
    seen: set[int] = set()
    for sect in sects:
        ident = id(sect)
        if ident not in seen:
            unique.append(sect)
            seen.add(ident)
    return unique


def section_page_values(sect: ET.Element) -> dict[str, float | str | None]:
    values: dict[str, float | str | None] = {}
    pg_mar = sect.find(qn("pgMar"))
    if pg_mar is not None:
        for key in ("top", "bottom", "left", "right", "header", "footer", "gutter"):
            raw = wattr(pg_mar, key)
            if raw is not None:
                values[f"margin_{key}_cm"] = int(raw) / TWIPS_PER_CM
    pg_sz = sect.find(qn("pgSz"))
    if pg_sz is not None:
        width = wattr(pg_sz, "w")
        height = wattr(pg_sz, "h")
        if width is not None:
            values["width_cm"] = int(width) / TWIPS_PER_CM
        if height is not None:
            values["height_cm"] = int(height) / TWIPS_PER_CM
        orient = wattr(pg_sz, "orient")
        if orient is not None:
            values["orientation"] = orient
        elif width is not None and height is not None:
            values["orientation"] = "landscape" if int(width) > int(height) else "portrait"
    return values


def build_style_maps(styles_root: ET.Element | None) -> tuple[dict[str, ET.Element], dict[str, str]]:
    by_id: dict[str, ET.Element] = {}
    by_name: dict[str, str] = {}
    if styles_root is None:
        return by_id, by_name
    for style in styles_root.findall(qn("style")):
        style_id = wattr(style, "styleId")
        if not style_id:
            continue
        by_id[style_id] = style
        name_node = style.find(qn("name"))
        if name_node is not None:
            name = wattr(name_node, "val")
            if name:
                by_name[name] = style_id
    return by_id, by_name


def resolve_style_id(requested: str, by_id: dict[str, ET.Element], by_name: dict[str, str]) -> str | None:
    if requested in by_id:
        return requested
    return by_name.get(requested)


def merge_props(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in update.items():
        if value is not None:
            merged[key] = value
    return merged


def style_direct_props(style: ET.Element) -> dict[str, Any]:
    props: dict[str, Any] = {}
    rpr = style.find(qn("rPr"))
    if rpr is not None:
        fonts = rpr.find(qn("rFonts"))
        if fonts is not None:
            for key in ("eastAsia", "ascii", "hAnsi"):
                value = wattr(fonts, key)
                if value:
                    props[f"font_{key}"] = value
        sz = rpr.find(qn("sz"))
        if sz is not None and wattr(sz, "val"):
            props["size_pt"] = int(wattr(sz, "val")) / 2
        b = rpr.find(qn("b"))
        if b is not None:
            props["bold"] = bool_from_onoff(wattr(b, "val"))
        i = rpr.find(qn("i"))
        if i is not None:
            props["italic"] = bool_from_onoff(wattr(i, "val"))

    ppr = style.find(qn("pPr"))
    if ppr is not None:
        jc = ppr.find(qn("jc"))
        if jc is not None and wattr(jc, "val"):
            props["alignment"] = wattr(jc, "val")
        spacing = ppr.find(qn("spacing"))
        if spacing is not None:
            before = wattr(spacing, "before")
            after = wattr(spacing, "after")
            line = wattr(spacing, "line")
            line_rule = wattr(spacing, "lineRule") or "auto"
            if before is not None:
                props["space_before_pt"] = int(before) / TWIPS_PER_PT
            if after is not None:
                props["space_after_pt"] = int(after) / TWIPS_PER_PT
            if line is not None:
                if line_rule == "auto":
                    props["line_multiple"] = int(line) / 240.0
                else:
                    props["line_spacing_pt"] = int(line) / TWIPS_PER_PT
                props["line_rule"] = line_rule
        ind = ppr.find(qn("ind"))
        if ind is not None:
            first = wattr(ind, "firstLine")
            left = wattr(ind, "left")
            hanging = wattr(ind, "hanging")
            if first is not None:
                props["first_line_indent_twips"] = int(first)
            if left is not None:
                props["left_indent_twips"] = int(left)
            if hanging is not None:
                props["hanging_indent_twips"] = int(hanging)
    return props


def effective_style_props(
    style_id: str,
    by_id: dict[str, ET.Element],
    cache: dict[str, dict[str, Any]],
    stack: set[str] | None = None,
) -> dict[str, Any]:
    if style_id in cache:
        return cache[style_id]
    stack = stack or set()
    if style_id in stack or style_id not in by_id:
        return {}
    stack.add(style_id)
    style = by_id[style_id]
    props: dict[str, Any] = {}
    based_on = style.find(qn("basedOn"))
    if based_on is not None and wattr(based_on, "val"):
        props = merge_props(props, effective_style_props(wattr(based_on, "val"), by_id, cache, stack))
    props = merge_props(props, style_direct_props(style))
    cache[style_id] = props
    return props


def expected_indent_twips(spec: dict[str, Any], props: dict[str, Any]) -> int | None:
    if "first_line_indent_twips" in spec:
        return int(spec["first_line_indent_twips"])
    if "first_line_indent_cm" in spec:
        return round(float(spec["first_line_indent_cm"]) * TWIPS_PER_CM)
    if "first_line_indent_chars" in spec:
        size = as_float(spec.get("size_pt")) or as_float(props.get("size_pt"))
        if size is None:
            return None
        return round(float(spec["first_line_indent_chars"]) * size * TWIPS_PER_PT)
    return None


def check_page(document_root: ET.Element, contract: dict[str, Any]) -> list[Finding]:
    spec = contract.get("page")
    if not isinstance(spec, dict) or not spec:
        return [Finding("WARN", "page", "guidance-derived page contract", "missing")]

    findings: list[Finding] = []
    sects = collect_section_props(document_root)
    if not sects:
        return [Finding("FAIL", "page", "section properties", "missing")]

    numeric_keys = [
        "margin_top_cm",
        "margin_bottom_cm",
        "margin_left_cm",
        "margin_right_cm",
        "margin_header_cm",
        "margin_footer_cm",
        "width_cm",
        "height_cm",
    ]
    for idx, sect in enumerate(sects, start=1):
        actual = section_page_values(sect)
        for key in numeric_keys:
            expected = as_float(spec.get(key))
            if expected is None:
                continue
            actual_value = as_float(actual.get(key))
            if not almost_equal(actual_value, expected, float(spec.get("tolerance_cm", 0.06))):
                findings.append(
                    Finding(
                        "FAIL",
                        f"page.section{idx}.{key}",
                        f"{expected:.2f} cm",
                        "missing" if actual_value is None else f"{actual_value:.2f} cm",
                        evidence_for(spec, key),
                    )
                )
        if spec.get("orientation") and actual.get("orientation") != spec.get("orientation"):
            findings.append(
                Finding(
                    "FAIL",
                    f"page.section{idx}.orientation",
                    str(spec.get("orientation")),
                    str(actual.get("orientation")),
                    evidence_for(spec, "orientation"),
                )
            )
    return findings


def check_one_style(
    style_key: str,
    spec: dict[str, Any],
    by_id: dict[str, ET.Element],
    by_name: dict[str, str],
    cache: dict[str, dict[str, Any]],
) -> list[Finding]:
    style_id = resolve_style_id(style_key, by_id, by_name)
    if style_id is None:
        return [Finding("FAIL", f"style.{style_key}", "existing Word style", "missing")]
    props = effective_style_props(style_id, by_id, cache)
    findings: list[Finding] = []

    font_checks = {
        "font_east_asia": "font_eastAsia",
        "font_ascii": "font_ascii",
        "font_hansi": "font_hAnsi",
    }
    for expected_key, actual_key in font_checks.items():
        expected = spec.get(expected_key)
        if not expected:
            continue
        actual = props.get(actual_key)
        if not font_matches(str(actual) if actual else None, str(expected)):
            findings.append(
                Finding(
                    "FAIL",
                    f"style.{style_key}.{expected_key}",
                    str(expected),
                    str(actual or "missing"),
                    evidence_for(spec, expected_key),
                )
            )

    numeric_checks = [
        ("size_pt", 0.15, "pt"),
        ("space_before_pt", 0.3, "pt"),
        ("space_after_pt", 0.3, "pt"),
        ("line_multiple", 0.03, "x"),
        ("line_spacing_pt", 0.3, "pt"),
    ]
    for key, tol, unit in numeric_checks:
        expected = as_float(spec.get(key))
        if expected is None:
            continue
        actual = as_float(props.get(key))
        if not almost_equal(actual, expected, tol):
            findings.append(
                Finding(
                    "FAIL",
                    f"style.{style_key}.{key}",
                    f"{expected:g} {unit}",
                    "missing" if actual is None else f"{actual:g} {unit}",
                    evidence_for(spec, key),
                )
            )

    expected_indent = expected_indent_twips(spec, props)
    if expected_indent is not None:
        actual_indent = props.get("first_line_indent_twips")
        if actual_indent is None or abs(int(actual_indent) - expected_indent) > 24:
            findings.append(
                Finding(
                    "FAIL",
                    f"style.{style_key}.first_line_indent",
                    f"{expected_indent} twips",
                    "missing" if actual_indent is None else f"{actual_indent} twips",
                    evidence_for(spec, "first_line_indent_chars"),
                )
            )

    for key in ("bold", "italic"):
        if key in spec:
            expected_bool = bool(spec[key])
            actual_bool = bool(props.get(key, False))
            if actual_bool != expected_bool:
                findings.append(
                    Finding(
                        "FAIL",
                        f"style.{style_key}.{key}",
                        str(expected_bool),
                        str(actual_bool),
                        evidence_for(spec, key),
                    )
                )

    if spec.get("alignment"):
        actual_alignment = props.get("alignment")
        if actual_alignment != spec.get("alignment"):
            findings.append(
                Finding(
                    "FAIL",
                    f"style.{style_key}.alignment",
                    str(spec.get("alignment")),
                    str(actual_alignment or "missing"),
                    evidence_for(spec, "alignment"),
                )
            )
    return findings


def check_styles(styles_root: ET.Element | None, contract: dict[str, Any]) -> list[Finding]:
    style_specs = contract.get("styles")
    if not isinstance(style_specs, dict) or not style_specs:
        return [Finding("WARN", "styles", "guidance-derived style contract", "missing")]
    by_id, by_name = build_style_maps(styles_root)
    if styles_root is None:
        return [Finding("FAIL", "styles.xml", "word/styles.xml", "missing")]
    cache: dict[str, dict[str, Any]] = {}
    findings: list[Finding] = []
    for style_key, spec in style_specs.items():
        if isinstance(spec, dict):
            findings.extend(check_one_style(style_key, spec, by_id, by_name, cache))
    return findings


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.iter(qn("t")))


def paragraph_style(paragraph: ET.Element) -> str:
    ppr = paragraph.find(qn("pPr"))
    if ppr is None:
        return "Normal"
    pstyle = ppr.find(qn("pStyle"))
    if pstyle is None:
        return "Normal"
    return wattr(pstyle, "val") or "Normal"


def check_paragraph_style_samples(document_root: ET.Element, contract: dict[str, Any]) -> list[Finding]:
    samples = contract.get("paragraph_style_samples") or []
    if not isinstance(samples, list):
        return []
    paragraphs = list(document_root.iter(qn("p")))
    findings: list[Finding] = []
    for sample in samples:
        if not isinstance(sample, dict) or not sample.get("contains") or not sample.get("style"):
            continue
        needle = str(sample["contains"])
        expected_style = str(sample["style"])
        matched = False
        for p in paragraphs:
            text = paragraph_text(p)
            if needle not in text:
                continue
            matched = True
            actual_style = paragraph_style(p)
            if actual_style != expected_style:
                findings.append(
                    Finding(
                        "FAIL",
                        f"paragraph_style_sample.{needle}",
                        expected_style,
                        actual_style,
                        str(sample.get("evidence", "")),
                    )
                )
            break
        if not matched:
            findings.append(
                Finding(
                    "WARN",
                    f"paragraph_style_sample.{needle}",
                    f"paragraph containing {needle}",
                    "not found",
                    str(sample.get("evidence", "")),
                )
            )
    return findings


def build_report(docx: Path, contract: Path, findings: list[Finding]) -> tuple[str, str]:
    fail_count = sum(1 for f in findings if f.severity == "FAIL")
    warn_count = sum(1 for f in findings if f.severity == "WARN")
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    lines = [
        "# Word Format Contract Report",
        "",
        f"Status: **{status}**",
        "",
        f"- DOCX: `{docx}`",
        f"- Contract: `{contract}`",
        f"- Failures: {fail_count}",
        f"- Warnings: {warn_count}",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.append("| Severity | Item | Expected | Actual | Evidence |")
        lines.append("|---|---|---|---|---|")
        for finding in findings:
            lines.append(
                "| "
                f"{finding.severity} | `{finding.item}` | {escape_md(finding.expected)} | "
                f"{escape_md(finding.actual)} | {escape_md(finding.evidence)} |"
            )
    else:
        lines.append("No format-contract violations detected.")
    lines.append("")
    return status, "\n".join(lines)


def escape_md(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def validate(docx_path: Path, contract_path: Path) -> tuple[str, str]:
    contract = read_json(contract_path)
    document_root = read_docx_xml(docx_path, "word/document.xml")
    if document_root is None:
        report = f"# Word Format Contract Report\n\nStatus: **FAIL**\n\n`{docx_path}` has no `word/document.xml`.\n"
        return "FAIL", report
    styles_root = read_docx_xml(docx_path, "word/styles.xml")
    findings: list[Finding] = []
    findings.extend(check_page(document_root, contract))
    findings.extend(check_styles(styles_root, contract))
    findings.extend(check_paragraph_style_samples(document_root, contract))
    return build_report(docx_path, contract_path, findings)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", required=True, help="Final DOCX to validate.")
    parser.add_argument("--contract", required=True, help="Guidance-derived format_contract.json.")
    parser.add_argument("--output", help="Markdown report path.")
    parser.add_argument("--fail-on", choices=("fail", "warn", "never"), default="fail")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    docx_path = Path(args.docx)
    contract_path = Path(args.contract)
    if not docx_path.exists():
        raise FileNotFoundError(docx_path)
    if not contract_path.exists():
        raise FileNotFoundError(contract_path)
    status, report = validate(docx_path, contract_path)
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
