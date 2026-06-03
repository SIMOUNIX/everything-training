import re
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from bs4 import BeautifulSoup

from .normalize import normalize_text, parse_number

# TODO: define and explain the value of those
_AMOUNT_TOLERANCE = 0.01
_NAME_MATCH_THRESHOLD = 0.3
_NUMBER_CELL = re.compile(r"[\s\d.,%€$+\-()]+")
# Annotation fields whose value should appear among the matched row's cells.
_CHECKED_FIELDS = (
    "quantity",
    "unit_price_ht",
    "unit_price_ttc",
    "discount_amount",
    "tva_amount",
    "total_ttc",
)


@dataclass
class _HtmlRow:
    # this represent a line, tokens are string values such as the name and numbers are numerical values such as price
    tokens: Set[str]
    numbers: List[float]


@dataclass
class Verification:
    html_row_count: int = 0
    unmatched_article_names: List[str] = field(default_factory=list)  # invented by llm
    missed_html_rows: int = 0  # possibly skipped
    amount_mismatches: List[str] = field(default_factory=list)
    non_article_rows: List[Tuple[str, str]] = field(default_factory=list)


def _is_number_cell(text: str) -> bool:
    return bool(_NUMBER_CELL.fullmatch(text)) and any(c.isdigit() for c in text)


def _name_tokens(text: str) -> Set[str]:
    # transform name from annotations result into normalized independant tokens to match with ocr result
    return set(normalize_text(text).split())


def _html_rows(pages: List[dict]) -> List[_HtmlRow]:
    rows: List[_HtmlRow] = []
    for page in pages:
        for html in page.get("tables", []):
            table = BeautifulSoup(html, "html.parser").find("table")
            if table is None:
                continue
            # <tr> ... </tr> are all lines
            for tr in table.find_all("tr")[1:]:
                # cells are between <th> ... </th> or <td> ... </td>, h is for header and d is for cell containing data
                cells = tr.find_all(["td", "th"])
                # TODO: to define under
                if any(int(c.get("colspan", 1) or 1) > 1 for c in cells):
                    continue  # structural summary row
                texts = [c.get_text(" ", strip=True) for c in cells]
                tokens = _name_tokens(
                    " ".join(t for t in texts if not _is_number_cell(t))
                )
                numbers = [parse_number(t) for t in texts if _is_number_cell(t)]
                numbers = [n for n in numbers if n is not None]
                if tokens and numbers:  # a name and at least one amount
                    rows.append(_HtmlRow(tokens, numbers))
    return rows


def _best_match(tokens: Set[str], rows: List[_HtmlRow]) -> Optional[_HtmlRow]:
    best, best_score = None, 0.0
    for row in rows:
        # TODO: explaine me this, is it to compare the length of union and see if similar to both of the inputs -> making them the same tokens?
        union = tokens | row.tokens
        if union:
            score = len(tokens & row.tokens) / len(union)
            if score > best_score:
                best, best_score = row, score
    return best if best_score >= _NAME_MATCH_THRESHOLD else None


def _present(value: float, numbers: List[float]) -> bool:
    return any(abs(abs(value) - abs(n)) <= _AMOUNT_TOLERANCE for n in numbers)


# TODO: explain me more this function
def verify(annotation: dict, pages: List[dict]) -> Verification:
    available = _html_rows(pages)
    report = Verification(html_row_count=len(available))

    # Annotation class contains rows if articles were found
    for row in annotation.get("rows", []):
        name = row.get("name") or ""
        is_article = row.get("kind") == "article"
        if not is_article:
            report.non_article_rows.append((name, row.get("kind") or "unknown"))

        match = _best_match(_name_tokens(name), available)
        if match is not None:
            available.remove(match)  # consume the row whatever its kind
        elif is_article:
            report.unmatched_article_names.append(name)
            continue

        if is_article and match is not None:
            for field_name in _CHECKED_FIELDS:
                value = parse_number(row.get(field_name))
                if value is not None and not _present(value, match.numbers):
                    report.amount_mismatches.append(f"{name}: {field_name}={value}")

    # HTML rows nobody claimed are line items the annotation may have skipped.
    report.missed_html_rows = len(available)
    return report
