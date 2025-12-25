import streamlit as st
import pandas as pd

st.title("Comparaison de fichiers Excel et extraction des données")

# Upload des fichiers
file1 = st.file_uploader("Upload du premier fichier Excel (ID , ACT)", type=["xlsx"], key="file1")
file2 = st.file_uploader("Upload du deuxième fichier Excel (proc_id , N json , proc_title", type=["xlsx"], key="file2")

def process_files(df1, df2):
    # Supprimer les espaces autour des noms de colonnes
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Renommer les colonnes pour correspondre au script
    df1.rename(columns={'ID': 'id', 'ACT': 'act'}, inplace=True)

    # Vérifier les colonnes nécessaires
    if not all(col in df1.columns for col in ['id', 'act']):
        st.error("Le premier fichier doit contenir les colonnes 'ID' et 'ACT'.")
        return None
    if not all(col in df2.columns for col in ['proc_id', 'proc_title', 'N json']):
        st.error("Le deuxième fichier doit contenir les colonnes 'proc_id', 'proc_title' et 'N json'.")
        return None

    # Convertir les colonnes ID en string pour éviter les problèmes de type
    df1['id'] = df1['id'].astype(str)
    df2['proc_id'] = df2['proc_id'].astype(str)

    # Merge des fichiers sur les colonnes correspondantes
    merged_df = pd.merge(df1, df2, left_on=['id', 'act'], right_on=['proc_id', 'proc_title'], how='inner')

    # Supprimer les espaces dans les noms de colonnes après merge
    merged_df.columns = merged_df.columns.str.strip()

    # Extraire les colonnes demandées
    result_df = merged_df[['id', 'N json', 'act']]

    return result_df

# Si les deux fichiers sont uploadés
if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        result_df = process_files(df1, df2)

        if result_df is not None and not result_df.empty:
            st.success("Extraction terminée ! Voici un aperçu :")
            st.dataframe(result_df)

            # Bouton pour télécharger le fichier résultant
            result_file = "result.xlsx"
            result_df.to_excel(result_file, index=False)
            with open(result_file, "rb") as f:
                st.download_button("Télécharger le fichier Excel", f, file_name="result.xlsx")
        else:
            st.warning("Aucune correspondance trouvée entre les fichiers.")
    except Exception as e:
        st.error(f"Erreur lors du traitement : {e}")
