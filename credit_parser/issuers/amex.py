import re
from .base import BaseIssuerParser
from ..confidence import calibrate

class AmexParser(BaseIssuerParser):
    name = "American Express"
    KEYWORDS = ["american express", "amex", "member since"]

    # AMEX often phrases "Account ending" and "New Balance" prominently
    PAT_LAST4 = [
        r'account (?:number )?ending(?: in)?\s*[:\-]?\s*(\d{4})',
        r'\*{4,}\s*(\d{4})'
    ]

    PAT_DUE = [
        r'payment due(?: date)?\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})'
    ]

    def extract_last4(self, text: str):
        for p in self.PAT_LAST4:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return m.group(1), calibrate(True, "regex")
        return super().extract_last4(text)
