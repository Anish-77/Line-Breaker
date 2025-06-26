#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import io

def clean_excel(file):
    df = pd.read_excel(file, dtype=str)  # Read all as strings to preserve blanks
    df.columns = df.columns.str.strip()

    line_breaks_dict = {}

    # Detect line breaks
    for col in df.columns:
        rows_with_breaks = df[df[col].astype(str).str.contains(r'[\n\r]', regex=True, na=False)]
        if not rows_with_breaks.empty:
            line_breaks_dict[col] = rows_with_breaks

    # Clean only columns with line breaks
    for col in line_breaks_dict.keys():
        df[col] = df[col].astype(str).str.replace(r'[\n\r]', ' ', regex=True)

    # Strip leading/trailing whitespace from all cells
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x).strip() if pd.notnull(x) else '')

    # Prepare cleaned rows preview (union of all rows with any breaks originally)
    cleaned_rows = pd.concat(line_breaks_dict.values()).drop_duplicates() if line_breaks_dict else pd.DataFrame()

    return df, cleaned_rows, line_breaks_dict

def main():
    st.set_page_config(page_title="Excel Cleaner - Line Break & Whitespace Cleaner", layout="wide")
    st.title("📊 Surf Excel – Remove Line Breaks & Trim Whitespaces")

    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

    if uploaded_file is not None:
        st.subheader("📄 Original File Preview")
        df_orig = pd.read_excel(uploaded_file, dtype=str)
        st.dataframe(df_orig.head(50))

        with st.spinner("🔄 Cleaning file..."):
            cleaned_df, cleaned_rows, breaks_dict = clean_excel(uploaded_file)

        st.success("✅ File cleaned successfully!")

        st.subheader("🔍 Cleaned Data Preview")
        st.dataframe(cleaned_df.head(50))

        if not cleaned_rows.empty:
            st.subheader("🧹 Cleaned Rows (Had Line Breaks Previously)")
            st.dataframe(cleaned_rows)
        else:
            st.info("No line breaks were found in any column.")

        # Download cleaned file
        towrite = io.BytesIO()
        cleaned_df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=towrite,
            file_name="cleaned_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
