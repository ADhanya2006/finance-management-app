import streamlit as st
from supabase_client import supabase

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Finance App Login")

mode = st.radio("Select Mode", ["Login", "Sign Up"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if mode == "Sign Up":
    if st.button("Register"):
        try:
            user = supabase.auth.sign_up({"email": email, "password": password})
            if user.user:
                supabase.table("user_profiles").insert({
                    "id": user.user.id,
                    "role": "staff"
                }).execute()
                st.success("User registered! Please confirm email (if required).")
        except Exception as e:
            st.error(f"Signup failed: {e}")

elif mode == "Login":
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user.session:
                st.session_state.user = user
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
        except Exception as e:
            st.error(f"Login failed: {e}")
