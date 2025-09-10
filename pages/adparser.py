import streamlit as st
import pandas as pd

st.title("Airworthiness Directive (AD) Data")

# Structured AD data (extracted from PDF)
ad_data = {
    "AD-id": "2025-06-02",
    "Agency": "Federal Aviation Administration (FAA), DOT",
    "Effective date": "April 23, 2025",
    "Material incorporated by Reference": "777-57A0125 RB",
    "Superseding": "No",
    "Affected ADs": "None",
    "Applicability": ["The Boeing Company Model 777-200, -200LR, -300, -300ER, and 777F series airplanes"],
    "ATA": "57",
    "Service Bulletins": [
        {
            "SB-id": "B777-57A0125 RB",
            "SB Type": "Alert Requirements Bulletin",
            "Dated": "July 15, 2025",
            "Description": "Repetitive inspections for cracking of the upper wing skin and applicable on-condition actions"
        }
    ]
}

# Link to download the original AD PDF
st.markdown(
    """
    **[Download the original AD PDF here](https://ad.easa.europa.eu/ad/US-2025-06-02)**
    """,
    unsafe_allow_html=True
)

st.subheader("AD Information")
with st.expander("Show AD Details"):
    st.markdown(f"**AD ID:** {ad_data['AD-id']}")
    st.markdown(f"**Agency:** {ad_data['Agency']}")
    st.markdown(f"**Effective Date:** {ad_data['Effective date']}")
    st.markdown(f"**Material Incorporated by Reference:** {ad_data['Material incorporated by Reference']}")
    st.markdown(f"**Superseding:** {ad_data['Superseding']}")
    st.markdown(f"**Affected ADs:** {ad_data['Affected ADs']}")
    st.markdown(f"**ATA:** {ad_data['ATA']}")

st.subheader("Applicability")
with st.expander("Show Applicability"):
    for airplane_model in ad_data["Applicability"]:
        st.markdown(f"- {airplane_model}")

st.subheader("Service Bulletins")
if ad_data.get("Service Bulletins"):
    with st.expander("Show Service Bulletins"):
        for sb in ad_data["Service Bulletins"]:
            st.markdown(f"**SB-id:** {sb['SB-id']}")
            st.markdown(f"**Description:** {sb['Description']}")