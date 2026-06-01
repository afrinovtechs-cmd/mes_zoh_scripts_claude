import re
import pathlib

_ALL_WORDS = re.compile(r'\b(all|tout|portfolio|full|complet)\b', re.I)
_FAIL_WORDS = re.compile(r'\b(fail|failed|échoué|rerun|re.run|relance)\b', re.I)
_MOAT = re.compile(r'\bmoat\b', re.I)
_MGMT = re.compile(r'\b(management|mgmt|gestion)\b', re.I)
_PRICE = re.compile(r'\b(price|prix|valuation|valorisation)\b', re.I)

def _load_tickers() -> list:
    p = pathlib.Path("portfolio.csv")
    if not p.exists():
        return []
    return [t.strip().upper() for t in p.read_text().splitlines() if t.strip()]

def parse_intent(msg: str) -> dict:
    upper = msg.upper()
    known = _load_tickers()

    # Filters
    filters = []
    if _MOAT.search(msg):   filters.append("moat")
    if _MGMT.search(msg):   filters.append("management")
    if _PRICE.search(msg):  filters.append("price")
    if not filters:
        filters = ["moat", "management", "price"]

    # Re-run FAILs
    if _FAIL_WORDS.search(msg):
        return {"action": "rerun_fails", "tickers": [], "filters": filters}

    # Explicit tickers mentioned in message
    mentioned = [t for t in known if re.search(rf'\b{re.escape(t)}\b', upper)]

    # "audit all portfolio"
    if _ALL_WORDS.search(msg) or not mentioned:
        if not known:
            return {"action": "clarify",
                    "question": "portfolio.csv is empty. Which tickers would you like to add?"}
        return {"action": "audit", "tickers": "all", "filters": filters}

    return {"action": "audit", "tickers": mentioned, "filters": filters}
