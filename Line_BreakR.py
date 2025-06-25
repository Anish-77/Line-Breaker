# excel_cleaning_app.py
import streamlit as st
import pandas as pd
import numpy as np
import io

def clean_excel(file):
    df = pd.read_excel(file)

    # Strip column names
    df.columns = df.columns.str.strip()

    # Strip cell values & remove line breaks
    df = df.applymap(
        lambda x: str(x).replace("\n", " ").replace("\r", " ").strip() if pd.notnull(x) else x
    )

    # Detect line breaks (before removal)
    line_breaks_dict = {}
    for col in df.columns:
        rows_with_breaks = df[df[col].astype(str).str.contains(r'[\n\r]', regex=True, na=False)]
        if not rows_with_breaks.empty:
            line_breaks_dict[col] = rows_with_breaks

    return df, line_breaks_dict

def main():
    st.set_page_config(page_title="Excel Line Break Cleaner", layout="wide")
    st.title("📊 Surf Excel - Line Break Detection and Removal")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            df_cleaned, line_breaks_info = clean_excel(uploaded_file)

        st.success("File processed successfully!")

        st.subheader("Cleaned Data Preview")
        st.dataframe(df_cleaned.fillna("").head(50))  # Replace NaN with empty string for display

        st.subheader("Detected Line Breaks")
        if line_breaks_info:
            for col, rows in line_breaks_info.items():
                st.markdown(f"### Column: `{col}`")
                st.dataframe(rows)
        else:
            st.info("No line breaks detected in any column.")

        # Option to download cleaned file (with NaN replaced)
        towrite = io.BytesIO()
        df_cleaned.fillna("").to_excel(towrite, index=False, engine='openpyxl')  # Ensure empty cells are blank
        towrite.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel",
            data=towrite,
            file_name="cleaned_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
