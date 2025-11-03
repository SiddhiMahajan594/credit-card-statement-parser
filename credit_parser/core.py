import re
import pdfplumber
from .ocr import ocr_image
from .issuers import pick_issuer_parser
from .confidence import combine

def pdf_to_text(path, max_pages=8, do_ocr_fallback=True):
    pages_text = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            txt = page.extract_text() or ""
            txt = txt.strip()
            if not txt and do_ocr_fallback:
                # OCR fallback on a rendered page image
                im = page.to_image(resolution=300).original
                txt = ocr_image(im, psm=6, oem=3)
            if txt:
                pages_text.append(txt)
    return "\n\n".join(pages_text)


def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def detect_issuer_name(text_lower: str):
    # light heuristic; actual parser selection is done in pick_issuer_parser
    if "american express" in text_lower or "amex" in text_lower:
        return "American Express", 0.95
    if "chase" in text_lower:
        return "Chase", 0.95
    if "citibank" in text_lower or "citi" in text_lower:
        return "Citi", 0.95
    if "bank of america" in text_lower or "bofa" in text_lower:
        return "Bank of America", 0.95
    if "capital one" in text_lower:
        return "Capital One", 0.95
    return None, 0.0


def parse_fields(text: str):
    txt_norm = normalize_whitespace(text)
    lo = txt_norm.lower()

    # issuer detection + parser dispatch
    issuer_guess, issuer_conf = detect_issuer_name(lo)
    parser = pick_issuer_parser(lo)

    # field extraction (issuer-specific overrides)
    last4, c1 = parser.extract_last4(txt_norm)
    period, c2 = parser.extract_period(txt_norm)
    due, c3 = parser.extract_due(txt_norm)
    balance, c4 = parser.extract_balance(txt_norm)

    return {
        "issuer": {"value": issuer_guess or parser.name if parser.name != "Generic" else None, "confidence": issuer_conf or (0.8 if parser.name != "Generic" else 0.0)},
        "last4": {"value": last4, "confidence": c1},
        "statement_period": {"value": period, "confidence": c2},
        "due_date": {"value": due, "confidence": c3},
        "total_balance": {"value": balance, "confidence": c4},
        "sample_text_snippet": txt_norm[:2000],
        "confidence_overall": combine(c1, c2, c3, c4),
    }


def parse_statement(path: str, max_pages: int = 8):
    raw = pdf_to_text(path, max_pages=max_pages, do_ocr_fallback=True)
    return parse_fields(raw)
