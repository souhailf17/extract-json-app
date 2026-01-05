import streamlit as st
import pandas as pd
import json
import re
from io import BytesIO

st.set_page_config(page_title="Extraction JSON → Excel", layout="wide")

st.title("📄 Extraction des données JSON vers Excel")

# =========================
# Fonctions utilitaires
# =========================

def extract_number_from_filename(filename):
    """Extrait le numéro entouré par _ ex: _72_"""
    match = re.search(r"_([0-9]+)_", filename)
    return match.group(1) if match else None

def extract_date_from_filename(filename):
    """Extrait une date au format YYYY-MM-DD"""
    match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
    return match.group(0) if match else None

# =========================
# Upload des fichiers
# =========================

uploaded_files = st.file_uploader(
    "📤 Uploader les fichiers JSON",
    type=["json"],
    accept_multiple_files=True
)

if uploaded_files:
    results = []

    for file in uploaded_files:
        filename = file.name

        # Extraction depuis le nom du fichier
        extracted_number = extract_number_from_filename(filename)
        extracted_date = extract_date_from_filename(filename)

        try:
            data = json.load(file)

            proc_title = data.get("proc_title")
            proc_id = data.get("proc_id")

            results.append({
                "nom_fichier": filename,
                "numero_extrait": extracted_number,
                "date_extraite": extracted_date,
                "proc_title": proc_title,
                "proc_id": proc_id
            })

        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier {filename}: {e}")

    # =========================
    # DataFrame
    # =========================
    df = pd.DataFrame(results)

    st.subheader("📊 Données extraites")
    st.dataframe(df, use_container_width=True)

    # =========================
    # Export Excel
    # =========================
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Extraction")

    st.download_button(
        label="⬇️ Télécharger le fichier Excel",
        data=output.getvalue(),
        file_name="extraction_json.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
