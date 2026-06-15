import sys
from dataclasses import fields as dc_fields
from pathlib import Path
try:
    from .models import Article
    from .pipeline import run_pipeline
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pipeline.models import Article
    from pipeline.pipeline import run_pipeline

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SAMPLES = [
    DATA_DIR / "simontest.pdf",
    DATA_DIR / "testmultipages.pdf",
    DATA_DIR / "testhard.pdf",
]


def _eur(cents):
    return "-" if cents is None else f"{cents / 100:.2f}"


_CENT_FIELDS = {
    "predicted_pu_ht", "predicted_pu_ttc", "predicted_discount_amount",
    "predicted_tva_amount", "predicted_total_ttc",
}


def _fmt(field_name: str, value) -> str:
    if value is None:
        return "-"
    if field_name in _CENT_FIELDS:
        return _eur(value)
    if hasattr(value, "name"):
        return value.name
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _print_articles(articles: list[Article]):
    if not articles:
        return

    article_fields = dc_fields(Article)
    headers = [f.name.replace("predicted_", "") for f in article_fields]
    rows = [
        [_fmt(f.name, getattr(a, f.name)) for f in article_fields]
        for a in articles
    ]

    widths = [
        max(len(h), max(len(r[i]) for r in rows))
        for i, h in enumerate(headers)
    ]

    sep = "  " + "-" * (4 + sum(w + 2 for w in widths))
    print()
    print("  #  " + "  ".join(f"{h:<{w}}" for h, w in zip(headers, widths)))
    print(sep)
    for i, row in enumerate(rows, 1):
        print(f"  {i:>2}  " + "  ".join(f"{v:<{w}}" for v, w in zip(row, widths)))


def show(pdf_path: Path) -> None:
    res = run_pipeline(str(pdf_path))
    inv, rec = res.invoice, res.reconciliation

    print(f"\n{'=' * 80}\n {pdf_path.name}\n{'=' * 80}")
    print(
        f" vendor={inv.vendor_name!r}  invoice={inv.invoice_number!r}  pages={res.page_count}  buyer_firstname={inv.buyer_firstname}  buyer_lastname={inv.buyer_lastname}"
    )
    print(
        f" totals  HT={_eur(inv.total_price_without_taxes)}  "
        f"TVA={_eur(inv.taxes)}  TTC={_eur(inv.total_price_with_taxes)}"
    )
    print(
        f" articles={len(res.articles)}  dropped_rows={len(res.dropped)}  "
        f"needs_review={rec.needs_review}  reasons={rec.reasons}"
    )

    _print_articles(res.articles)


def main() -> None:
    targets = [Path(a) for a in sys.argv[1:]] or SAMPLES
    for pdf in targets:
        show(pdf)


if __name__ == "__main__":
    main()
