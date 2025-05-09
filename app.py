
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("TB Test Expiry Checker")

uploaded_file = st.file_uploader("Upload 'renewables' spreadsheet (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    try:
        # Step 2: Filter active employees
        df_active = df[df['Position Status'] == 'Active']
        
        # Step 3: Convert and filter test dates from 2022
        df_active['Most Recent TB Test Date'] = pd.to_datetime(df_active['Most Recent TB Test Date'], errors='coerce')
        df_2022 = df_active[df_active['Most Recent TB Test Date'].dt.year == 2022]
        
        # Step 4: Calculate expiration
        df_2022['TB Test Expiry Date'] = df_2022['Most Recent TB Test Date'] + pd.DateOffset(years=3)
        
        # Step 5: Filter for expirations on or before 2025-06-30
        cutoff = pd.to_datetime("2025-06-30")
        df_expiring = df_2022[df_2022['TB Test Expiry Date'] <= cutoff]
        
        st.success(f"Found {len(df_expiring)} employees with TB tests expiring by 2025-06-30.")
        st.dataframe(df_expiring[['Employee Name', 'Most Recent TB Test Date', 'TB Test Expiry Date']])
        
        # Optional: Download
        csv = df_expiring.to_csv(index=False)
        st.download_button("Download CSV", csv, "tb_expiring_employees.csv", "text/csv")
    
    except KeyError as e:
        st.error(f"Missing expected column: {e}")
