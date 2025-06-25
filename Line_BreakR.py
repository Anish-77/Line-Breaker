#!/usr/bin/env python
# coding: utf-8

  

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
