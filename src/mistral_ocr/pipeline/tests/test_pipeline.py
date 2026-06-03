from ..articles import articles_from_annotation
from ..normalize import parse_number
from ..verify import verify

PAGE = (
    "<table><tr><th>Description</th><th>Quantité</th><th>Prix</th><th>Montant</th></tr>"
    "<tr><td>Montage CXC</td><td>1</td><td>3330,00</td><td>3330,00</td></tr>"
    "<tr><td>Selle Italia</td><td>1</td><td>39,90</td><td>0,00</td></tr>"
    '<tr><td></td><td colspan="2">Total TTC</td><td>3330,00</td></tr></table>'
)


def test_number_parsing_eu_formats():
    assert parse_number("1,299") == 1299.0
    assert parse_number("1,17") == 1.17
    assert parse_number("3.330,00") == 3330.0
    assert parse_number("-105,30") == -105.30


def test_articles_from_annotation_maps_db_fields():
    annotation = {
        "rows": [
            {"kind": "article", "name": "VELO ELOPS", "quantity": 1,
             "unit_price_ttc": 1299.0, "tva_percentage": 20, "tva_amount": 216.5,
             "total_ttc": 1299.0},
            {"kind": "total", "name": "Total TTC", "total_ttc": 1299.0},
        ]
    }
    arts = articles_from_annotation(annotation)
    assert len(arts) == 1
    a = arts[0]
    assert a.predicted_quantity == 1
    assert a.predicted_pu_ttc == 129900
    assert a.predicted_pu_ht is None
    assert a.predicted_tva_amount == 21650
    assert a.predicted_total_ttc == 129900
    assert a.type == "NON_REFUNDABLE_ACCESSORY" and a.is_refundable is False


def test_discount_stored_as_positive_cents():
    annotation = {"rows": [
        {"kind": "article", "name": "X", "quantity": 1,
         "unit_price_ttc": 105.30, "discount_amount": -105.30, "total_ttc": 0.0},
    ]}
    assert articles_from_annotation(annotation)[0].predicted_discount_amount == 10530


def test_verify_counts_matches_and_flags():
    annotation = {"rows": [
        {"kind": "article", "name": "Montage CXC", "quantity": 1,
         "unit_price_ttc": 3330.0, "total_ttc": 3330.0},
        {"kind": "article", "name": "Selle Italia", "quantity": 1,
         "unit_price_ttc": 39.90, "total_ttc": 0.0},
        {"kind": "article", "name": "Ghost Part", "unit_price_ttc": 99.0},
        {"kind": "total", "name": "Total TTC", "total_ttc": 3330.0},
    ]}
    report = verify(annotation, [{"index": 0, "tables": [PAGE]}])

    assert report.html_row_count == 2                          # colspan summary excluded
    assert report.unmatched_article_names == ["Ghost Part"]    # hallucinated row caught
    assert report.missed_html_rows == 0                        # every html row claimed
    assert ("Total TTC", "total") in report.non_article_rows
    assert report.amount_mismatches == []


def test_verify_detects_mistranscribed_amount():
    annotation = {"rows": [
        {"kind": "article", "name": "Montage CXC", "quantity": 1,
         "unit_price_ttc": 9999.0, "total_ttc": 3330.0},
    ]}
    report = verify(annotation, [{"index": 0, "tables": [PAGE]}])
    assert any("unit_price_ttc" in m for m in report.amount_mismatches)


def test_orm_kwargs_match_db_columns():
    annotation = {"rows": [{"kind": "article", "name": "X", "quantity": 1,
                            "unit_price_ttc": 10.0}]}
    kwargs = articles_from_annotation(annotation)[0].to_orm_kwargs()
    assert set(kwargs) == {
        "predicted_name", "predicted_quantity", "predicted_pu_ht", "predicted_pu_ttc",
        "predicted_discount_amount", "predicted_discount_percentage",
        "predicted_tva_percentage", "predicted_tva_amount", "predicted_total_ttc",
        "type", "is_refundable",
    }
