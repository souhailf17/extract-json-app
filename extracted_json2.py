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

def find_matching_procedures(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "matching_procedure" and isinstance(value, list):
                for item in value:
                    rows.append({
                        "matching_procedure_id": item.get("matching_procedure_id"),
                        "proc_title": item.get("proc_title")
                    })
            else:
                find_matching_procedures(value)
    elif isinstance(obj, list):
        for item in obj:
            find_matching_procedures(item)

if uploaded_files:
    for file in uploaded_files:
        data = json.load(file)
        find_matching_procedures(data)

    df = pd.DataFrame(rows, columns=["matching_procedure_id", "proc_title"])
    st.dataframe(df)

    df.to_excel("extracted_data.xlsx", index=False)

    with open("extracted_data.xlsx", "rb") as f:
        st.download_button(
            "Télécharger le fichier Excel",
            f,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
