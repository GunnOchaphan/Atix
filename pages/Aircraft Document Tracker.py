import streamlit as st
import pandas as pd
import json

# Use the data schema to generate synthetic data
def generate_synthetic_data():
    """Generates synthetic data for the Streamlit app based on the schema."""
    
    # Aircraft data based on a simplified Thai Airways fleet
    fleet_data = [
        {
            "aircraft_id": "A101",
            "registration": "HS-TKK",
            "manufacturer": "Boeing",
            "model": "777-300ER",
            "serial_number": "41682",
            "airworthiness_certificate_date": "2014-01-15",
            "status": "Active",
            "applicable_ads": ["AD-2025-06-02", "AD-2024-03-10"],
            "applicable_sbs": ["SB-777-28-001", "SB-777-57-0125"],
            "applicable_tos": ["TO-2023-A01"],
            "applicable_eds": ["ED-2024-01"]
        },
        {
            "aircraft_id": "A102",
            "registration": "HS-THB",
            "manufacturer": "Airbus",
            "model": "A350-900",
            "serial_number": "106",
            "airworthiness_certificate_date": "2016-09-01",
            "status": "Active",
            "applicable_ads": ["AD-2024-03-11"],
            "applicable_sbs": ["SB-A350-57-001"],
            "applicable_tos": ["TO-2023-A02"],
            "applicable_eds": ["ED-2024-02"]
        },
        {
            "aircraft_id": "A103",
            "registration": "HS-TQC",
            "manufacturer": "Boeing",
            "model": "787-8",
            "serial_number": "35308",
            "airworthiness_certificate_date": "2013-09-16",
            "status": "Active",
            "applicable_ads": ["AD-2024-03-10"],
            "applicable_sbs": [],
            "applicable_tos": [],
            "applicable_eds": ["ED-2024-01"]
        }
    ]

    # AD data, including compliance for specific aircraft
    ads_data = [
        {
            "document_id": "AD-2025-06-02",
            "title": "Wing Skin Inspection",
            "issuing_authority": "FAA",
            "ad_type": "Final Rule",
            "effective_date": "2025-04-23",
            "compliance_summary": "Repetitive inspections for cracking on the upper wing skin.",
            "compliance_status": [
                {"aircraft_id": "A101", "status": "Compliant", "last_completed_date": "2025-05-01", "next_due_date": "2026-05-01"}
            ],
            "applicability": {"aircraft_models": ["777-200", "777-300ER", "777F"], "serial_numbers": []},
            "referred_documents": {"service_bulletins": ["SB-777-57-0125"], "technical_orders": [], "engineering_directives": []}
        },
        {
            "document_id": "AD-2024-03-10",
            "title": "Engine Fire Suppression System",
            "issuing_authority": "EASA",
            "ad_type": "Emergency",
            "effective_date": "2024-03-10",
            "compliance_summary": "Inspection and possible replacement of fire suppression bottles.",
            "compliance_status": [
                {"aircraft_id": "A101", "status": "Compliant", "last_completed_date": "2024-03-15", "next_due_date": "N/A"},
                {"aircraft_id": "A103", "status": "Compliant", "last_completed_date": "2024-03-16", "next_due_date": "N/A"}
            ],
            "applicability": {"aircraft_models": ["777-300ER", "787-8"], "serial_numbers": []},
            "referred_documents": {"service_bulletins": [], "technical_orders": [], "engineering_directives": []}
        },
        {
            "document_id": "AD-2024-03-11",
            "title": "Landing Gear Actuator",
            "issuing_authority": "EASA",
            "ad_type": "Final Rule",
            "effective_date": "2024-03-15",
            "compliance_summary": "Replacement of a specific landing gear actuator part.",
            "compliance_status": [
                {"aircraft_id": "A102", "status": "Compliant", "last_completed_date": "2024-04-01", "next_due_date": "N/A"}
            ],
            "applicability": {"aircraft_models": ["A350-900"], "serial_numbers": []},
            "referred_documents": {"service_bulletins": [], "technical_orders": [], "engineering_directives": []}
        }
    ]

    # Service Bulletin data
    sbs_data = [
        {
            "document_id": "SB-777-28-001",
            "title": "Hydraulic Pump Seal Replacement",
            "issuing_authority": "Boeing",
            "revision": "Rev. 1",
            "issue_date": "2024-01-20",
            "description": "Recommended replacement of hydraulic pump seals to prevent leakage.",
            "applicability": {"aircraft_models": ["777-300ER"], "serial_numbers": []},
            "referred_ads": []
        },
        {
            "document_id": "SB-777-57-0125",
            "title": "Wing Skin Inspection",
            "issuing_authority": "Boeing",
            "revision": "Rev. 0",
            "issue_date": "2023-07-25",
            "description": "Details for wing skin inspection procedure.",
            "applicability": {"aircraft_models": ["777-300ER"], "serial_numbers": []},
            "referred_ads": ["AD-2025-06-02"]
        },
        {
            "document_id": "SB-A350-57-001",
            "title": "Fuselage Frame Repair",
            "issuing_authority": "Airbus",
            "revision": "Rev. 2",
            "issue_date": "2023-11-10",
            "description": "Details a repair procedure for a fuselage frame.",
            "applicability": {"aircraft_models": ["A350-900"], "serial_numbers": []},
            "referred_ads": []
        }
    ]

    # Technical Order data
    tos_data = [
        {
            "document_id": "TO-2023-A01",
            "title": "Cockpit Display Unit Update",
            "originator": "Thai Airways Engineering",
            "revision": "Ver. 1.0",
            "issue_date": "2023-08-01",
            "description": "Procedure for updating cockpit display unit software.",
            "applicability": {"aircraft_models": ["777-300ER"], "serial_numbers": []},
            "referred_ads": [],
            "referred_sbs": []
        },
        {
            "document_id": "TO-2023-A02",
            "title": "Cabin Lighting Modification",
            "originator": "Thai Airways Engineering",
            "revision": "Ver. 1.1",
            "issue_date": "2023-09-05",
            "description": "Instructions for installing new LED cabin lighting.",
            "applicability": {"aircraft_models": ["A350-900"], "serial_numbers": []},
            "referred_ads": [],
            "referred_sbs": []
        }
    ]

    # Engineering Directive data
    eds_data = [
        {
            "document_id": "ED-2024-01",
            "title": "Inspection of Landing Gear Latch",
            "description": "Mandatory inspection of the landing gear latch mechanism.",
            "applicability": {"aircraft_models": ["777-300ER", "787-8"], "serial_numbers": []},
            "issue_date": "2024-02-10"
        },
        {
            "document_id": "ED-2024-02",
            "title": "Fuel Tank Vent System Check",
            "description": "Check of the fuel tank vent system for blockages.",
            "applicability": {"aircraft_models": ["A350-900"], "serial_numbers": []},
            "issue_date": "2024-02-15"
        }
    ]

    return {
        "fleet_metadata": pd.DataFrame(fleet_data),
        "ads": pd.DataFrame(ads_data),
        "sbs": pd.DataFrame(sbs_data),
        "tos": pd.DataFrame(tos_data),
        "eds": pd.DataFrame(eds_data)
    }

