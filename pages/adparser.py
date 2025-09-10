import streamlit as st
import pandas as pd

st.title("Airworthiness Directive (AD) Data")

# Structured AD data (extracted from PDF)
ad_data = {
    "AD-id": "2025-06-02",
    "Agency": "Federal Aviation Administration (FAA), DOT",
    "Effective date": "April 23, 2025",
    "Material incorporated by Reference": "Boeing Alert Requirements Bulletin 777-57A0125 RB, dated July 25, 2023",
    "Superseding": "No",
    "Affected ADs": "None",
    "Applicability": ["The Boeing Company Model 777-200, -200LR, -300, -300ER, and 777F series airplanes"],
    "ATA": "57 (Wings)",
    "Service Bulletins": [
        {
            "SB-id": "Boeing Alert Requirements Bulletin 777-57A0125 RB, dated July 25, 2023",
            "Description": "Repetitive inspections for cracking of the upper wing skin and applicable on-condition actions"
        }
    ]
}

# Show main AD information
st.subheader("AD Information")
main_fields = {k: v for k, v in ad_data.items() if k != "Service Bulletins"}
df_main = pd.DataFrame(list(main_fields.items()), columns=["Field", "Value"])
st.table(df_main)

# Show Service Bulletins table
if ad_data.get("Service Bulletins"):
    st.subheader("Service Bulletins")
    df_sbs = pd.DataFrame(ad_data["Service Bulletins"])
    st.table(df_sbs)