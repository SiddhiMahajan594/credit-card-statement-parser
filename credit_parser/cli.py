import sys, json, argparse
from .core import parse_statement
from .tables import try_camelot, normalize_transactions

def main():
    ap = argparse.ArgumentParser(description="Credit Card Statement Parser")
    ap.add_argument("pdf", help="Path to statement PDF")
    ap.add_argument("--pages", type=int, default=8, help="Max pages to scan")
    ap.add_argument("--transactions", action="store_true", help="Attempt to extract transactions table(s)")
    args = ap.parse_args()

    result = parse_statement(args.pdf, max_pages=args.pages)

    if args.transactions:
        dfs = try_camelot(args.pdf)
        norm = normalize_transactions(dfs)
        # convert to JSON-serializable
        result["transactions"] = [df.to_dict(orient="records") for df in norm]

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
