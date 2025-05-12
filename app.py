import streamlit as st
import pandas as pd
from supabase_client import supabase

st.set_page_config(page_title="Dashboard", layout="wide")

# Restrict access
if "user" not in st.session_state:
    st.warning("🔒 Please login at `/login`.")
    st.stop()

# Get user role
user_id = st.session_state.user.user.id
role_data = supabase.table("user_profiles").select("role").eq("id", user_id).execute().data
role = role_data[0]["role"] if role_data else "staff"

# Logout
st.sidebar.write(f"👋 {st.session_state.user.user.email}")
st.sidebar.write(f"🧑‍💼 Role: {role}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

# Navigation
menu = st.sidebar.radio("📂 Menu", ["Dashboard", "Customers", "Loans"])

# Dashboard
if menu == "Dashboard":
    st.header("📊 Overview")
    customers = supabase.table("customers").select("*").execute().data
    loans = supabase.table("loans").select("*").execute().data
    active = [l for l in loans if l["status"] == "active"]
    st.metric("Customers", len(customers))
    st.metric("Total Loans", len(loans))
    st.metric("Active Loans", len(active))

# Customers
elif menu == "Customers":
    st.header("👤 Add Customer")
    with st.form("add_customer"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        submit = st.form_submit_button("Add")
        if submit:
            supabase.table("customers").insert({
                "name": name,
                "email": email,
                "phone": phone,
                "address": address
            }).execute()
            st.success("Customer added!")

    st.subheader("📋 Customer List")
    data = supabase.table("customers").select("*").execute().data
    st.dataframe(pd.DataFrame(data))

# Loans
elif menu == "Loans":
    st.header("💰 Issue Loan")

    customers = supabase.table("customers").select("id, name").execute().data
    customer_map = {c["name"]: c["id"] for c in customers}
    selected_name = st.selectbox("Select Customer", list(customer_map.keys()))

    with st.form("add_loan"):
        amount = st.number_input("Amount", min_value=1000)
        rate = st.number_input("Interest Rate (%)", step=0.1)
        duration = st.number_input("Duration (months)", min_value=1)
        submit = st.form_submit_button("Create Loan")
        if submit:
            supabase.table("loans").insert({
                "customer_id": customer_map[selected_name],
                "amount": amount,
                "interest_rate": rate,
                "duration_months": duration
            }).execute()
            st.success("Loan added!")

    st.subheader("📄 All Loans")
    loans = supabase.table("loans").select("*").execute().data
    st.dataframe(pd.DataFrame(loans))
