from .articles import articles_from_annotation
from .globals_ import build_invoice_prediction
from .models import DroppedRow, PipelineResult, Reconciliation
from .ocr import run_ocr
from .verify import Verification, verify


def _reconcile(article_count: int, report: Verification) -> Reconciliation:
    reasons = []
    if article_count == 0:
        reasons.append("no_articles_found")
    if report.unmatched_article_names:
        reasons.append(f"unmatched_articles={len(report.unmatched_article_names)}")
    if report.missed_html_rows:
        reasons.append(f"possibly_missed_rows={report.missed_html_rows}")
    if report.amount_mismatches:
        reasons.append(f"amount_mismatches={len(report.amount_mismatches)}")

    return Reconciliation(
        deterministic_article_count=report.html_row_count,
        annotation_article_count=article_count,
        needs_review=bool(reasons),
        reasons=reasons + report.amount_mismatches,
    )


def run_pipeline(pdf_path: str, *, force_ocr: bool = False) -> PipelineResult:
    ocr = run_ocr(pdf_path, force=force_ocr)
    articles = articles_from_annotation(ocr.annotation)
    report = verify(ocr.annotation, ocr.pages)

    return PipelineResult(
        articles=articles,
        invoice=build_invoice_prediction(ocr.annotation),
        reconciliation=_reconcile(len(articles), report),
        dropped=[DroppedRow(-1, name, kind) for name, kind in report.non_article_rows],
        page_count=len(ocr.pages),
    )
