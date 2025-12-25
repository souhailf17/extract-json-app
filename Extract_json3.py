import streamlit as st
import pandas as pd

st.title("Comparaison de fichiers Excel et extraction des données")

# Upload du premier fichier Excel
file1 = st.file_uploader("Upload du premier fichier Excel", type=["xlsx"])
# Upload du deuxième fichier Excel
file2 = st.file_uploader("Upload du deuxième fichier Excel", type=["xlsx"])

if file1 and file2:
    # Lire les fichiers Excel
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Vérifier si les colonnes nécessaires existent
    if 'id' not in df1.columns or 'act' not in df1.columns:
        st.error("Le premier fichier doit contenir les colonnes 'id' et 'act'.")
    elif 'proc_id' not in df2.columns or 'proc_title' not in df2.columns or 'N json' not in df2.columns:
        st.error("Le deuxième fichier doit contenir les colonnes 'proc_id', 'proc_title' et 'N json'.")
    else:
        # Merge des fichiers sur les colonnes correspondantes
        merged_df = pd.merge(df1, df2, left_on=['id', 'act'], right_on=['proc_id', 'proc_title'], how='inner')

        # Sélectionner uniquement les colonnes demandées
        result_df = merged_df[['id', 'N json', 'act']]

        st.success("Extraction terminée ! Voici un aperçu :")
        st.dataframe(result_df)

        # Bouton pour télécharger le fichier résultant
        output_file = "result.xlsx"
        result_df.to_excel(output_file, index=False)
        with open(output_file, "rb") as f:
            st.download_button("Télécharger le fichier Excel", f, file_name="result.xlsx")
