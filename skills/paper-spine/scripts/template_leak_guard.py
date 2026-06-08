#!/usr/bin/env python3
"""Detect leakage from structure-only exemplars into a final report.

The guard is intentionally dependency-free. It supports plain text/Markdown/
LaTeX, DOCX, and simple XLSX text extraction. It is a screening tool: shared
numbers are warnings unless evidence files also contain them; copied passages
and formulas are blocking findings.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
import zipfile
from dataclasses import dataclass
from bisect import bisect_left, bisect_right
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


TEXT_EXTS = {".txt", ".md", ".markdown", ".tex", ".csv", ".tsv", ".json", ".xml"}
DOCX_PART_RE = re.compile(r"word/(document|header\d+|footer\d+|footnotes|endnotes)\.xml$")
NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


@dataclass(frozen=True)
class SourceText:
    path: Path
    text: str


@dataclass(frozen=True)
class PassageHit:
    score: float
    final_path: Path
    exemplar_path: Path
    final_text: str
    exemplar_text: str


def read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_docx(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not DOCX_PART_RE.match(name):
                continue
            root = ET.fromstring(zf.read(name))
            for node in root.iter():
                if node.tag in (NS_W + "t", NS_W + "delText", NS_W + "instrText"):
                    if node.text:
                        chunks.append(node.text)
                elif node.tag == NS_W + "tab":
                    chunks.append("\t")
                elif node.tag in (NS_W + "br", NS_W + "cr", NS_W + "p"):
                    chunks.append("\n")
    return "".join(chunks)


def extract_xlsx(path: Path) -> str:
    chunks: list[str] = []
    shared: list[str] = []
    with zipfile.ZipFile(path) as zf:
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.iter(NS_MAIN + "si"):
                parts = [t.text or "" for t in si.iter(NS_MAIN + "t")]
                shared.append("".join(parts))
        for name in zf.namelist():
            if not name.startswith("xl/worksheets/") or not name.endswith(".xml"):
                continue
            root = ET.fromstring(zf.read(name))
            for c in root.iter(NS_MAIN + "c"):
                t = c.attrib.get("t")
                value = c.find(NS_MAIN + "v")
                if value is None or value.text is None:
                    inline = c.find(NS_MAIN + "is")
                    if inline is not None:
                        chunks.extend(tn.text or "" for tn in inline.iter(NS_MAIN + "t"))
                        chunks.append("\n")
                    continue
                if t == "s":
                    try:
                        chunks.append(shared[int(value.text)])
                    except (ValueError, IndexError):
                        chunks.append(value.text)
                else:
                    chunks.append(value.text)
                chunks.append("\n")
    return "".join(chunks)


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTS:
        return read_text_file(path)
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".xlsx":
        return extract_xlsx(path)
    raise ValueError(f"Unsupported file type: {path}")


def load_sources(paths: Iterable[Path]) -> list[SourceText]:
    sources: list[SourceText] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        text = extract_text(path)
        sources.append(SourceText(path=path, text=text))
    return sources


def norm_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def compact_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", "", text)


def split_passages(source: SourceText, min_chars: int) -> list[tuple[Path, str, str]]:
    raw = unicodedata.normalize("NFKC", source.text)
    parts = re.split(r"(?<=[。！？!?；;])|\n+", raw)
    out: list[tuple[Path, str, str]] = []
    seen: set[str] = set()
    for part in parts:
        clean = norm_text(part)
        compact = compact_text(clean)
        if len(compact) < min_chars:
            continue
        if compact in seen:
            continue
        if not re.search(r"[\w\u4e00-\u9fff]", compact):
            continue
        seen.add(compact)
        out.append((source.path, clean, compact))
    return out


def find_passage_hits(
    finals: list[SourceText],
    exemplars: list[SourceText],
    min_chars: int,
    threshold: float,
    limit: int,
) -> list[PassageHit]:
    final_passages = [p for src in finals for p in split_passages(src, min_chars)]
    exemplar_passages = [p for src in exemplars for p in split_passages(src, min_chars)]
    hits: list[PassageHit] = []

    final_exact: dict[str, tuple[Path, str, str]] = {}
    for item in final_passages:
        final_exact.setdefault(item[2], item)
    for ex_path, ex_text, ex_compact in exemplar_passages:
        exact = final_exact.get(ex_compact)
        if exact is not None:
            fn_path, fn_text, _ = exact
            hits.append(PassageHit(1.0, fn_path, ex_path, fn_text, ex_text))

    # Similarity pass: compare only passages with roughly compatible lengths.
    # This keeps large reports from degenerating into all-pairs matching.
    exemplar_index = sorted((len(item[2]), idx) for idx, item in enumerate(exemplar_passages))
    exemplar_lengths = [length for length, _ in exemplar_index]
    for fn_path, fn_text, fn_compact in final_passages:
        fn_len = len(fn_compact)
        lower = max(min_chars, int(fn_len * 0.55) - 80)
        upper = int(fn_len * 1.85) + 80
        start = bisect_left(exemplar_lengths, lower)
        end = bisect_right(exemplar_lengths, upper)
        for _, ex_idx in exemplar_index[start:end]:
            ex_path, ex_text, ex_compact = exemplar_passages[ex_idx]
            if fn_compact == ex_compact:
                continue
            max_len = max(len(fn_compact), len(ex_compact))
            if abs(len(fn_compact) - len(ex_compact)) > max(80, int(max_len * 0.45)):
                continue
            matcher = SequenceMatcher(None, fn_compact, ex_compact, autojunk=False)
            if matcher.quick_ratio() < threshold:
                continue
            score = matcher.ratio()
            if score >= threshold:
                hits.append(PassageHit(score, fn_path, ex_path, fn_text, ex_text))
                if len(hits) >= limit * 5:
                    break
        if len(hits) >= limit * 5:
            break

    dedup: dict[tuple[Path, Path, str, str], PassageHit] = {}
    for hit in hits:
        key = (
            hit.final_path,
            hit.exemplar_path,
            compact_text(hit.final_text)[:120],
            compact_text(hit.exemplar_text)[:120],
        )
        old = dedup.get(key)
        if old is None or hit.score > old.score:
            dedup[key] = hit
    return sorted(dedup.values(), key=lambda h: h.score, reverse=True)[:limit]


FORMULA_PATTERNS = [
    re.compile(r"\$\$.*?\$\$", re.S),
    re.compile(r"\\\[.*?\\\]", re.S),
    re.compile(r"\\begin\{(?:equation|align|gather)\*?\}.*?\\end\{(?:equation|align|gather)\*?\}", re.S),
    re.compile(r"\$[^$\n]{4,}\$"),
]
FORMULA_LINE_RE = re.compile(r"[=+\-*/^_×÷≤≥≈≠∑√∫]|\\frac|\\sum|\\sqrt|\\alpha|\\beta|\\gamma")
FORMULA_SYMBOL_RE = re.compile(r"[=+\-*/^_×÷≤≥≈≠∑√∫(){}\[\]\\]")
LATIN_WORD_RE = re.compile(r"[A-Za-z]{3,}")


def extract_formulas(text: str) -> set[str]:
    formulas: set[str] = set()
    for pattern in FORMULA_PATTERNS:
        for match in pattern.finditer(text):
            compact = compact_text(match.group(0))
            if len(compact) >= 6:
                formulas.add(compact)
    for line in text.splitlines():
        clean = norm_text(line)
        compact = compact_text(clean)
        if len(compact) < 8 or len(compact) > 240:
            continue
        if FORMULA_LINE_RE.search(compact) and re.search(r"\d|[A-Za-z]", compact):
            symbol_count = len(FORMULA_SYMBOL_RE.findall(compact))
            latin_words = len(LATIN_WORD_RE.findall(clean))
            has_cjk = bool(re.search(r"[\u4e00-\u9fff]", clean))
            if symbol_count < 2:
                continue
            if latin_words >= 5 or (has_cjk and len(compact) > 80):
                continue
            formulas.add(compact)
    return {f for f in formulas if not any(f != other and f in other for other in formulas)}


NUMBER_RE = re.compile(
    r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:\s*(?:m3/s|m³/s|m/s|mm|cm|km|ha|m2|m²|m3|m³|mg/L|%|‰|万元|元|分|级|年|月|日|人|组|项|次|h|d|m))?"
)


def extract_numbers(text: str) -> set[str]:
    nums: set[str] = set()
    for match in NUMBER_RE.finditer(unicodedata.normalize("NFKC", text)):
        token = re.sub(r"\s+", "", match.group(0))
        bare = re.sub(r"[^\d.]", "", token)
        if not bare:
            continue
        has_unit = bool(re.search(r"[^\d.+-]", token))
        distinctive = "." in bare or has_unit or len(bare) >= 3
        if distinctive:
            nums.add(token)
    return nums


def shared_formulas(
    finals: list[SourceText], exemplars: list[SourceText], evidence: list[SourceText]
) -> list[str]:
    final_set = set().union(*(extract_formulas(src.text) for src in finals))
    exemplar_set = set().union(*(extract_formulas(src.text) for src in exemplars))
    evidence_set = set().union(*(extract_formulas(src.text) for src in evidence)) if evidence else set()
    return sorted((final_set & exemplar_set) - evidence_set, key=len, reverse=True)[:50]


def shared_numbers(
    finals: list[SourceText], exemplars: list[SourceText], evidence: list[SourceText]
) -> list[str]:
    final_set = set().union(*(extract_numbers(src.text) for src in finals))
    exemplar_set = set().union(*(extract_numbers(src.text) for src in exemplars))
    evidence_set = set().union(*(extract_numbers(src.text) for src in evidence)) if evidence else set()
    return sorted((final_set & exemplar_set) - evidence_set)[:80]


def md_escape(text: str) -> str:
    text = html.escape(text, quote=False)
    text = text.replace("|", "\\|")
    return text


def truncate(text: str, n: int = 180) -> str:
    text = norm_text(text)
    return text if len(text) <= n else text[: n - 1] + "..."


def build_report(
    finals: list[SourceText],
    exemplars: list[SourceText],
    evidence: list[SourceText],
    passage_hits: list[PassageHit],
    formulas: list[str],
    numbers: list[str],
) -> tuple[str, str]:
    status = "PASS"
    if passage_hits or formulas:
        status = "FAIL"
    elif numbers:
        status = "WARN"

    lines: list[str] = []
    lines.append("# Template Leak Guard Report")
    lines.append("")
    lines.append(f"Status: **{status}**")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("Final files:")
    lines.extend(f"- `{src.path}`" for src in finals)
    lines.append("")
    lines.append("Structure-only exemplars:")
    lines.extend(f"- `{src.path}`" for src in exemplars)
    if evidence:
        lines.append("")
        lines.append("Evidence suppressors:")
        lines.extend(f"- `{src.path}`" for src in evidence)

    lines.append("")
    lines.append(f"## Copied Or Near-Copied Passages ({len(passage_hits)})")
    lines.append("")
    if passage_hits:
        lines.append("| Score | Final | Exemplar | Final text | Exemplar text |")
        lines.append("|---:|---|---|---|---|")
        for hit in passage_hits:
            lines.append(
                "| "
                f"{hit.score:.3f} | `{hit.final_path.name}` | `{hit.exemplar_path.name}` | "
                f"{md_escape(truncate(hit.final_text))} | {md_escape(truncate(hit.exemplar_text))} |"
            )
    else:
        lines.append("No copied or near-copied passages above the threshold.")

    lines.append("")
    lines.append(f"## Shared Formulas Not Found In Evidence ({len(formulas)})")
    lines.append("")
    if formulas:
        for formula in formulas:
            lines.append(f"- `{md_escape(truncate(formula, 220))}`")
    else:
        lines.append("No blocking shared formulas found.")

    lines.append("")
    lines.append(f"## Shared Distinctive Numbers Not Found In Evidence ({len(numbers)})")
    lines.append("")
    if numbers:
        lines.append(
            "These are warnings. Check whether each value is supported by the user's data, task book, standard, or a labelled assumption."
        )
        for number in numbers:
            lines.append(f"- `{md_escape(number)}`")
    else:
        lines.append("No distinctive shared numbers outside evidence files.")

    lines.append("")
    if status == "FAIL":
        lines.append(
            "Action: rewrite copied passages and replace exemplar-only formulas with values derived from requirement, evidence, reference, or labelled assumption sources."
        )
    elif status == "WARN":
        lines.append("Action: verify the shared numbers before final delivery.")
    else:
        lines.append("Action: no template leakage detected by this guard.")
    lines.append("")
    return status, "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="append", required=True, help="Final report file; repeat for multiple files.")
    parser.add_argument(
        "--exemplar",
        action="append",
        required=True,
        help="Structure-only exemplar/template/sample file; repeat for multiple files.",
    )
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="User evidence, task book, or data file whose numbers/formulas are allowed; repeat for multiple files.",
    )
    parser.add_argument("--output", help="Markdown report path.")
    parser.add_argument("--min-chars", type=int, default=28, help="Minimum compact passage length.")
    parser.add_argument("--similarity", type=float, default=0.92, help="Near-copy similarity threshold.")
    parser.add_argument("--limit", type=int, default=30, help="Maximum copied-passage hits in the report.")
    parser.add_argument(
        "--fail-on",
        choices=("fail", "warn", "never"),
        default="fail",
        help="Exit nonzero on FAIL, WARN, or never.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    finals = load_sources(Path(p) for p in args.final)
    exemplars = load_sources(Path(p) for p in args.exemplar)
    evidence = load_sources(Path(p) for p in args.evidence)

    passage_hits = find_passage_hits(finals, exemplars, args.min_chars, args.similarity, args.limit)
    formulas = shared_formulas(finals, exemplars, evidence)
    numbers = shared_numbers(finals, exemplars, evidence)
    status, report = build_report(finals, exemplars, evidence, passage_hits, formulas, numbers)

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
