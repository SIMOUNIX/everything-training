# Vehicle-invoice pipeline (Mistral OCR)

Extracts article line items + global fields from vehicle/bicycle purchase
invoices and produces records that map 1:1 onto the existing DB. Replaces the
old PaddleOCR + per-vendor-template + 735-line geometric extractor.

**Language-agnostic by design.** There is no French (or any-language) vocabulary
in the matching logic. The OCR annotation interprets headers and classifies rows
in whatever language the invoice uses, against a schema that mirrors the DB; the
HTML tables are used only as a language-neutral cross-check (product-name + number
matching, colspan structure).

## Flow

```
            run_pipeline(pdf_path)
                     │
            ┌────────▼─────────┐
            │  ocr.py (1 call) │   table_format="html"  +  document_annotation
            └───┬──────────┬───┘   (annotation schema mirrors the Article columns)
                │          │
       HTML tables      annotation rows (kind + DB-shaped fields, any language)
                │          │
                │     ┌────▼─────────┐   ┌──────────────┐
                │     │ articles.py  │   │ globals_.py  │
                │     │ kind==article│   │ vendor/totals│
                │     │  → Article   │   └──────────────┘
                │     └────┬─────────┘
        ┌───────▼───┐      │
        │ verify.py │◄─────┘   match articles to HTML rows by name,
        │ cross-chk │          check amounts, count colspan/missed rows
        └─────┬─────┘
        ┌─────▼──────┐
        │ pipeline.py│  needs_review if a row is unmatched (hallucinated),
        │            │  an HTML row is unclaimed (skipped), or an amount differs
        └────────────┘
```

## Modules

| File | Responsibility |
|------|----------------|
| `models.py` | `Article` (mirrors the `articles` table), `InvoicePrediction`, `Reconciliation`, `PipelineResult` |
| `ocr.py` | One Mistral OCR call (tables + annotation); annotation schema mirrors `Article`; cached by file hash |
| `normalize.py` | `"1.299,00"` / `"20 %"` → cents / float / int |
| `articles.py` | annotation rows where `kind == "article"` → `Article` |
| `globals_.py` | annotation → `InvoicePrediction` |
| `verify.py` | HTML tables as a language-neutral cross-check of the annotation |
| `pipeline.py` | orchestrator + reconciliation |
| `run.py` | CLI demo on `../data/*.pdf` |

## Why the annotation owns interpretation

Column meaning (HT vs TTC, amount vs %) and row type (article vs summary) are
language-dependent. Rather than maintain header-alias and stop-word lists per
language, the annotation schema is shaped like the DB (`unit_price_ht`,
`unit_price_ttc`, `discount_amount`, `tva_percentage`, …, plus a row `kind`), and
the model fills it from the headers in any language. `verify.py` then confirms,
without any vocabulary, that each annotation article maps to a real HTML table row
and that its amounts appear in that row's cells — flagging hallucinated rows,
skipped rows, and mis-transcribed amounts for human review.

## DB mapping (`Article` → `articles` table)

`Article` field names are the table's `predicted_*` columns. Money is integer
cents, percent is float, quantity is int — matching the Postgres column types.

| `Article` field | DB column | unit |
|-----------------|-----------|------|
| `predicted_name` | `predicted_name` | text |
| `predicted_quantity` | `predicted_quantity` | int |
| `predicted_pu_ht` / `predicted_pu_ttc` | same | cents |
| `predicted_discount_amount` | same | cents (magnitude) |
| `predicted_discount_percentage` | same | float |
| `predicted_tva_percentage` | same | float |
| `predicted_tva_amount` | same | cents |
| `predicted_total_ttc` | same | cents |
| `type` = `"NON_REFUNDABLE_ACCESSORY"`, `is_refundable` = `False` | same | const |

`Article.to_orm_kwargs()` returns exactly the kwargs for `Article(**kwargs)`; the
lambda then sets `document_id` / `created_by`.
`InvoicePrediction.to_prediction_payload()` returns the `{"global_info": {...}}`
shape consumed by `validate_document`.

## Run

```bash
# from src/mistral_ocr/pipeline/
uv run run.py                      # both sample PDFs
uv run run.py ../data/x.pdf        # one PDF

# tests (hermetic, no API call), from repo root
.venv/bin/python -m pytest src/mistral_ocr/pipeline/tests/ -q
```

OCR responses are cached in `pipeline/.ocr_cache/`; delete it (or pass
`force_ocr=True`) to re-call the API.

## Notes

- The annotation prompt in `ocr.py` lists summary-row *examples* (brut, acompte,
  …) only to convey the concept; the model generalises to other languages — they
  are not used as match rules anywhere.
- Amounts come from the annotation (generative) and are cross-checked against the
  exact HTML cells. A mismatch sets `needs_review` rather than being trusted.
