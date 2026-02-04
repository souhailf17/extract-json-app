import streamlit as st
import re
from urllib.parse import urlparse
from docx import Document

# -----------------------------
# Fonctions
# -----------------------------

def extract_urls(text):
    """Extraire toutes les URLs depuis un texte"""
    url_pattern = r'https?://[^\s"\'>]+'
    return re.findall(url_pattern, text)

def clean_url(url):
    """Nettoyer une URL pour garder seulement https://domaine"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# -----------------------------
# Interface Streamlit
# -----------------------------

st.set_page_config(page_title="URL Cleaner", layout="centered")

st.title("🧹 Nettoyage des liens (URL Cleaner)")
st.write("Uploader un fichier **.txt** ou **.docx** pour extraire et nettoyer les liens.")

uploaded_file = st.file_uploader(
    "📤 Choisir un fichier",
    type=["txt", "docx"]
)

if uploaded_file:
    # Lecture du fichier
    if uploaded_file.name.endswith(".txt"):
        content = read_txt(uploaded_file)
    else:
        content = read_docx(uploaded_file)

    # Extraction des URLs
    urls = extract_urls(content)

    if urls:
        cleaned_urls = sorted(set(clean_url(url) for url in urls))

        st.success(f"✅ {len(cleaned_urls)} domaine(s) trouvé(s)")

        st.subheader("🔗 Liens nettoyés")
        for url in cleaned_urls:
            st.write(url)

        # Téléchargement
        output_text = "\n".join(cleaned_urls)
        st.download_button(
            label="⬇️ Télécharger le résultat (.txt)",
            data=output_text,
            file_name="urls_nettoyees.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ Aucun lien trouvé dans le fichier.")
