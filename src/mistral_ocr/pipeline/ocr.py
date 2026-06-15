import base64
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from mistralai.client import Mistral
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel, Field
from typing_extensions import Literal

from .models import ArticleType

_CACHE_DIR = Path(__file__).resolve().parent / ".ocr_cache"

# The model interprets headers in any language and fills the schema below (which
# mirrors the DB). It labels every row instead of dropping summaries itself, so
# omissions stay visible. Amounts are cross-checked against the HTML cells later.
ANNOTATION_PROMPT = (
    "This is a vehicle/bicycle purchase invoice whose line-item table may span "
    "several pages. Transcribe EVERY row of EVERY line-item table, in reading "
    "order, across ALL pages, in whatever language the invoice uses. Do NOT "
    "skip, merge or summarise any row. Set 'kind' per row: 'article' (a "
    "purchased product/service line; a fully-discounted line with total 0 is "
    "still an article; a row at the top/bottom of a page is still an article), "
    "'subtotal'/'total' (brut/net/HT/TVA/TTC summaries), 'deposit', 'payment', "
    "'footer' (free text/legal) or 'other'. Use the column headers to decide "
    "HT vs TTC and amount vs percentage. Copy every amount exactly as printed. "
    "For each article row set 'type' as follows — 1: vehicle/bike/scooter/e-bike "
    "(the main purchased vehicle); 2: lock/antitheft/cable; "
    "3: refundable accessory (accessory tightly/permanently attached to the bike — "
    "e.g. integrated lights, mudguards, built-in rack, permanently fixed lock); "
    "4: non-refundable accessory or anything else (easily removable items like helmet, "
    "bag, child seat, portable lock, service, insurance). "
    "For buyer information: extract the customer's first name into 'buyer_firstname' "
    "and last name into 'buyer_lastname' from the invoice header or billing address. "
    "If only a full name is shown, split it as 'Firstname Lastname'."
)


class _Row(BaseModel):
    # TODO: decide if we use predicted_ here or we concate that later before feeding the database
    kind: Literal[
        "article", "subtotal", "total", "deposit", "payment", "footer", "other"
    ]
    name: str
    quantity: Optional[float] = None
    unit_price_ht: Optional[float] = None
    unit_price_ttc: Optional[float] = None
    discount_amount: Optional[float] = None
    discount_percentage: Optional[float] = None
    tva_percentage: Optional[float] = None
    tva_amount: Optional[float] = None
    total_ttc: Optional[float] = None
    type: ArticleType = ArticleType.NON_REFUNDABLE_ACCESSORY


class _Annotation(BaseModel):
    # TODO: check naming w sharelock db
    vendor_name: Optional[str] = None
    buyer_firstname: Optional[str] = None
    buyer_lastname: Optional[str] = None
    invoice_number: Optional[str] = None
    total_ht: Optional[float] = None
    total_tva: Optional[float] = None
    total_ttc: Optional[float] = None
    rows: List[_Row] = Field(default_factory=list)


@dataclass
class OcrOutput:
    pages: List[dict]  # [{"index": int, "tables": [html, ...]}]
    annotation: dict


def _encode(pdf_path: str) -> str:
    return base64.b64encode(Path(pdf_path).read_bytes()).decode()


# TODO: remove force before moving code to sharelock, only to force ocr and not use the cache data
def run_ocr(pdf_path: str, *, force: bool = False) -> OcrOutput:
    # this will be replaced with direct bytes reading from aws s3
    digest = hashlib.sha1(Path(pdf_path).read_bytes()).hexdigest()[:16]

    # to remove before aws
    cache_path = _CACHE_DIR / f"{Path(pdf_path).stem}.{digest}.json"
    if cache_path.exists() and not force:
        cached = json.loads(cache_path.read_text())
        return OcrOutput(cached["pages"], cached["annotation"])
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{_encode(pdf_path)}",
        },
        table_format="html",
        document_annotation_format=response_format_from_pydantic_model(_Annotation),
        document_annotation_prompt=ANNOTATION_PROMPT,
        # we do not care about images
        include_image_base64=False,
    )

    pages = [
        {"index": p.index, "tables": [t.content for t in (p.tables or [])]}
        for p in response.pages
    ]
    # this is the output data in format _Annotation
    raw = response.document_annotation
    annotation = json.loads(raw) if isinstance(raw, str) else (raw or {})

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"pages": pages, "annotation": annotation}, ensure_ascii=False)
    )
    return OcrOutput(pages, annotation)
