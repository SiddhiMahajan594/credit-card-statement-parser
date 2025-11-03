# streamlit_app.py
import io
import json
from datetime import datetime

import streamlit as st
import pandas as pd

# import your parser package
from credit_parser.core import parse_fields, pdf_to_text
from credit_parser.tables import try_camelot, normalize_transactions

st.set_page_config(page_title="Card Statement Parser", page_icon="💳", layout="centered")

# --- Small helpers ---
def fmt_conf(c):
    if c is None: 
        return "—"
    if c >= 0.9: color = "green"
    elif c >= 0.75: color = "orange"
    else: color = "red"
    return f":{color}[{c:.2f}]"

def safe_float(v):
    try:
        return float(v)
    except Exception:
        return v

st.title("💳 Credit Card Statement Parser")
st.caption("Upload a statement PDF. We’ll extract issuer, last 4, statement period, due date, and balance. Optional: transactions table.")

# Sidebar options
with st.sidebar:
    st.header("Options")
    pages = st.number_input("Max pages to scan", min_value=1, max_value=50, value=8, step=1)
    do_transactions = st.checkbox("Extract transactions table(s)", value=False)
    st.markdown("---")
    st.caption("If your PDF is a scanned image, ensure **Tesseract** is installed for OCR fallback.")

uploaded = st.file_uploader("Drop a PDF here", type=["pdf"])

if uploaded is not None:
    st.info("Parsing… This can take a few seconds for multi-page or OCR-heavy PDFs.")
    with st.spinner("Reading and parsing…"):
        # Write uploaded to a temp buffer/file-like object
        # Streamlit gives us a BytesIO; pdfplumber can open file-like objects
        pdf_bytes = uploaded.read()
        tmp = io.BytesIO(pdf_bytes)

        # Extract full text for parser (core pipeline will OCR fallback if text is empty by page)
        # Note: pdf_to_text expects a path or file-like; pdfplumber works with file-like objects
        text = pdf_to_text(tmp, max_pages=pages, do_ocr_fallback=True)

        # Parse fields (issuer, last4, period, due date, balance)
        parsed = parse_fields(text)

        # Optional: transactions via Camelot (needs vector PDFs + ghostscript)
        txns = None
        if do_transactions:
            # Rewind buffer for Camelot (it needs a real path; workaround: write to temp)
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tf:
                tf.write(pdf_bytes)
                tf.flush()
                dfs = try_camelot(tf.name)
                norm = normalize_transactions(dfs)
                if norm:
                    txns = pd.concat(norm, ignore_index=True)
                parsed["transactions"] = [df.to_dict(orient="records") for df in norm] if norm else []

    # --- Results card ---
    st.subheader("Extracted Fields")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Issuer:** {parsed['issuer']['value'] or '—'} {fmt_conf(parsed['issuer'].get('confidence', 0))}")
        st.markdown(f"**Card last 4:** {parsed['last4']['value'] or '—'} {fmt_conf(parsed['last4']['confidence'])}")
        st.markdown(f"**Statement period:** {parsed['statement_period']['value'] or '—'} {fmt_conf(parsed['statement_period']['confidence'])}")

    with col2:
        st.markdown(f"**Payment due date:** {parsed['due_date']['value'] or '—'} {fmt_conf(parsed['due_date']['confidence'])}")
        bal = parsed['total_balance']['value']
        st.markdown(f"**Total / New balance:** {('' if bal is None else f'${bal:,.2f}')} {fmt_conf(parsed['total_balance']['confidence'])}")
        overall = parsed.get("confidence_overall", None)
        if overall is not None:
            st.markdown(f"**Overall confidence:** {fmt_conf(overall)}")

    # Optional: transactions table
    if do_transactions:
        st.subheader("Transactions")
        if txns is not None and len(txns):
            # Try to coerce amount to numeric for nicer display/sort
            if "amount" in txns.columns:
                txns["amount"] = txns["amount"].map(safe_float)
            st.dataframe(txns, use_container_width=True)
        else:
            st.caption("No transactions table detected (or extraction not supported for this PDF).")

    # --- Raw snippet (for debugging)
    with st.expander("Show raw text snippet (debug)"):
        st.code(parsed.get("sample_text_snippet", "")[:2000])

    # --- Download JSON
    st.subheader("Download")
    out = parsed.copy()
    # Avoid huge snippet in JSON by default; keep first ~1000 chars
    if "sample_text_snippet" in out:
        out["sample_text_snippet"] = out["sample_text_snippet"][:1000]

    json_bytes = json.dumps(out, indent=2, default=str).encode("utf-8")
    st.download_button(
        label="Download JSON",
        data=json_bytes,
        file_name=f"statement_parsed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

# else:
    # st.caption("Tip: If you don’t have a PDF yet, run `python make_sample_statement.py` to generate one in `samples/`.")