# Load data
data = generate_synthetic_data()
fleet_df = data["fleet_metadata"]
ads_df = data["ads"]
sbs_df = data["sbs"]
tos_df = data["tos"]
eds_df = data["eds"]

# --- Streamlit UI ---

st.set_page_config(
    page_title="Aircraft Document Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Aircraft Document Tracker")
st.markdown("Track and manage all relevant documents for your aircraft fleet.")

# Sidebar for filters
st.sidebar.header("Filter by Aircraft")
selected_registration = st.sidebar.selectbox(
    "Select Aircraft Registration:",
    options=["All"] + fleet_df["registration"].tolist()
)

# Display data based on selection
if selected_registration == "All":
    st.header("Thai Airways Fleet Overview")
    st.dataframe(fleet_df, use_container_width=True)

    st.subheader("All Airworthiness Directives (ADs)")
    st.dataframe(ads_df, use_container_width=True)

    st.subheader("All Service Bulletins (SBs)")
    st.dataframe(sbs_df, use_container_width=True)

    st.subheader("All Technical Orders (TOs)")
    st.dataframe(tos_df, use_container_width=True)

    st.subheader("All Engineering Directives (EDs)")
    st.dataframe(eds_df, use_container_width=True)

else:
    st.header(f"Documents for Aircraft: {selected_registration}")
    
    # Get the selected aircraft's metadata
    selected_aircraft = fleet_df[fleet_df["registration"] == selected_registration].iloc[0]
    st.subheader("Aircraft Information")
    st.json(selected_aircraft.to_dict())

    # Filter and display documents based on the selected aircraft's applicable lists
    applicable_ads = ads_df[ads_df["document_id"].isin(selected_aircraft["applicable_ads"])]
    if not applicable_ads.empty:
        st.subheader("Applicable Airworthiness Directives (ADs)")
        st.dataframe(applicable_ads, use_container_width=True)
    
    applicable_sbs = sbs_df[sbs_df["document_id"].isin(selected_aircraft["applicable_sbs"])]
    if not applicable_sbs.empty:
        st.subheader("Applicable Service Bulletins (SBs)")
        st.dataframe(applicable_sbs, use_container_width=True)

    applicable_tos = tos_df[tos_df["document_id"].isin(selected_aircraft["applicable_tos"])]
    if not applicable_tos.empty:
        st.subheader("Applicable Technical Orders (TOs)")
        st.dataframe(applicable_tos, use_container_width=True)

    applicable_eds = eds_df[eds_df["document_id"].isin(selected_aircraft["applicable_eds"])]
    if not applicable_eds.empty:
        st.subheader("Applicable Engineering Directives (EDs)")
        st.dataframe(applicable_eds, use_container_width=True)
