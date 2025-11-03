import re
from .base import BaseIssuerParser
from ..confidence import calibrate

class ChaseParser(BaseIssuerParser):
    name = "Chase"
    KEYWORDS = ["chase", "jpmorgan chase"]

    PAT_PERIOD = [
        r'(statement period|billing period)\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})\s*(?:to|\-|–)\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})'
    ]

    PAT_DUE = [
        r'payment due(?: date)?\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})',
        r'payment due by\s*[:\-]?\s*([A-Za-z]+\s+\d{1,2},?\s*\d{4})'
    ]

    PAT_BAL = [
        r'new balance(?:\s*due)?\s*[:\-]?\s*\$?([\d,]+\.\d{2})'
    ]
