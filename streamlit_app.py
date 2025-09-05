# File: streamlit_app.py
import pandas as pd
import streamlit as st

# IMPORTANT: this matches your actual parser function name
from utils.parser import run_compliance_checks

st.set_page_config(page_title="Email Compliance Checker", page_icon="📧", layout="wide")

st.title("📧 Email Compliance Checker")
st.caption("Upload a CSV with columns: Timestamp, From, To, Subject, Body. (Case-sensitive)")

# ---- Sample CSV download (helps recruiters test instantly) ----
def sample_csv_bytes() -> bytes:
    df = pd.DataFrame([
        {
            "Timestamp": "2025-06-01 09:00",
            "From": "alice@company.com",
            "To": "bob@company.com",
            "Subject": "Quarterly report",
            "Body": "Please find attached. This is confidential."
        },
        {
            "Timestamp": "2025-06-01 10:15",
            "From": "alice@company.com",
            "To": "personal@gmail.com",
            "Subject": "",
            "Body": "Can you review this quickly?"
        },
        {
            "Timestamp": "2025-06-01 11:40",
            "From": "it@company.com",
            "To": "team@company.com",
            "Subject": "Password reset policy update",
            "Body": "Do not share your password. Unsubscribe link is in footer."
        },
    ])
    return df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download sample_emails.csv",
    data=sample_csv_bytes(),
    file_name="sample_emails.csv",
    mime="text/csv",
    type="secondary",
)

st.markdown("---")

# ---- File uploader ----
uploaded = st.file_uploader("Upload email CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV (or download the sample above) to continue.")
    st.stop()

# ---- Read CSV safely ----
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

# ---- Validate expected columns ----
required_cols = {"Subject", "Body"}
optional_cols = {"Timestamp", "From", "To"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(sorted(missing))}")
    st.markdown("**Required:** Subject, Body &nbsp;&nbsp; **Optional:** Timestamp, From, To")
    st.stop()

# ---- Run compliance checks (your function) ----
flagged_df, stats = run_compliance_checks(df)

# ---- KPI metrics ----
st.subheader("Summary")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Emails", stats.get("Total Emails", 0))
c2.metric("Flagged Emails", stats.get("Flagged Emails", 0))
c3.metric("Sensitive Terms", stats.get("Sensitive Terms", 0))
c4.metric("External Recipients", stats.get("External Recipients", 0))
c5.metric("Blank Subjects", stats.get("Blank Subjects", 0))

st.markdown("---")

# ---- Results table ----
st.subheader("Flagged Emails")
if flagged_df.empty:
    st.success("No compliance issues detected. ✅")
else:
    st.dataframe(flagged_df, use_container_width=True)

# ---- Raw data preview ----
with st.expander("Preview uploaded data"):
    st.dataframe(df.head(100), use_container_width=True)

