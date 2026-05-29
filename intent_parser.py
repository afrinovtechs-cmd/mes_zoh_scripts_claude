import anthropic, json, re, pathlib

def parse_intent(msg: str) -> dict:
    tickers = []
    p = pathlib.Path("portfolio.csv")
    if p.exists():
        tickers = [t.strip() for t in p.read_text().splitlines() if t.strip()]

    prompt = (
        "Intent parser for a stock audit assistant. Convert the user message to JSON.\n"
        'Schema: {"action":"audit|clarify|rerun_fails","tickers":["T1","T2"]|"all","filters":["moat","management","price"]}\n'
        'If ambiguous: {"action":"clarify","question":"..."}\n'
        f"Available tickers: {tickers}\n"
        "Return only valid JSON, no commentary.\n"
        f"User: {msg}"
    )
    resp = anthropic.Anthropic().messages.create(
        model="claude-haiku-4-5-20251001", max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    m = re.search(r'\{.*\}', resp.content[0].text, re.DOTALL)
    return json.loads(m.group()) if m else {"action": "clarify", "question": "Could you clarify your request?"}
