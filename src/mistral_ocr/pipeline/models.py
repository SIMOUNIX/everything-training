from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional


class ArticleType(Enum):
    VEHICLE = 1
    LOCK = 2
    REFUNDABLE_ACCESSORY = 3
    NON_REFUNDABLE_ACCESSORY = 4


@dataclass
class Article:
    """Line item mirroring the `articles` table. Money in integer cents."""

    predicted_name: Optional[str] = None
    predicted_quantity: Optional[int] = None
    predicted_pu_ht: Optional[int] = None
    predicted_pu_ttc: Optional[int] = None
    predicted_discount_amount: Optional[int] = None
    predicted_discount_percentage: Optional[float] = None
    predicted_tva_percentage: Optional[float] = None
    predicted_tva_amount: Optional[int] = None
    predicted_total_ttc: Optional[int] = None
    type: ArticleType = ArticleType.NON_REFUNDABLE_ACCESSORY
    is_refundable: bool = False

    def to_orm_kwargs(self) -> dict:
        return asdict(self)


@dataclass
class InvoicePrediction:
    vendor_name: Optional[str] = None
    buyer_firstname: Optional[str] = None
    buyer_lastname: Optional[str] = None
    invoice_number: Optional[str] = None
    total_price_without_taxes: Optional[int] = None
    taxes: Optional[int] = None
    total_price_with_taxes: Optional[int] = None

    def to_prediction_payload(self) -> dict:
        return {"global_info": {k: v for k, v in asdict(self).items() if v is not None}}


@dataclass
class Reconciliation:
    deterministic_article_count: int = 0
    annotation_article_count: int = 0
    sum_line_total_ttc: Optional[int] = None
    invoice_total_ttc: Optional[int] = None
    needs_review: bool = False
    reasons: List[str] = field(default_factory=list)


@dataclass
class DroppedRow:
    page_index: int
    label: str
    reason: str


@dataclass
class PipelineResult:
    articles: List[Article] = field(default_factory=list)
    invoice: InvoicePrediction = field(default_factory=InvoicePrediction)
    reconciliation: Reconciliation = field(default_factory=Reconciliation)
    dropped: List[DroppedRow] = field(default_factory=list)
    page_count: int = 0
