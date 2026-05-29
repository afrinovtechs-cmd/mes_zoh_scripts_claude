import subprocess, pathlib, re
from typing import Generator

WORK_DIR = pathlib.Path(__file__).parent

def get_fail_tickers() -> list:
    v = WORK_DIR / "verdicts.md"
    if not v.exists():
        return []
    return re.findall(r'\|\s*(\S+)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*\*\*FAIL\*\*', v.read_text())

def _prompt(tickers: list) -> str:
    cache = (WORK_DIR / "cache" / "analyst-framework.md")
    framework = cache.read_text()[:2000] if cache.exists() else "Use Buffett shareholder letters framework."
    return f"""Warren Buffett portfolio audit. Working dir: {WORK_DIR}
Tickers to audit: {', '.join(tickers)}

Buffett framework summary (from cache):
{framework}

Instructions:
1. For each ticker write ./reports/[TICKER].md with moat/management/price analysis.
2. Append Judge verdict (PASS/WATCH/FAIL) to each report.
3. Write ./verdicts.md sorted FAIL->WATCH->PASS.
Print one progress line per step: "TICKER: action done"
Do not stop until verdicts.md is written."""

def run_audit(tickers: list) -> Generator:
    (WORK_DIR / "portfolio.csv").write_text("\n".join(tickers))
    yield f"Starting audit for: {', '.join(tickers)}"

    proc = subprocess.Popen(
        ["claude", "-p", _prompt(tickers)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, cwd=str(WORK_DIR)
    )

    verdict_re = re.compile(r'(PASS|FAIL|WATCH)', re.I)
    for line in iter(proc.stdout.readline, ""):
        line = line.strip()
        if not line:
            continue
        if verdict_re.search(line):
            yield f"→ {line}"
        elif any(t in line for t in tickers):
            yield line

    proc.wait()
    err = proc.stderr.read()
    if proc.returncode != 0:
        if "403" in err or "auth" in err.lower() or "login" in err.lower():
            yield "AUTH_EXPIRED"
        else:
            yield f"ERROR: {err[:300]}"
        return
    yield "DONE"
