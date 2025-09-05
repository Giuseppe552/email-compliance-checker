import streamlit as st
import pandas as pd
from utils.parser import analyze_email_df

st.set_page_config(page_title="Email Compliance Checker", layout="wide")

st.title("📧 Email Compliance Checker")
st.markdown("Upload a CSV file with email logs to analyze compliance risks.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = analyze_email_df(df)

    st.subheader("⚠️ Flagged Emails")
    st.dataframe(results[results["Flagged"] == True], use_container_width=True)

    st.subheader("📊 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Emails", len(results))
    col2.metric("Flagged Emails", results["Flagged"].sum())
    col3.metric("External Recipients", results["External"].sum())
else:
    st.info("Awaiting CSV upload...")

