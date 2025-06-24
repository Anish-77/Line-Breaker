{
 "cells": [
  {
   "cell_type": "code",
   "id": "a009dd8b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Line_Breaker.py\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import io\n",
    "\n",
    "def clean_excel(file):\n",
    "    df = pd.read_excel(file)\n",
    "    df.columns = df.columns.str.strip()\n",
    "\n",
    "    line_breaks_dict = {}\n",
    "    for col in df.columns:\n",
    "        rows_with_breaks = df[df[col].astype(str).str.contains(r'[\\n\\r]', regex=True, na=False)]\n",
    "        if not rows_with_breaks.empty:\n",
    "            line_breaks_dict[col] = rows_with_breaks\n",
    "\n",
    "    return df, line_breaks_dict\n",
    "\n",
    "def main():\n",
    "    st.set_page_config(page_title=\"Excel Line Break Cleaner\", layout=\"wide\")\n",
    "    st.title(\"📊 Excel Cleaner - Line Break Detection\")\n",
    "\n",
    "    uploaded_file = st.file_uploader(\"Upload an Excel file\", type=[\"xlsx\"])\n",
    "\n",
    "    if uploaded_file is not None:\n",
    "        with st.spinner(\"Processing file...\"):\n",
    "            df_cleaned, line_breaks_info = clean_excel(uploaded_file)\n",
    "\n",
    "        st.success(\"File processed successfully!\")\n",
    "\n",
    "        st.subheader(\"Cleaned Data Preview\")\n",
    "        st.dataframe(df_cleaned.head(50))\n",
    "\n",
    "        st.subheader(\"Detected Line Breaks\")\n",
    "        if line_breaks_info:\n",
    "            for col, rows in line_breaks_info.items():\n",
    "                st.markdown(f\"### Column: `{col}`\")\n",
    "                st.dataframe(rows)\n",
    "        else:\n",
    "            st.info(\"No line breaks detected in any column.\")\n",
    "\n",
    "        # Option to download cleaned file\n",
    "        towrite = io.BytesIO()\n",
    "        df_cleaned.to_excel(towrite, index=False, engine='openpyxl')\n",
    "        towrite.seek(0)\n",
    "\n",
    "        st.download_button(\n",
    "            label=\"📥 Download Cleaned Excel\",\n",
    "            data=towrite,\n",
    "            file_name=\"cleaned_file.xlsx\",\n",
    "            mime=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\"\n",
    "        )\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "2ffc33f6",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
