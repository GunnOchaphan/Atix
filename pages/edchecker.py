import streamlit as st
import pandas as pd
import io

# Data setup
# Note: The 'export.xlsx' file is assumed to exist in the same directory.
# If not, you'll need to create a dummy file for the code to run.
# For demonstration purposes, we'll create a dummy DataFrame to mimic the excel file.
try:
    file_path = '../export.xlsx'
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.warning("`export.xlsx` not found. Using dummy data for demonstration.")
    data = {
        'Document': [f'ED-{i}' for i in range(1, 101)],
        'Document version': [f'Rev {i}' for i in range(1, 101)],
        'Description': [
            'Inspection of A350 engines', 'Boeing 777 landing gear check', 'A320 wing flap inspection',
            'Engine wash for A350 fleet', 'B777 cabin lights upgrade', 'A330 fuselage repair',
            'A350 cabin oxygen system', 'B787 nav system check', 'A320 cargo hold fix',
            'B777 emergency slide test', 'Boeing 787 wing anti-ice', 'Airbus A330-300 emergency systems',
            'A350-900 pilot communication', 'B777-300ER seating modification', 'B787-8 Dreamliner electrical system',
            'A320 P320 ITO update', 'HS-THY landing gear', 'A330 HS tail number'
        ] * 5 + ['Description 1', 'Description 2', 'Description 3', 'Description 4', 'Description 5'],
        'From date': pd.to_datetime([
            '2024-01-15', '2006-12-01', '2023-01-20', '2023-03-22', '2012-05-18', '2009-02-14',
            '2016-07-28', '2014-03-10', '2023-04-05', '2007-01-30', '2014-06-01', '2009-03-01',
            '2016-08-01', '2012-08-01', '2014-07-01', '2023-01-01', '2024-02-15', '2024-10-10'
        ] * 5 + ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'])
    }
    df = pd.DataFrame(data)

# Keep only relevant columns and deduplicate
df = df[['Document', 'Document version', 'Description', 'From date']]
df = df.drop_duplicates(subset=['Document'], keep='last')
df['From date'] = pd.to_datetime(df['From date'], errors='coerce')

# Filter main ED dataframe by aircraft type
df_a350 = df[df['Description'].str.contains('A350|350', case=False, na=False) & ~df['Description'].str.contains('HS', case=False, na=False)]
df_a330 = df[df['Description'].str.contains('A330|330', case=False, na=False) & ~df['Description'].str.contains('HS', case=False, na=False)]
df_a320 = df[df['Description'].str.contains('A320|320', case=False, na=False) & ~df['Description'].str.contains('HS|ITO|P320 ', case=False, na=False)]
df_b777 = df[df['Description'].str.contains('B777|777', case=False, na=False) & ~df['Description'].str.contains('HS', case=False, na=False)]
df_b787 = df[df['Description'].str.contains('B787|787', case=False, na=False) & ~df['Description'].str.contains('HS', case=False, na=False)]

# Fleet data and dataframe creation
fleet_data = [
    ("HS-THY", "Airbus A350-900", "Mar 2024"), ("HS-THZ", "Airbus A350-900", "May 2024"),
    ("HS-TJR", "Boeing 777-200", "Nov 2006"), ("HS-TJV", "Boeing 777-200", "Sep 2007"),
    ("HS-TJW", "Boeing 777-200", "Oct 2007"), ("HS-TKK", "Boeing 777-300ER", "Aug 2012"),
    ("HS-TKL", "Boeing 777-300ER", "Oct 2012"), ("HS-TKM", "Boeing 777-300ER", "Mar 2013"),
    ("HS-TKN", "Boeing 777-300ER", "Apr 2013"), ("HS-TKO", "Boeing 777-300ER", "Jun 2013"),
    ("HS-TKP", "Boeing 777-300ER", "Jul 2013"), ("HS-TKQ", "Boeing 777-300ER", "Aug 2013"),
    ("HS-TKR", "Boeing 777-300ER", "Oct 2013"), ("HS-TKU", "Boeing 777-300ER", "Jan 2014"),
    ("HS-TKV", "Boeing 777-300ER", "Jul 2014"), ("HS-TKW", "Boeing 777-300ER", "Aug 2014"),
    ("HS-TKX", "Boeing 777-300ER", "Jan 2015"), ("HS-TKY", "Boeing 777-300ER", "Jun 2015"),
    ("HS-TKZ", "Boeing 777-300ER", "Sep 2015"), ("HS-TTA", "Boeing 777-300ER", "Apr 2022"),
    ("HS-TTB", "Boeing 777-300ER", "Apr 2022"), ("HS-TTC", "Boeing 777-300ER", "Apr 2022"),
    ("HS-TQA", "Boeing 787-8 Dreamliner", "Jul 2014"), ("HS-TQB", "Boeing 787-8 Dreamliner", "Sep 2014"),
    ("HS-TQC", "Boeing 787-8 Dreamliner", "Oct 2014"), ("HS-TQD", "Boeing 787-8 Dreamliner", "Dec 2014"),
    ("HS-TQE", "Boeing 787-8 Dreamliner", "Apr 2015"), ("HS-TQF", "Boeing 787-8 Dreamliner", "Aug 2015"),
    ("HS-TWA", "Boeing 787-9 Dreamliner", "Sep 2017"), ("HS-TWB", "Boeing 787-9 Dreamliner", "Oct 2017"),
    ("HS-TWC", "Boeing 787-9 Dreamliner", "May 2024"),
    ("HS-TXA", "Airbus A320-200", "Oct 2023"), ("HS-TXB", "Airbus A320-200", "Dec 2023"),
    ("HS-TXC", "Airbus A320-200", "Nov 2023"), ("HS-TXD", "Airbus A320-200", "Dec 2023"),
    ("HS-TXE", "Airbus A320-200", "Jul 2023"), ("HS-TXF", "Airbus A320-200", "Sep 2023"),
    ("HS-TXG", "Airbus A320-200", "Oct 2023"), ("HS-TXH", "Airbus A320-200", "Dec 2023"),
    ("HS-TXJ", "Airbus A320-200", "Jan 2024"), ("HS-TXK", "Airbus A320-200", "Sep 2023"),
    ("HS-TXL", "Airbus A320-200", "Nov 2023"), ("HS-TXM", "Airbus A320-200", "Jan 2024"),
    ("HS-TXN", "Airbus A320-200", "Dec 2023"), ("HS-TXO", "Airbus A320-200", "Jan 2024"),
    ("HS-TXP", "Airbus A320-200", "Jan 2024"), ("HS-TXQ", "Airbus A320-200", "May 2023"),
    ("HS-TXR", "Airbus A320-200", "May 2023"), ("HS-TXS", "Airbus A320-200", "Jul 2023"),
    ("HS-TXT", "Airbus A320-200", "Nov 2023"), ("HS-TXU", "Airbus A320-200", "Dec 2023"),
    ("HS-TEN", "Airbus A330-300", "Apr 2009"), ("HS-TEO", "Airbus A330-300", "May 2009"),
    ("HS-TEP", "Airbus A330-300", "Jul 2009"), ("HS-TEV", "Airbus A330-300", "Oct 2024"),
    ("HS-TEW", "Airbus A330-300", "Oct 2024"), ("HS-TEX", "Airbus A330-300", "Aug 2025"),
    ("HS-THB", "Airbus A350-900", "Aug 2016"), ("HS-THC", "Airbus A350-900", "Oct 2016"),
    ("HS-THD", "Airbus A350-900", "Apr 2017"), ("HS-THE", "Airbus A350-900", "Jun 2017"),
    ("HS-THF", "Airbus A350-900", "Jul 2017"), ("HS-THG", "Airbus A350-900", "Aug 2017"),
    ("HS-THH", "Airbus A350-900", "Sep 2017"), ("HS-THJ", "Airbus A350-900", "Jan 2018"),
    ("HS-THK", "Airbus A350-900", "Jan 2018"), ("HS-THL", "Airbus A350-900", "Feb 2018"),
    ("HS-THM", "Airbus A350-900", "Mar 2018"), ("HS-THN", "Airbus A350-900", "May 2018"),
    ("HS-THO", "Airbus A350-900", "May 2023"), ("HS-THP", "Airbus A350-900", "Jun 2023"),
    ("HS-THQ", "Airbus A350-900", "Sep 2023"), ("HS-THR", "Airbus A350-900", "Oct 2023"),
    ("HS-THS", "Airbus A350-900", "Feb 2024"), ("HS-THT", "Airbus A350-900", "Apr 2024"),
    ("HS-THU", "Airbus A350-900", "Apr 2024"), ("HS-THV", "Airbus A350-900", "Nov 2023"),
    ("HS-THX", "Airbus A350-900", "Mar 2024"),
]

df_fleet_a350 = pd.DataFrame([f for f in fleet_data if 'A350' in f[1]], columns=['Registration', 'Aircraft Type', 'In Service Date'])
df_fleet_a330 = pd.DataFrame([f for f in fleet_data if 'A330' in f[1]], columns=['Registration', 'Aircraft Type', 'In Service Date'])
df_fleet_a320 = pd.DataFrame([f for f in fleet_data if 'A320' in f[1]], columns=['Registration', 'Aircraft Type', 'In Service Date'])
df_fleet_b777 = pd.DataFrame([f for f in fleet_data if '777' in f[1]], columns=['Registration', 'Aircraft Type', 'In Service Date'])
df_fleet_b787 = pd.DataFrame([f for f in fleet_data if '787' in f[1]], columns=['Registration', 'Aircraft Type', 'In Service Date'])

# Convert 'In Service Date' to datetime
df_fleet_a350['In Service Date'] = pd.to_datetime(df_fleet_a350['In Service Date'], errors='coerce')
df_fleet_a330['In Service Date'] = pd.to_datetime(df_fleet_a330['In Service Date'], errors='coerce')
df_fleet_a320['In Service Date'] = pd.to_datetime(df_fleet_a320['In Service Date'], errors='coerce')
df_fleet_b777['In Service Date'] = pd.to_datetime(df_fleet_b777['In Service Date'], errors='coerce')
df_fleet_b787['In Service Date'] = pd.to_datetime(df_fleet_b787['In Service Date'], errors='coerce')

# Filter EDs based on in-service date for each aircraft
results_a350 = {row['Registration']: df_a350[df_a350['From date'] < row['In Service Date']] for _, row in df_fleet_a350.iterrows()}
results_a330 = {row['Registration']: df_a330[df_a330['From date'] < row['In Service Date']] for _, row in df_fleet_a330.iterrows()}
results_a320 = {row['Registration']: df_a320[df_a320['From date'] < row['In Service Date']] for _, row in df_fleet_a320.iterrows()}
results_b777 = {row['Registration']: df_b777[df_b777['From date'] < row['In Service Date']] for _, row in df_fleet_b777.iterrows()}
results_b787 = {row['Registration']: df_b787[df_b787['From date'] < row['In Service Date']] for _, row in df_fleet_b787.iterrows()}

# Combine all results and fleet data for easy lookup
all_results = {
    'A350': {'results': results_a350, 'fleet_df': df_fleet_a350},
    'A330': {'results': results_a330, 'fleet_df': df_fleet_a330},
    'A320': {'results': results_a320, 'fleet_df': df_fleet_a320},
    'B777': {'results': results_b777, 'fleet_df': df_fleet_b777},
    'B787': {'results': results_b787, 'fleet_df': df_fleet_b787},
}

# --- Streamlit App ---
st.set_page_config(
    page_title="ED Checker",
    layout="wide",
)

st.sidebar.markdown("# Pending EDs")

st.title("Aircraft Engineering Directives Checker")
st.write("Simple data manipulation can reduce working hours by half. By using this tool, you can quickly identify relevant Engineering Documents (EDs) for your aircraft fleet based on their in-service dates.")
st.write("Making sure your aircraft are compliant with the latest EDs for safety and regulatory adherence.")

# Use a radio button to switch between modes
mode = st.radio(
    "Choose Mode",
    ("Check Existing Aircraft", "Check for a New Aircraft")
)

# ----------------- Mode 1: Existing Aircraft -----------------
if mode == "Check Existing Aircraft":
    st.write("Select an aircraft type and registration from the fleet to see all Engineering Directives (EDs) issued before its in-service date.")

    # Create dropdown for aircraft type
    aircraft_types = list(all_results.keys())
    selected_ac_type = st.selectbox(
        "Select Aircraft Type",
        aircraft_types
    )

    if selected_ac_type:
        # Get the dictionary for the selected type
        current_data = all_results[selected_ac_type]
        current_results = current_data['results']
        current_fleet_df = current_data['fleet_df']

        # Get the list of registrations for the selected type
        registrations = list(current_results.keys())
        
        # Create dropdown for aircraft registration
        selected_ac_reg = st.selectbox(
            "Select Aircraft Registration",
            registrations
        )

        if selected_ac_reg:
            # Get the DataFrame for the selected registration
            filtered_eds_df = current_results[selected_ac_reg]

            # Get the in-service date for the selected aircraft
            in_service_date = current_fleet_df[current_fleet_df['Registration'] == selected_ac_reg]['In Service Date'].iloc[0]

            st.subheader(f"Engineering Directives for {selected_ac_reg}")
            st.info(f"Showing EDs issued **before** the in-service date of **{in_service_date.strftime('%Y-%m-%d')}**.")

            if not filtered_eds_df.empty:
                st.dataframe(filtered_eds_df.reset_index(drop=True), hide_index=True)
            else:
                st.success(f"No Engineering Documents found for {selected_ac_reg} that were issued before its in-service date.")

# ----------------- Mode 2: New Aircraft -----------------
else: # mode == "Check for a New Aircraft"
    st.write("Select an aircraft type and specify its in-service date to find relevant EDs.")
    
    # Select aircraft type
    aircraft_types = list(all_results.keys())
    selected_ac_type_new = st.selectbox(
        "Select Aircraft Type",
        aircraft_types,
        key="new_aircraft_type" # Use a unique key to prevent conflicts
    )
    
    # Get the correct DataFrame for the selected type
    if selected_ac_type_new == 'A350':
        df_to_filter = df_a350
    elif selected_ac_type_new == 'A330':
        df_to_filter = df_a330
    elif selected_ac_type_new == 'A320':
        df_to_filter = df_a320
    elif selected_ac_type_new == 'B777':
        df_to_filter = df_b777
    elif selected_ac_type_new == 'B787':
        df_to_filter = df_b787
    
    # Select in-service date
    in_service_date_new = st.date_input(
        "Select In-Service Date",
        pd.to_datetime('today'),
    )
    
    # Convert the date_input to a datetime object for comparison
    in_service_date_new = pd.to_datetime(in_service_date_new)
    
    # Filter the DataFrame based on the selected date
    filtered_eds_new_df = df_to_filter[df_to_filter['From date'] < in_service_date_new]
    
    st.subheader(f"Engineering Directives for a New {selected_ac_type_new} Aircraft")
    st.info(f"Showing EDs issued **before** the in-service date of **{in_service_date_new.strftime('%Y-%m-%d')}**.")

    if not filtered_eds_new_df.empty:
        st.dataframe(filtered_eds_new_df.reset_index(drop=True), hide_index=True)
    else:
        st.success(f"No Engineering Derivatives found that were issued before the selected in-service date.")


st.write("It is recommended to cross-check the results with the official document management system to ensure completeness and accuracy.")
