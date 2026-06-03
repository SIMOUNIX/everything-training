from .models import InvoicePrediction
from .normalize import to_cents


def build_invoice_prediction(annotation: dict) -> InvoicePrediction:
    return InvoicePrediction(
        vendor_name=annotation.get("vendor_name"),
        invoice_number=annotation.get("invoice_number"),
        total_price_without_taxes=to_cents(annotation.get("total_ht")),
        taxes=to_cents(annotation.get("total_tva")),
        total_price_with_taxes=to_cents(annotation.get("total_ttc")),
    )


def annotation_article_count(annotation: dict) -> int:
    return sum(r.get("kind") == "article" for r in annotation.get("rows", []))
