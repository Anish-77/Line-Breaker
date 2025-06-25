#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import io

def clean_excel(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()  # Trim column headers

    line_breaks_dict = {}

    for col in df.columns:
        # Detect line breaks before cleaning
        rows_with_breaks = df[df[col].astype(str).str.contains(r'[\n\r]', regex=True, na=False)]
        if not rows_with_breaks.empty:
            line_breaks_dict[col] = rows_with_breaks

        # Step 1: Convert all cells to string
        df[col] = df[col].astype(str)

        # Step 2: Remove line breaks
        df[col] = df[col].str.replace(r'[\n\r]+', ' ', regex=True)

        # Step 3: Trim leading/trailing whitespace
        df[col] = df[col].str.strip()

    return df, line_breaks_dict

def main():
    st.set_page_config(page_title="Excel Cleaner - Line Breaks & Trimming", layout="wide")
    st.title("📊 Excel Cleaner: Line Break Removal + Whitespace Trimming")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            df_cleaned, line_breaks_info = clean_excel(uploaded_file)

        st.success("File processed successfully!")

        st.subheader("🧹 Cleaned Data Preview")
        st.dataframe(df_cleaned.head(50))

        st.subheader("🔍 Detected Line Breaks (Before Cleaning)")
        if line_breaks_info:
            for col, rows in line_breaks_info.items():
                st.markdown(f"### Column: `{col}`")
                st.dataframe(rows)
        else:
            st.info("No line breaks detected in any column.")

        # Download cleaned file
        towrite = io.BytesIO()
        df_cleaned.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel",
            data=towrite,
            file_name="cleaned_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
