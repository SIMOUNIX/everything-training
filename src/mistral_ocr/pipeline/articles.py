from typing import List, Optional

from .models import Article
from .normalize import to_cents, to_percent, to_quantity


def _abs_cents(value: object) -> Optional[int]:
    # in case the discount is written negative
    cents = to_cents(value)
    return abs(cents) if cents is not None else None


def _to_article(row: dict) -> Article:
    return Article(
        predicted_name=" ".join((row.get("name") or "").split()),
        predicted_quantity=to_quantity(row.get("quantity")),
        predicted_pu_ht=to_cents(row.get("unit_price_ht")),
        predicted_pu_ttc=to_cents(row.get("unit_price_ttc")),
        predicted_discount_amount=_abs_cents(row.get("discount_amount")),
        predicted_discount_percentage=to_percent(row.get("discount_percentage")),
        predicted_tva_percentage=to_percent(row.get("tva_percentage")),
        predicted_tva_amount=to_cents(row.get("tva_amount")),
        predicted_total_ttc=to_cents(row.get("total_ttc")),
    )


def articles_from_annotation(annotation: dict) -> List[Article]:
    return [
        _to_article(row)
        for row in annotation.get("rows", [])
        if row.get("kind") == "article"
    ]
