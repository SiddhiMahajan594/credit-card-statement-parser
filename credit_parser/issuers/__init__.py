from .base import BaseIssuerParser
from .amex import AmexParser
from .chase import ChaseParser
from .citi import CitiParser
from .bofa import BofaParser
from .capone import CapitalOneParser

PARSERS = [
    AmexParser(),
    ChaseParser(),
    CitiParser(),
    BofaParser(),
    CapitalOneParser(),
]

def pick_issuer_parser(text_lower: str):
    for p in PARSERS:
        if p.matches(text_lower):
            return p
    return BaseIssuerParser()
