import sys
from pathlib import Path

try:
    from .pipeline import run_pipeline
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pipeline.pipeline import run_pipeline

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SAMPLES = [DATA_DIR / "simontest.pdf", DATA_DIR / "testmultipages.pdf"]


def _eur(cents):
    return "-" if cents is None else f"{cents / 100:.2f}"


def show(pdf_path: Path) -> None:
    res = run_pipeline(str(pdf_path))
    inv, rec = res.invoice, res.reconciliation

    print(f"\n{'=' * 80}\n {pdf_path.name}\n{'=' * 80}")
    print(
        f" vendor={inv.vendor_name!r}  invoice={inv.invoice_number!r}  pages={res.page_count}"
    )
    print(
        f" totals  HT={_eur(inv.total_price_without_taxes)}  "
        f"TVA={_eur(inv.taxes)}  TTC={_eur(inv.total_price_with_taxes)}"
    )
    print(
        f" articles={len(res.articles)}  dropped_rows={len(res.dropped)}  "
        f"needs_review={rec.needs_review}  reasons={rec.reasons}"
    )

    print(
        "\n  # name                                          qty   pu_ttc    remise   tva%    total"
    )
    for i, a in enumerate(res.articles, 1):
        pu = a.predicted_pu_ttc if a.predicted_pu_ttc is not None else a.predicted_pu_ht
        print(
            f"  {i:>2} {(a.predicted_name or '')[:44]:<44} "
            f"{str(a.predicted_quantity or '-'):>3}  "
            f"{_eur(pu):>8}  {_eur(a.predicted_discount_amount):>7}  "
            f"{str(a.predicted_tva_percentage or '-'):>4}  {_eur(a.predicted_total_ttc):>8}"
        )

    for d in res.dropped:
        print(f"    dropped [p{d.page_index}] {d.reason:<18} {d.label!r}")


def main() -> None:
    targets = [Path(a) for a in sys.argv[1:]] or SAMPLES
    for pdf in targets:
        show(pdf)


if __name__ == "__main__":
    main()
