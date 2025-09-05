import streamlit as st
import pandas as pd
from utils.parser import run_compliance_checks


st.set_page_config(page_title="Email Audit & Compliance Checker", layout="wide")
st.title("📧 Email Audit & Compliance Checker")


st.markdown("""
Upload a CSV of email logs to detect common compliance risks in communications.


**Expected columns:** `From`, `To`, `Subject`, `Timestamp`, `Body`
""")


uploaded = st.file_uploader("Upload email log CSV", type=["csv"])


if uploaded:
  df = pd.read_csv(uploaded)
flagged, stats = run_compliance_checks(df)


st.subheader("⚠️ Compliance Summary")
for k, v in stats.items():
  st.metric(k, v)


st.subheader("🚨 Flagged Emails")
st.dataframe(flagged, use_container_width=True)


st.download_button("Download flagged emails", flagged.to_csv(index=False), "flagged_emails.csv")


else:
st.info("Upload a file to begin.")
