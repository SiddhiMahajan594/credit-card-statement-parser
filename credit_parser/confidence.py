def combine(*scores):
    """Combine confidence scores (0-1) using a simple average of non-zero entries."""
    vals = [s for s in scores if s and s > 0]
    return round(sum(vals) / len(vals), 3) if vals else 0.0


def calibrate(value_found: bool, method: str = "regex"):
    """Tiny helper to provide a baseline by method."""
    base = {
        "regex": 0.9,
        "heuristic": 0.75,
        "ocr": 0.7,
        "fuzzy": 0.6,
        "guess": 0.3,
    }.get(method, 0.5)
    return base if value_found else 0.0
