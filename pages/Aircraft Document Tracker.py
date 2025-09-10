import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta
import io

# Sample data for aircraft. This would typically come from a database.
aircraft_data = {
    'All': {'model': 'N/A', 'airworthiness_certificate_date': 'N/A'},
    'HS-TWA': {
        'model': 'Airbus A320',
        'airworthiness_certificate_date': date(2015, 3, 10),
        'flight_hours': 12500,
        'flight_cycles': 8900
    },
    'HS-TWB': {
        'model': 'Boeing 737',
        'airworthiness_certificate_date': date(2018, 7, 25),
        'flight_hours': 8700,
        'flight_cycles': 6300
    },
    'HS-TWC': {
        'model': 'Cessna 172',
        'airworthiness_certificate_date': date(2005, 1, 15),
        'flight_hours': 2500,
        'flight_cycles': 20000
    }
}

# Generate more realistic-looking sample data for documents with a hierarchical structure
def generate_documents_with_relations(ad_count, sb_count, to_count, ed_count):
    # Create ADs first, as they are the top level
    ads = [{
        'document_id': f'AD-{random.randint(100, 999)}-{random.randint(10, 99)}',
        'title': f'Airworthiness Directive for Component {i+1}',
        'status': random.choice(['Compliant', 'Not Compliant', 'N/A', 'Pending Review']),
        'date_due': date.today() + timedelta(days=random.randint(10, 365)),
        'last_completed': date.today() - timedelta(days=random.randint(10, 365))
    } for i in range(ad_count)]

    sbs = []
    tos = []
    eds = []

    for ad in ads:
        # Each AD can have 1-2 related SBs
        num_sbs = random.randint(1, 2)
        for i in range(num_sbs):
            sb_id = f'SB-{random.randint(1000, 9999)}'
            sbs.append({
                'document_id': sb_id,
                'title': f'Service Bulletin related to {ad["document_id"]}',
                'status': random.choice(['Compliant', 'Not Compliant', 'N/A', 'Pending Review']),
                'related_document_id': ad['document_id']
            })

            # Guarantee at least one TO and one ED for each SB
            tos.append({
                'document_id': f'TO-{random.randint(1000, 9999)}',
                'title': f'Technical Order for {sb_id}',
                'status': random.choice(['Compliant', 'Not Compliant']),
                'related_document_id': sb_id
            })
            
            eds.append({
                'document_id': f'ED-{random.randint(1000, 9999)}',
                'title': f'Engineering Document for {sb_id}',
                'status': random.choice(['Compliant', 'Not Compliant']),
                'related_document_id': sb_id
            })

    return ads, sbs, tos, eds

