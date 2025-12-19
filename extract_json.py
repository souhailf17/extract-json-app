# app.py
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

        if isinstance(data, list):
            for item in data:
                rows.append({
                    "proc_title": item.get("proc_title"),
                    "proc_id": item.get("proc_id")
                })
        elif isinstance(data, dict):
            rows.append({
                "proc_title": data.get("proc_title"),
                "proc_id": data.get("proc_id")
            })

    df = pd.DataFrame(rows)
    st.dataframe(df)

    with open("extracted_data.xlsx", "wb") as f:
        df.to_excel(f, index=False)

    with open("extracted_data.xlsx", "rb") as f:
        st.download_button(
            label="Télécharger le fichier Excel",
            data=f,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
