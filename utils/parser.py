# File: utils/parser.py

import pandas as pd

SENSITIVE_TERMS = ["confidential", "password", "urgent wire", "ssn", "bank details"]
EXTERNAL_DOMAINS = ["@gmail.com", "@yahoo.com", "@outlook.com"]

def run_compliance_checks(df: pd.DataFrame):
    issues = []

    for idx, row in df.iterrows():
        row_issues = []
        body = str(row.get("Body", "")).lower()
        subject = str(row.get("Subject", "")).lower()
        to_field = str(row.get("To", "")).lower()

        # Check for sensitive keywords
        if any(term in body for term in SENSITIVE_TERMS):
            row_issues.append("Sensitive term")

        # Check for unapproved external recipients
        if any(domain in to_field for domain in EXTERNAL_DOMAINS):
            row_issues.append("External email")

        # Check blank subject or body
        if subject.strip() == "":
            row_issues.append("Blank subject")
        if body.strip() == "":
            row_issues.append("Blank body")

        if row_issues:
            issues.append({
                "From": row.get("From"),
                "To": to_field,
                "Subject": row.get("Subject"),
                "Body": row.get("Body"),
                "Timestamp": row.get("Timestamp"),
                "Flags": ", ".join(row_issues)
            })

    flagged_df = pd.DataFrame(issues)

    stats = {
        "Total Emails": len(df),
        "Flagged Emails": len(flagged_df),
        "Sensitive Terms": flagged_df["Flags"].str.contains("Sensitive term").sum(),
        "External Recipients": flagged_df["Flags"].str.contains("External email").sum(),
        "Blank Subjects": flagged_df["Flags"].str.contains("Blank subject").sum(),
    }

    return flagged_df, stats