# Generate the data for all aircrafts.
aircraft_documents = {}
for ac_id in aircraft_data.keys():
    if ac_id != 'All':
        ads, sbs, tos, eds = generate_documents_with_relations(ad_count=5, sb_count=7, to_count=4, ed_count=6)
        aircraft_documents[ac_id] = {
            'ADs': ads,
            'SBs': sbs,
            'TOs': tos,
            'EDs': eds
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
    pending_ads = sum(1 for doc in ac_docs.get('ADs', []) if doc['status'] != 'Compliant')
    pending_sbs = sum(1 for doc in ac_docs.get('SBs', []) if doc['status'] != 'Compliant')
    pending_tos = sum(1 for doc in ac_docs.get('TOs', []) if doc['status'] != 'Compliant')
    pending_eds = sum(1 for doc in ac_docs.get('EDs', []) if doc['status'] != 'Compliant')

    # Metadata display using columns
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
| **Airworthiness Directives (ADs)** | `{num_ads}` | `{pending_ads}` |
| **Service Bulletins (SBs)** | `{num_sbs}` | `{pending_sbs}` |
| **Technical Orders (TOs)** | `{num_tos}` | `{pending_tos}` |
| **Engineering Documents (EDs)** | `{num_eds}` | `{pending_eds}` |
""")

    st.divider()

    # Function to create a downloadable DataFrame
    def create_download_df(docs):
        flat_list = []
        for ad in docs.get('ADs', []):
            flat_list.append({
                'Document_Type': 'AD',
                'Document_ID': ad['document_id'],
                'Title': ad['title'],
                'Status': ad['status'],
                'Date_Due': ad.get('date_due', 'N/A'),
                'Last_Completed': ad.get('last_completed', 'N/A'),
                'Related_To': 'N/A'
            })
            # Find related SBs, TOs, and EDs
            related_sbs = [sb for sb in docs['SBs'] if sb['related_document_id'] == ad['document_id']]
            related_tos = [to for to in docs['TOs'] if to['related_document_id'] == ad['document_id']]
            related_eds = [ed for ed in docs['EDs'] if ed['related_document_id'] == ad['document_id']]
            
            for sb in related_sbs:
                flat_list.append({
                    'Document_Type': 'SB',
                    'Document_ID': sb['document_id'],
                    'Title': sb['title'],
                    'Status': sb['status'],
                    'Date_Due': 'N/A',
                    'Last_Completed': 'N/A',
                    'Related_To': ad['document_id']
                })
            for to in related_tos:
                flat_list.append({
                    'Document_Type': 'TO',
                    'Document_ID': to['document_id'],
                    'Title': to['title'],
                    'Status': to['status'],
                    'Date_Due': 'N/A',
                    'Last_Completed': 'N/A',
                    'Related_To': ad['document_id']
                })
            for ed in related_eds:
                flat_list.append({
                    'Document_Type': 'ED',
                    'Document_ID': ed['document_id'],
                    'Title': ed['title'],
                    'Status': ed['status'],
                    'Date_Due': 'N/A',
                    'Last_Completed': 'N/A',
                    'Related_To': ad['document_id']
                })
        return pd.DataFrame(flat_list)



    # New section for a table overview
    st.subheader("All Airworthiness Directives")
    df_ads = pd.DataFrame(ac_docs['ADs'])
    st.dataframe(df_ads[['document_id', 'title', 'status', 'date_due', 'last_completed']], use_container_width=True, hide_index=True)

    # Allow users to select an AD to view related docs
    st.subheader("Related Documents for Selected AD")
    
    ad_options = [ad['document_id'] for ad in ac_docs['ADs']]
    if ad_options:
        selected_ad_id = st.selectbox(
            "Select an AD to view related documents:",
            ad_options
        )

        # Display related SBs, TOs, and EDs
        related_sbs = [sb for sb in ac_docs['SBs'] if sb['related_document_id'] == selected_ad_id]
        related_tos = [to for to in ac_docs['TOs'] if to['related_document_id'] == selected_ad_id]
        related_eds = [ed for ed in ac_docs['EDs'] if ed['related_document_id'] == selected_ad_id]
        
        col_sb, col_to, col_ed = st.columns(3)

        with col_sb:
            st.markdown("##### Service Bulletins (SBs)")
            if related_sbs:
                st.dataframe(pd.DataFrame(related_sbs)[['document_id', 'title', 'status']], use_container_width=True, hide_index=True)
            else:
                st.info("No SBs found for this AD.")

        with col_to:
            st.markdown("##### Technical Orders (TOs)")
            if related_tos:
                st.dataframe(pd.DataFrame(related_tos)[['document_id', 'title', 'status']], use_container_width=True, hide_index=True)
            else:
                st.info("No TOs found for this AD.")
        
        with col_ed:
            st.markdown("##### Engineering Documents (EDs)")
            if related_eds:
                st.dataframe(pd.DataFrame(related_eds)[['document_id', 'title', 'status']], use_container_width=True, hide_index=True)
            else:
                st.info("No EDs found for this AD.")
    else:
        st.info("No ADs found for this aircraft.")
    
    # Add the download button
    df_download = create_download_df(ac_docs)
    csv_string = df_download.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All Documents List as CSV",
        data=csv_string,
        file_name=f"{aircraft_id}_documents_list.csv",
        mime='text/csv'
    )