from .base import BaseIssuerParser

class CitiParser(BaseIssuerParser):
    name = "Citi"
    KEYWORDS = ["citi", "citibank", "citigroup"]
