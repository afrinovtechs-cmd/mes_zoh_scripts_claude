import streamlit as st
import pathlib
from intent_parser import parse_intent
from agent_runner import run_audit, get_fail_tickers
from dashboard import generate_and_open

WORK_DIR = pathlib.Path(__file__).parent
VERDICTS = WORK_DIR / "verdicts.md"
PORTFOLIO = WORK_DIR / "portfolio.csv"

st.set_page_config(page_title="Buffett Audit Assistant", page_icon="📈")
st.title("📈 Buffett Audit Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
        "content": "I audit your portfolio against Buffett's framework. What do you want me to check?"}]
if "pending" not in st.session_state:
    st.session_state.pending = None

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

def add(role, text):
    st.session_state.messages.append({"role": role, "content": text})

if user_input := st.chat_input("e.g. 'Audit my full portfolio' or 'Re-run the FAIL stocks'"):
    add("user", user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        # ── Awaiting yes/no confirmation ──────────────────────────────────
        if st.session_state.pending:
            if user_input.lower().strip() in ("yes", "y", "oui", "ok"):
                plan = st.session_state.pending
                st.session_state.pending = None

                tickers = (plan["tickers"] if plan["tickers"] != "all"
                           else [t for t in PORTFOLIO.read_text().splitlines() if t.strip()])

                if not tickers:
                    msg = ("portfolio.csv is empty. Add tickers one per line, "
                           "then say 'audit my portfolio'.")
                    st.warning(msg); add("assistant", msg)
                else:
                    log = st.empty()
                    lines: list = []
                    done = False
                    for event in run_audit(tickers):
                        if event == "AUTH_EXPIRED":
                            msg = ("⚠️ NotebookLM auth expired. "
                                   "Run `notebooklm login` on your machine, then retry.")
                            st.error(msg); add("assistant", msg); break
                        elif event.startswith("NO_CLAUDE_CLI|"):
                            info = event.split("|", 1)[1]
                            st.warning(info); add("assistant", info)
                        elif event.startswith("ERROR:"):
                            st.error(event); add("assistant", event); break
                        elif event == "DONE":
                            done = True
                        else:
                            lines.append(event)
                            log.markdown("\n".join(f"- {l}" for l in lines[-12:]))

                    if done:
                        if VERDICTS.exists():
                            path = generate_and_open()
                            msg = f"✅ Audit complete! Dashboard opened. File: `{path}`"
                        else:
                            msg = "✅ Audit complete! Check `./reports/` for individual reports."
                        st.success(msg); add("assistant", msg)
            else:
                msg = "OK — what would you like to change?"
                st.markdown(msg); add("assistant", msg)
                st.session_state.pending = None

        # ── Parse fresh intent ────────────────────────────────────────────
        else:
            plan = parse_intent(user_input)
            action = plan.get("action")

            if action == "clarify":
                q = plan.get("question", "Could you clarify your request?")
                st.markdown(q); add("assistant", q)

            elif action == "rerun_fails":
                fails = get_fail_tickers()
                if not fails:
                    msg = "No FAIL stocks found in the last audit."
                    st.markdown(msg); add("assistant", msg)
                else:
                    plan = {"action": "audit", "tickers": fails,
                            "filters": ["moat", "management", "price"]}
                    filters = ", ".join(plan["filters"])
                    msg = (f"I'll re-audit the FAIL stocks: **{', '.join(fails)}** "
                           f"against {filters}. ~3 min/stock. Proceed? (yes/no)")
                    st.markdown(msg); add("assistant", msg)
                    st.session_state.pending = plan

            elif action == "audit":
                tickers = plan.get("tickers", "all")
                filters = ", ".join(plan.get("filters", ["moat", "management", "price"]))
                label = "all tickers in portfolio.csv" if tickers == "all" else f"**{', '.join(tickers)}**"
                msg = (f"I'll audit {label} against {filters}. "
                       f"~3 min/stock. Proceed? (yes/no)")
                st.markdown(msg); add("assistant", msg)
                st.session_state.pending = plan

            else:
                msg = "I didn't understand that. Try: 'Audit my portfolio' or 'Re-run the FAIL stocks'."
                st.markdown(msg); add("assistant", msg)
