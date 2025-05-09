import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.title("TB Test Expiry Checker")
    st.write("This application filters active employees with TB tests performed in 2022 and identifies those whose TB tests expire by 2025-06-30.")
    
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if not uploaded_file:
        st.warning("Please upload an Excel (.xlsx) file to proceed.")
        return
    
    try:
        df = pd.read_excel(uploaded_file)
    except Exception:
        st.error("Error reading the Excel file. Please ensure it's a valid .xlsx file.")
        return
    
    # Determine the employee name column
    if 'Legal Name' in df.columns:
        name_col = 'Legal Name'
    elif 'Employee Name' in df.columns:
        name_col = 'Employee Name'
    elif 'Name' in df.columns:
        name_col = 'Name'
    else:
        st.error("Employee name column not found. Expected 'Legal Name' or similar.")
        return
    
    # Check required columns
    if 'Position Status' not in df.columns:
        st.error("Missing required column: 'Position Status'.")
        return
    if 'Most Recent TB Test Date' not in df.columns:
        st.error("Missing required column: 'Most Recent TB Test Date'.")
        return
    
    # Convert TB Test Date to datetime, coerce errors
    try:
        df['Most Recent TB Test Date'] = pd.to_datetime(df['Most Recent TB Test Date'], errors='coerce')
    except Exception:
        st.error("Could not parse 'Most Recent TB Test Date' as dates.")
        return
    
    # Warn about invalid or missing dates
    invalid_dates = df['Most Recent TB Test Date'].isna().sum()
    if invalid_dates > 0:
        st.warning(f"{invalid_dates} rows have invalid or missing TB test dates and will be ignored.")
    
    # Filter for active employees
    df_active = df[df['Position Status'] == 'Active'].copy()
    if df_active.empty:
        st.info("No active employees found in the data.")
        return
    
    # Filter out rows without a valid TB test date
    df_active = df_active[df_active['Most Recent TB Test Date'].notna()]
    if df_active.empty:
        st.info("No active employees have a valid TB test date.")
        return
    
    # Filter TB test dates from year 2022
    df_2022 = df_active[df_active['Most Recent TB Test Date'].dt.year == 2022].copy()
    if df_2022.empty:
        st.info("No active employees have a TB test date in 2022.")
        return
    
    # Compute expiry date by adding 3 years to the test date
    df_2022['Expiry Date'] = df_2022['Most Recent TB Test Date'] + pd.DateOffset(years=3)
    
    # Identify employees whose TB test expires by 2025-06-30
    cutoff_date = datetime(2025, 6, 30)
    df_expire = df_2022[df_2022['Expiry Date'] <= cutoff_date].copy()
    
    # Display results
    if df_expire.empty:
        st.info("No active employees have TB tests expiring by 2025-06-30.")
    else:
        st.success(f"Found {len(df_expire)} active employees with TB tests expiring by 2025-06-30.")
        result_df = df_expire[[name_col, 'Most Recent TB Test Date', 'Expiry Date']].copy()
        result_df.rename(columns={name_col: 'Name', 'Most Recent TB Test Date': 'TB Test Date'}, inplace=True)
        # Format dates for display
        result_df['TB Test Date'] = result_df['TB Test Date'].dt.date
        result_df['Expiry Date'] = result_df['Expiry Date'].dt.date
        
        st.dataframe(result_df.reset_index(drop=True))

        # Display list of employee names with expiring TB tests
        expiring_names = result_df['Name'].tolist()
        st.write("Employees with expiring TB tests:")
        for name in expiring_names:
            st.write("- " + name)

if __name__ == "__main__":
    main()
