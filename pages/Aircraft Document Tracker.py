import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

# Sample data for aircraft and documents. This would typically come from a database.
aircraft_data = {
    'All': {'model': 'N/A', 'airworthiness_certificate_date': 'N/A'},
    'HS-TXC': {
        'model': 'Airbus A320',
        'airworthiness_certificate_date': date(2015, 3, 10),
        'flight_hours': 12500,
        'flight_cycles': 8900
    },
    'HS-TQB': {
        'model': 'Boeing 787',
        'airworthiness_certificate_date': date(2018, 7, 25),
        'flight_hours': 8700,
        'flight_cycles': 6300
    },
    'HS-TWB': {
        'model': 'Cessna 172',
        'airworthiness_certificate_date': date(2005, 1, 15),
        'flight_hours': 2500,
        'flight_cycles': 20000
    }
}

# Generate more realistic-looking sample data for documents
def generate_documents(prefix, count):
    docs = []
    for i in range(count):
        doc = {
            'document_id': f'{prefix}-{random.randint(100, 999)}-{random.randint(10, 99)}',
            'title': f'Inspection of {prefix} component {i+1}',
            'status': random.choice(['Compliant', 'Not Compliant', 'N/A', 'Pending Review']),
            'date_due': date.today() + timedelta(days=random.randint(10, 365)),
            'last_completed': date.today() - timedelta(days=random.randint(10, 365))
        }
        docs.append(doc)
    return docs

ads = generate_documents('AD', 45)
sbs = generate_documents('SB', 65)
tos = generate_documents('TO', 65)
eds = generate_documents('ED', 39)

aircraft_documents = {
    'HS-TXC': {
        'ADs': [d for d in ads if d['status'] != 'Not Applicable'],
        'SBs': [d for d in sbs if d['status'] != 'Not Applicable'],
        'TOs': [d for d in tos if d['status'] != 'Not Applicable'],
        'EDs': [d for d in eds if d['status'] != 'Not Applicable'],
    },
    'HS-TQB': {
        'ADs': [d for d in ads if d['status'] != 'Not Applicable'],
        'SBs': [d for d in sbs if d['status'] != 'Not Applicable'],
        'TOs': [d for d in tos if d['status'] != 'Not Applicable'],
        'EDs': [d for d in eds if d['status'] != 'Not Applicable'],
    },
    'HS-TWB': {
        'ADs': [d for d in ads if d['status'] != 'Not Applicable'],
        'SBs': [d for d in sbs if d['status'] != 'Not Applicable'],
        'TOs': [d for d in tos if d['status'] != 'Not Applicable'],
        'EDs': [d for d in eds if d['status'] != 'Not Applicable'],
    }
}

st.set_page_config(layout="wide")
st.title("Aircraft Maintenance & Compliance Dashboard")

# 1. Toggle on the page, not the side bar
aircraft_id = st.selectbox(
    "Select Aircraft",
    list(aircraft_data.keys())
)

st.divider()

if aircraft_id == 'All':
    st.info("Please select an aircraft from the dropdown above to view its specific details.")
else:
    # Get the data for the selected aircraft
    ac_info = aircraft_data[aircraft_id]
    ac_docs = aircraft_documents[aircraft_id]

    # Calculate metrics
    num_ads = len(ac_docs.get('ADs', []))
    num_sbs = len(ac_docs.get('SBs', []))
    num_tos = len(ac_docs.get('TOs', []))
    num_eds = len(ac_docs.get('EDs', []))

    # Example of how to count "pending" tasks
    pending_tasks = sum(1 for doc in ac_docs.get('ADs', []) if doc['status'] != 'Compliant')

    # New metadata display using columns and metrics
    st.subheader(f"Metadata for {aircraft_id}")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"**Aircraft Model:** `{ac_info['model']}`")
    with col2:
        st.markdown(f"**Date into Service:** `{ac_info['airworthiness_certificate_date'].strftime('%B %d, %Y')}`")
    with col3:
        st.markdown(f"**Flight Hours:** `{ac_info['flight_hours']:,}`")
    with col4:
        st.markdown(f"**Flight Cycles:** `{ac_info['flight_cycles']:,}`")
    
    st.markdown("---")
    
    st.subheader("Task Summary")
    st.markdown(f"""
| Document Type | Applicable | Pending Tasks |
| :--- | :---: | :---: |
| **Airworthiness Directives (ADs)** | `{num_ads}` | `{pending_tasks}` |
| **Service Bulletins (SBs)** | `{num_sbs}` | `{sum(1 for doc in ac_docs.get('SBs', []) if doc['status'] != 'Compliant')}` |
| **Technical Orders (TOs)** | `{num_tos}` | `{sum(1 for doc in ac_docs.get('TOs', []) if doc['status'] != 'Compliant')}` |
| **Engineering Documents (EDs)** | `{num_eds}` | `{sum(1 for doc in ac_docs.get('EDs', []) if doc['status'] != 'Compliant')}` |
""")

    st.divider()
    
    # Tables beside each other (horizontally), with expanders removed
    st.subheader("Document Details")
    
    col_ad, col_sb, col_to, col_ed = st.columns(4)

    with col_ad:
        st.write("#### Airworthiness Directives")
        df_ads = pd.DataFrame(ac_docs['ADs'])
        st.dataframe(df_ads, use_container_width=True, hide_index=True)
            
    with col_sb:
        st.write("#### Service Bulletins")
        df_sbs = pd.DataFrame(ac_docs['SBs'])
        st.dataframe(df_sbs, use_container_width=True, hide_index=True)

    with col_to:
        st.write("#### Technical Orders")
        df_tos = pd.DataFrame(ac_docs['TOs'])
        st.dataframe(df_tos, use_container_width=True, hide_index=True)
            
    with col_ed:
        st.write("#### Engineering Documents")
        df_eds = pd.DataFrame(ac_docs['EDs'])
        st.dataframe(df_eds, use_container_width=True, hide_index=True)

