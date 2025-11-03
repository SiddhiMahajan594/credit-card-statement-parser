# 💳 Credit Card Statement Parser

A Python-based PDF parser that extracts key financial data from credit card statements across 5 major issuers.

## 🧭 Features
- Supports **Chase, Amex, Citi, Bank of America, Capital One**
- Extracts:
  - Issuer  
  - Card last 4 digits  
  - Statement period  
  - Payment due date  
  - Total / new balance  
- OCR fallback for scanned statements  
- Streamlit UI for demo + JSON export  
- Modular design for issuer-specific parsing  

## 🧰 Tech Stack
**Python, pdfplumber, pytesseract, regex, pandas, dateutil, Streamlit**

## ⚙️ How to Run

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python make_sample_statement.py
streamlit run streamlit_app.py
