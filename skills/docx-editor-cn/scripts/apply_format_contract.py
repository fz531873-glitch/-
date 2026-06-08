#!/usr/bin/env python3
"""Apply a guidance-derived formatting contract to a DOCX template.

This script preserves the DOCX package and only updates page section properties
and existing paragraph styles named in the contract. It is meant to run after
content decisions are stable and before final validation with
format_contract_guard.py.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
TWIPS_PER_CM = 567.0
TWIPS_PER_PT = 20.0

ET.register_namespace("w", W_NS)
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
ET.register_namespace("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
ET.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
ET.register_namespace("pic", "http://schemas.openxmlformats.org/drawingml/2006/picture")
ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
ET.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006")


FONT_ALIASES = {
    "宋体": "SimSun",
    "simsun": "SimSun",
    "黑体": "SimHei",
    "simhei": "SimHei",
    "楷体": "KaiTi",
    "kaiti": "KaiTi",
    "仿宋": "FangSong",
    "fangsong": "FangSong",
}


def qn(local: str) -> str:
    return W + local


def set_wattr(node: ET.Element, local: str, value: str | int) -> None:
    node.set(qn(local), str(value))


def get_wattr(node: ET.Element, local: str) -> str | None:
    return node.attrib.get(qn(local))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cm_to_twips(value: Any) -> int:
    return round(float(value) * TWIPS_PER_CM)


def pt_to_half_points(value: Any) -> int:
    return round(float(value) * 2)


def pt_to_twips(value: Any) -> int:
    return round(float(value) * TWIPS_PER_PT)


def normalize_font(value: Any) -> str:
    text = str(value).strip()
    return FONT_ALIASES.get(text.lower(), FONT_ALIASES.get(text, text))


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(tag)
    if child is None:
        child = ET.SubElement(parent, tag)
    return child


def find_or_create_sect_pr(document_root: ET.Element) -> list[ET.Element]:
    sects = list(document_root.iter(qn("sectPr")))
    if sects:
        return sects
    body = document_root.find(qn("body"))
    if body is None:
        raise ValueError("word/document.xml has no w:body")
    sect = ET.SubElement(body, qn("sectPr"))
    return [sect]


def apply_page_contract(document_root: ET.Element, contract: dict[str, Any]) -> int:
    page = contract.get("page")
    if not isinstance(page, dict) or not page:
        return 0
    changed = 0
    for sect in find_or_create_sect_pr(document_root):
        pg_mar = ensure_child(sect, qn("pgMar"))
        margin_map = {
            "margin_top_cm": "top",
            "margin_bottom_cm": "bottom",
            "margin_left_cm": "left",
            "margin_right_cm": "right",
            "margin_header_cm": "header",
            "margin_footer_cm": "footer",
            "margin_gutter_cm": "gutter",
        }
        for contract_key, attr in margin_map.items():
            if contract_key in page:
                set_wattr(pg_mar, attr, cm_to_twips(page[contract_key]))
                changed += 1

        if "width_cm" in page or "height_cm" in page or "orientation" in page:
            pg_sz = ensure_child(sect, qn("pgSz"))
            if "width_cm" in page:
                set_wattr(pg_sz, "w", cm_to_twips(page["width_cm"]))
                changed += 1
            if "height_cm" in page:
                set_wattr(pg_sz, "h", cm_to_twips(page["height_cm"]))
                changed += 1
            if "orientation" in page:
                orient = str(page["orientation"])
                if orient in {"portrait", "landscape"}:
                    set_wattr(pg_sz, "orient", orient)
                    changed += 1
    return changed


def build_style_maps(styles_root: ET.Element) -> tuple[dict[str, ET.Element], dict[str, str]]:
    by_id: dict[str, ET.Element] = {}
    by_name: dict[str, str] = {}
    for style in styles_root.findall(qn("style")):
        style_id = get_wattr(style, "styleId")
        if not style_id:
            continue
        by_id[style_id] = style
        name_node = style.find(qn("name"))
        if name_node is not None:
            name = get_wattr(name_node, "val")
            if name:
                by_name[name] = style_id
    return by_id, by_name


def resolve_style(style_key: str, by_id: dict[str, ET.Element], by_name: dict[str, str]) -> ET.Element | None:
    if style_key in by_id:
        return by_id[style_key]
    style_id = by_name.get(style_key)
    return by_id.get(style_id) if style_id else None


def apply_run_props(style: ET.Element, spec: dict[str, Any]) -> int:
    changed = 0
    rpr = ensure_child(style, qn("rPr"))
    font_keys = {
        "font_east_asia": "eastAsia",
        "font_ascii": "ascii",
        "font_hansi": "hAnsi",
    }
    if any(key in spec for key in font_keys):
        rfonts = ensure_child(rpr, qn("rFonts"))
        for key, attr in font_keys.items():
            if key in spec:
                set_wattr(rfonts, attr, normalize_font(spec[key]))
                changed += 1
    if "size_pt" in spec:
        half_points = pt_to_half_points(spec["size_pt"])
        for tag in ("sz", "szCs"):
            sz = ensure_child(rpr, qn(tag))
            set_wattr(sz, "val", half_points)
            changed += 1
    if "bold" in spec:
        b = ensure_child(rpr, qn("b"))
        set_wattr(b, "val", "1" if spec["bold"] else "0")
        changed += 1
    if "italic" in spec:
        i = ensure_child(rpr, qn("i"))
        set_wattr(i, "val", "1" if spec["italic"] else "0")
        changed += 1
    return changed


def apply_paragraph_props(style: ET.Element, spec: dict[str, Any]) -> int:
    changed = 0
    ppr = ensure_child(style, qn("pPr"))
    if "alignment" in spec:
        jc = ensure_child(ppr, qn("jc"))
        set_wattr(jc, "val", spec["alignment"])
        changed += 1

    spacing_keys = {
        "space_before_pt",
        "space_after_pt",
        "line_multiple",
        "line_spacing_pt",
    }
    if any(key in spec for key in spacing_keys):
        spacing = ensure_child(ppr, qn("spacing"))
        if "space_before_pt" in spec:
            set_wattr(spacing, "before", pt_to_twips(spec["space_before_pt"]))
            changed += 1
        if "space_after_pt" in spec:
            set_wattr(spacing, "after", pt_to_twips(spec["space_after_pt"]))
            changed += 1
        if "line_multiple" in spec:
            set_wattr(spacing, "line", round(float(spec["line_multiple"]) * 240))
            set_wattr(spacing, "lineRule", "auto")
            changed += 1
        if "line_spacing_pt" in spec:
            set_wattr(spacing, "line", pt_to_twips(spec["line_spacing_pt"]))
            set_wattr(spacing, "lineRule", str(spec.get("line_rule", "exact")))
            changed += 1

    indent_keys = {"first_line_indent_twips", "first_line_indent_cm", "first_line_indent_chars", "left_indent_twips"}
    if any(key in spec for key in indent_keys):
        ind = ensure_child(ppr, qn("ind"))
        if "first_line_indent_twips" in spec:
            set_wattr(ind, "firstLine", int(spec["first_line_indent_twips"]))
            changed += 1
        elif "first_line_indent_cm" in spec:
            set_wattr(ind, "firstLine", cm_to_twips(spec["first_line_indent_cm"]))
            changed += 1
        elif "first_line_indent_chars" in spec:
            size_pt = float(spec.get("size_pt", 12))
            twips = round(float(spec["first_line_indent_chars"]) * size_pt * TWIPS_PER_PT)
            set_wattr(ind, "firstLine", twips)
            changed += 1
        if "left_indent_twips" in spec:
            set_wattr(ind, "left", int(spec["left_indent_twips"]))
            changed += 1
    return changed


def apply_style_contract(styles_root: ET.Element, contract: dict[str, Any]) -> tuple[int, list[str]]:
    style_specs = contract.get("styles")
    if not isinstance(style_specs, dict):
        return 0, []
    by_id, by_name = build_style_maps(styles_root)
    changed = 0
    missing: list[str] = []
    for style_key, spec in style_specs.items():
        if not isinstance(spec, dict):
            continue
        style = resolve_style(style_key, by_id, by_name)
        if style is None:
            missing.append(style_key)
            continue
        changed += apply_run_props(style, spec)
        changed += apply_paragraph_props(style, spec)
    return changed, missing


def copy_and_extract(input_docx: Path, work_dir: Path) -> None:
    with zipfile.ZipFile(input_docx) as zf:
        zf.extractall(work_dir)


def repack(work_dir: Path, output_docx: Path) -> None:
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in work_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(work_dir).as_posix())


def parse_xml(path: Path) -> ET.Element:
    return ET.fromstring(path.read_bytes())


def write_xml(path: Path, root: ET.Element) -> None:
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def apply_contract(input_docx: Path, contract_path: Path, output_docx: Path) -> dict[str, Any]:
    contract = read_json(contract_path)
    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        copy_and_extract(input_docx, work_dir)
        document_xml = work_dir / "word" / "document.xml"
        styles_xml = work_dir / "word" / "styles.xml"
        if not document_xml.exists():
            raise FileNotFoundError("word/document.xml")
        if not styles_xml.exists():
            raise FileNotFoundError("word/styles.xml")

        document_root = parse_xml(document_xml)
        styles_root = parse_xml(styles_xml)
        page_changes = apply_page_contract(document_root, contract)
        style_changes, missing_styles = apply_style_contract(styles_root, contract)
        write_xml(document_xml, document_root)
        write_xml(styles_xml, styles_root)
        repack(work_dir, output_docx)
    return {
        "input": str(input_docx),
        "output": str(output_docx),
        "contract": str(contract_path),
        "page_changes": page_changes,
        "style_changes": style_changes,
        "missing_styles": missing_styles,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Template/source DOCX.")
    parser.add_argument("--contract", required=True, help="format_contract.json.")
    parser.add_argument("--output", required=True, help="Output DOCX path.")
    parser.add_argument("--report", help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_docx = Path(args.input)
    contract_path = Path(args.contract)
    output_docx = Path(args.output)
    if not input_docx.exists():
        raise FileNotFoundError(input_docx)
    if not contract_path.exists():
        raise FileNotFoundError(contract_path)
    result = apply_contract(input_docx, contract_path, output_docx)
    report = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report + "\n", encoding="utf-8")
    print(report)
    return 1 if result["missing_styles"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
