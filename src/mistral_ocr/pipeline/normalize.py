import re
import unicodedata
from typing import Optional


def normalize_text(value: str) -> str:
    if not value:
        return ""
    decomposed = unicodedata.normalize("NFKD", value)
    no_accents = "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", no_accents.lower())).strip()


def parse_number(value: object) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None

    cleaned = re.sub(r"[^\d.,-]", "", value)
    if not cleaned:
        return None

    sign = -1.0 if cleaned.startswith("-") else 1.0
    cleaned = cleaned.lstrip("-")
    if not cleaned:
        return None

    comma, dot = cleaned.rfind(","), cleaned.rfind(".")
    if comma > -1 and dot > -1:
        cleaned = (
            cleaned.replace(".", "").replace(",", ".")
            if comma > dot
            else cleaned.replace(",", "")
        )
    elif comma > -1:
        decimals = cleaned.split(",")[-1]
        # "1,299" is 1299 (grouping); "1,17" is 1.17 (decimal).
        cleaned = (
            cleaned.replace(",", "")
            if cleaned.count(",") == 1 and len(decimals) == 3
            else cleaned.replace(",", ".")
        )

    try:
        return sign * float(cleaned)
    except ValueError:
        return None


def to_cents(value: object) -> Optional[int]:
    parsed = parse_number(value)
    return round(parsed * 100) if parsed is not None else None


def to_quantity(value: object) -> Optional[int]:
    parsed = parse_number(value)
    return round(abs(parsed)) if parsed is not None else None


def to_percent(value: object) -> Optional[float]:
    parsed = parse_number(value)
    return abs(parsed) if parsed is not None else None


def has_number(value: object) -> bool:
    return bool(value) and bool(re.search(r"\d", str(value)))
