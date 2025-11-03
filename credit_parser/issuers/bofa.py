from .base import BaseIssuerParser

class BofaParser(BaseIssuerParser):
    name = "Bank of America"
    KEYWORDS = ["bank of america", "bofa"]
