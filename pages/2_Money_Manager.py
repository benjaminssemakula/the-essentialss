import json
from datetime import date, datetime

import pandas as pd
import streamlit as st

from essentials_theme import apply_theme, require_profile

apply_theme("Money Manager", "💰")
require_profile()

st.title("Money Manager")
st.markdown(
    '<p class="lede">Track the allowance you receive and the money you spend.</p>',
    unsafe_allow_html=True,
)

EXPENSE_CATEGORIES = ["Food", "Transport", "School", "Entertainment", "Shopping", "Other"]


def rp(amount):
    """10000 -> 'Rp 10 000'"""
    return f"Rp {int(amount):,}".replace(",", " ")


def rp_signed(kind, amount):
    """Allowance -> 'Rp. + 10 000', Expense -> 'Rp. - 10 000'"""
    sign = "+" if kind == "Allowance" else "-"
    return f"Rp. {sign} {int(amount):,}".replace(",", " ")


if "money_transactions" not in st.session_state:
    st.session_state.money_transactions = []

st.session_state.setdefault("money_source", "")
st.session_state.setdefault("money_in_amount", 10000)
st.session_state.setdefault("money_in_date", date.today())
st.session_state.setdefault("money_what", "")
st.session_state.setdefault("money_category", EXPENSE_CATEGORIES[0])
st.session_state.setdefault("money_out_amount", 10000)
st.session_state.setdefault("money_out_date", date.today())


def money_totals():
    txns = st.session_state.money_transactions
    income = sum(t["amount"] for t in txns if t["type"] == "Allowance")
    spent = sum(t["amount"] for t in txns if t["type"] == "Expense")
    return income, spent, income - spent


def add_allowance():
    s = st.session_state
    source = s.money_source.strip()
    amount = int(s.money_in_amount)
    if not source:
        s.money_msg = ("warning", "Tell me where the money came from.")
        return
    if amount <= 0:
        s.money_msg = ("warning", "The amount must be more than 0.")
        return
    s.money_transactions.append(
        {"date": s.money_in_date.isoformat(), "type": "Allowance",
         "description": source, "category": "Income", "amount": amount}
    )
    s.money_source, s.money_in_amount, s.money_in_date = "", 10000, date.today()
    s.money_msg = ("success", f"Saved {rp(amount)} from {source}.")


def add_expense():
    s = st.session_state
    what = s.money_what.strip()
    amount = int(s.money_out_amount)
    _, _, balance = money_totals()
    if not what:
        s.money_msg = ("warning", "Tell me what you spent money on.")
        return
    if amount <= 0:
        s.money_msg = ("warning", "The amount must be more than 0.")
        return
    if amount > balance:
        s.money_msg = ("warning", f"You only have {rp(balance)} left. Add allowance first.")
        return
    s.money_transactions.append(
        {"date": s.money_out_date.isoformat(), "type": "Expense",
         "description": what, "category": s.money_category, "amount": amount}
    )
    s.money_what, s.money_out_amount, s.money_out_date = "", 10000, date.today()
    s.money_msg = ("success", f"Saved expense of {rp(amount)} for {what}.")


money_income, money_spent, money_balance = money_totals()

# ---------- dashboard ----------
st.subheader("Money Dashboard")
m1, m2, m3 = st.columns(3)
with m1:
    with st.container(border=True):
        st.metric("Total Allowance", rp(money_income))
with m2:
    with st.container(border=True):
        st.metric("Total Expenses", rp(money_spent))
with m3:
    with st.container(border=True):
        st.metric("Remaining Balance", rp(money_balance))

if money_balance < 0:
    st.error("You have spent more than you received.")
elif money_income > 0 and money_balance < money_income * 0.2:
    st.warning("Your balance is running low. Spend carefully.")
else:
    st.success("You're doing well! Keep managing your money wisely.")

# ---------- record a transaction ----------
st.subheader("Record a Transaction")

with st.container(border=True):
    tab_in, tab_out = st.tabs(["Add Allowance", "Add Expense"])

    with tab_in:
        st.text_input("Where did the money come from?", placeholder="Example: Mom, birthday gift, savings",
                      key="money_source")
        a1, a2 = st.columns(2)
        with a1:
            st.number_input("Amount received (Rp)", min_value=0, step=1000, key="money_in_amount")
        with a2:
            st.date_input("Date received", key="money_in_date")
        st.button("Save Allowance", key="money_save_in", use_container_width=True,
                  type="primary", on_click=add_allowance)

    with tab_out:
        st.text_input("What did you spend money on?", placeholder="Example: Lunch, bus fare, notebook",
                      key="money_what")
        b1, b2 = st.columns(2)
        with b1:
            st.selectbox("Category", EXPENSE_CATEGORIES, key="money_category")
        with b2:
            st.number_input("Amount spent (Rp)", min_value=0, step=1000, key="money_out_amount")
        st.date_input("Date spent", key="money_out_date")
        st.button("Save Expense", key="money_save_out", use_container_width=True,
                  type="primary", on_click=add_expense)

money_msg = st.session_state.pop("money_msg", None)
if money_msg:
    getattr(st, money_msg[0])(money_msg[1])

# ---------- transaction history ----------
st.subheader("Transaction History")

money_rows = sorted(st.session_state.money_transactions, key=lambda t: t["date"], reverse=True)

if not money_rows:
    st.markdown('<p class="lede">No transactions yet. Save an allowance or an expense above.</p>',
                unsafe_allow_html=True)
else:
    st.table(
        pd.DataFrame(
            {
                "Date": [t["date"] for t in money_rows],
                "Type": [t["type"] for t in money_rows],
                "Description": [t["description"] for t in money_rows],
                "Category": [t["category"] for t in money_rows],
                "Amount": [rp_signed(t["type"], t["amount"]) for t in money_rows],
            }
        ).set_index("Date")
    )

# ---------- download ----------
st.subheader("Download your data")

export_rows = [
    {
        "Date": t["date"],
        "Type": t["type"],
        "Description": t["description"],
        "Category": t["category"],
        "Amount (Rp)": t["amount"] if t["type"] == "Allowance" else -t["amount"],
    }
    for t in money_rows
]
money_csv = pd.DataFrame(
    export_rows, columns=["Date", "Type", "Description", "Category", "Amount (Rp)"]
).to_csv(index=False)

money_json = json.dumps(
    {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "total_allowance": money_income,
            "total_expenses": money_spent,
            "remaining_balance": money_balance,
        },
        "transactions": export_rows,
        "todos": [
            {"task": t["text"], "completed": t["done"]}
            for t in st.session_state.get("todo_items", [])
        ],
    },
    indent=2,
    ensure_ascii=False,
)

d1, d2 = st.columns(2)
with d1:
    st.download_button("Download transactions (CSV)", data=money_csv, file_name="transactions.csv",
                       mime="text/csv", disabled=not money_rows)
with d2:
    st.download_button("Download all data (JSON)", data=money_json, file_name="all_data.json",
                       mime="application/json")
