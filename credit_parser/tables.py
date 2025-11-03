import pandas as pd

def try_camelot(path: str, pages="1-end"):
    """Try extracting tables with camelot; return list of DataFrames or []."""
    try:
        import camelot  # optional
    except Exception:
        return []
    try:
        tables = camelot.read_pdf(path, pages=pages, flavor="lattice")
        dfs = [t.df for t in tables]
        # Basic cleanup heuristic: drop fully empty cols, rename columns
        cleaned = []
        for df in dfs:
            df2 = df.copy()
            df2.columns = [str(c).strip() or f"col_{i}" for i, c in enumerate(df2.columns)]
            df2 = df2.loc[:, ~df2.columns.duplicated()].copy()
            # Drop rows that are entirely empty
            df2 = df2.replace(r"^\s*$", None, regex=True).dropna(how="all")
            cleaned.append(df2.reset_index(drop=True))
        return cleaned
    except Exception:
        return []


def normalize_transactions(dfs):
    """Try to coerce a transactions DataFrame into (date, description, amount)."""
    normalized = []
    for df in dfs:
        dfc = df.copy()
        # Try best-effort column picking
        cols = [c.lower() for c in dfc.columns]
        date_col = next((c for c in dfc.columns if "date" in c.lower()), None)
        desc_col = next((c for c in dfc.columns if "desc" in c.lower() or "merchant" in c.lower() or "details" in c.lower()), None)
        amt_col = next((c for c in dfc.columns if "amount" in c.lower() or "amt" in c.lower() or "$" in c.lower()), None)
        if not all([date_col, desc_col, amt_col]):
            continue
        out = pd.DataFrame({
            "date": dfc[date_col].astype(str).str.strip(),
            "description": dfc[desc_col].astype(str).str.strip(),
            "amount": (dfc[amt_col]
                       .astype(str)
                       .str.replace("$", "", regex=False)
                       .str.replace(",", "", regex=False)
                       .str.replace("(", "-", regex=False)
                       .str.replace(")", "", regex=False))
        })
        # Coerce amount to float when possible
        def to_float(x):
            try:
                return float(x)
            except Exception:
                return None
        out["amount"] = out["amount"].map(to_float)
        normalized.append(out.dropna(how="all").reset_index(drop=True))
    return normalized
