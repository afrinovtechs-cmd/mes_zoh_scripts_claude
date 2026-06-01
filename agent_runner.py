import subprocess, pathlib, re, shutil
from typing import Generator

WORK_DIR = pathlib.Path(__file__).parent

def get_fail_tickers() -> list:
    v = WORK_DIR / "verdicts.md"
    if not v.exists():
        return []
    return re.findall(r'\|\s*(\S+)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*\*\*FAIL\*\*', v.read_text())

def claude_available() -> bool:
    return shutil.which("claude") is not None

def _prompt(tickers: list) -> str:
    cache = WORK_DIR / "cache" / "analyst-framework.md"
    framework = cache.read_text()[:2000] if cache.exists() else "Use Buffett shareholder letters framework."
    return (
        f"Warren Buffett portfolio audit. Working dir: {WORK_DIR}\n"
        f"Tickers: {', '.join(tickers)}\n\nFramework (cached):\n{framework}\n\n"
        "1. For each ticker write ./reports/[TICKER].md with moat/management/price analysis.\n"
        "2. Append Judge verdict (PASS/WATCH/FAIL) to each report.\n"
        "3. Write ./verdicts.md sorted FAIL->WATCH->PASS.\n"
        "Print one line per step: 'TICKER: status'. Do not stop until verdicts.md is written."
    )

def run_audit(tickers: list) -> Generator:
    (WORK_DIR / "portfolio.csv").write_text("\n".join(tickers))

    # ── Check Claude Code CLI is present ──────────────────────────────────
    if not claude_available():
        yield (
            "NO_CLAUDE_CLI|Claude Code CLI not found on this machine.\n"
            "Install it with:\n"
            "  npm install -g @anthropic-ai/claude-code\n"
            "(requires Node.js — download from https://nodejs.org)\n\n"
            "Falling back to last saved results..."
        )
        # Fallback: stream existing reports as read-only view
        for ticker in tickers:
            report = WORK_DIR / "reports" / f"{ticker}.md"
            if report.exists():
                yield f"📄 {ticker}: existing report found"
            else:
                yield f"⚠️  {ticker}: no report yet (run a live audit first)"
        verdicts = WORK_DIR / "verdicts.md"
        if verdicts.exists():
            yield "DONE"
        return

    # ── Live audit via Claude Code CLI ────────────────────────────────────
    yield f"Starting live audit: {', '.join(tickers)}"

    try:
        proc = subprocess.Popen(
            ["claude", "-p", _prompt(tickers)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, cwd=str(WORK_DIR)
        )
    except FileNotFoundError:
        yield "ERROR: claude CLI not found even after PATH check. Restart your terminal and try again."
        return

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
