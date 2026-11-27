

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
        "todos": [{"task": t["text"], "completed": t["done"]} for t in st.session_state.todo_items],
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
