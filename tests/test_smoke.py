import json, os, sys
from pathlib import Path

# allow running tests without install
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from credit_parser.core import parse_fields

def test_parse_fields_minimal():
    fake_text = """
    CHASE Card Services
    Statement Period: January 1, 2025 to January 31, 2025
    Payment Due Date: February 21, 2025
    New Balance: $1,234.56
    Account ending in 9876
    """
    out = parse_fields(fake_text)
    assert out["issuer"]["value"] in ("Chase", None)
    assert out["last4"]["value"] == "9876"
    assert "2025-01-01" in out["statement_period"]["value"]
    assert "2025-01-31" in out["statement_period"]["value"]
    assert out["due_date"]["value"] == "2025-02-21"
    assert abs(out["total_balance"]["value"] - 1234.56) < 1e-6
    assert out["confidence_overall"] > 0.6
