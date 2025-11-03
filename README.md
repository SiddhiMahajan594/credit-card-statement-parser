# Credit Card Statement Parser

Rule-based PDF parser with OCR fallback for extracting:
- Issuer
- Card last 4 digits
- Statement period (start–end)
- Payment due date
- Total/New balance

Optional: transactions table extraction via Camelot (vector PDFs).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Parse a PDF
python -m credit_parser.cli samples/your_statement.pdf

# With transactions (requires camelot deps)
python -m credit_parser.cli samples/your_statement.pdf --transactions
