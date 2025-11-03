import re
from dateutil import parser as dateparser
from ..confidence import calibrate

class BaseIssuerParser:
    """Base parser with generic regexes; issuer modules override as needed."""

    name = "Generic"

    # --- issuer detection keywords ---
    KEYWORDS = []  # override in subclasses

    # --- field patterns (override in subclasses for better accuracy) ---
    PAT_LAST4 = [
        r'(?:ending|ending in|ending with|ending:)\s*(\d{4})',
        r'card(?:\snumber)?(?:\sending)?[:\s]*\*+(\d{4})',
        r'\*{4,}\s*(\d{4})',
    ]

    PAT_PERIOD = [
        r'(statement period|billing period|statement from)\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})\s*(?:to|\-|–)\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})',
        r'([A-Za-z]+\s+\d{1,2},\s*\d{4}).{0,30}(?:to|-|–).{0,30}([A-Za-z]+\s+\d{1,2},\s*\d{4})'
    ]

    PAT_DUE = [
        r'(payment due date|due date|payment due)\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'due[^.\n]{0,60}([A-Za-z]+\s+\d{1,2},\s*\d{4})'
    ]

    PAT_BAL = [
        r'new balance\s*[:\-]?\s*\$?([\d,]+\.\d{2})',
        r'total balance\s*[:\-]?\s*\$?([\d,]+\.\d{2})',
        r'amount due\s*[:\-]?\s*\$?([\d,]+\.\d{2})',
        r'amount due by\s*[:\-]?\s*\$?([\d,]+\.\d{2})'
    ]

    def matches(self, text_lower: str) -> bool:
        return any(k in text_lower for k in self.KEYWORDS)

    def extract_last4(self, text: str):
        for p in self.PAT_LAST4:
            m = re.search(p, text, flags=re.IGNORECASE)
            if not m:
                continue
            digits = re.search(r'\d{4}', m.group(0))
            if digits:
                return digits.group(0), calibrate(True, "regex")
        return None, 0.0

    def extract_period(self, text: str):
        for p in self.PAT_PERIOD:
            m = re.search(p, text, flags=re.IGNORECASE)
            if not m:
                continue
            try:
                if len(m.groups()) >= 2:
                    start = dateparser.parse(m.group(len(m.groups()) - 1)).date()  # robust-ish
                    end = dateparser.parse(m.group(len(m.groups()))).date()
                    return f"{start.isoformat()} to {end.isoformat()}", calibrate(True, "regex")
            except Exception:
                continue
        return None, 0.0

    def extract_due(self, text: str):
        for p in self.PAT_DUE:
            m = re.search(p, text, flags=re.IGNORECASE)
            if not m:
                continue
            date_str = m.group(len(m.groups()))
            try:
                dt = dateparser.parse(date_str).date()
                return dt.isoformat(), calibrate(True, "regex")
            except Exception:
                continue
        return None, 0.0

    def extract_balance(self, text: str):
        for p in self.PAT_BAL:
            m = re.search(p, text, flags=re.IGNORECASE)
            if not m:
                continue
            amt = m.group(1) if m.lastindex else None
            if not amt:
                # fallback: any $ amount near keywords
                m2 = re.search(r'(new balance|total balance|amount due).{0,40}(\$[\d,]+\.\d{2})', text, flags=re.IGNORECASE)
                if not m2:
                    continue
                amt = m2.group(2)
            try:
                val = float(amt.replace("$", "").replace(",", ""))
                return val, calibrate(True, "regex")
            except Exception:
                continue
        return None, 0.0
