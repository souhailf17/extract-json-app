# extract_json.py
import streamlit as st
import json
import pandas as pd

st.title("JSON → Excel")

uploaded_files = st.file_uploader(
    "Uploader les fichiers JSON",
    type=["json"],
    accept_multiple_files=True
)

rows = []

if uploaded_files:
    for file in uploaded_files:
        data = json.load(file)

        if isinstance(data, dict) and "matching_procedure" in data:
            for item in data["matching_procedure"]:
                rows.append({
                    "matching_procedure_id": item.get("matching_procedure_id"),
                    "proc_title": item.get("proc_title")
                })

    df = pd.DataFrame(rows, columns=["matching_procedure_id", "proc_title"])
    st.dataframe(df)

    df.to_excel("extracted_data.xlsx", index=False)

    with open("extracted_data.xlsx", "rb") as f:
        st.download_button(
            label="Télécharger le fichier Excel",
            data=f,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
