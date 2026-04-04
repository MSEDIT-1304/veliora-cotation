import streamlit as st
from datetime import datetime

# CONFIG
st.set_page_config(page_title="Veliora Pro", layout="centered")

PASSWORD = "veliora2026"

# SESSION
if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================
# 🔐 CONNEXION
# =========================
if not st.session_state.auth:

    st.title("🔒 VELIORA COTATION PRO")

    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")

    st.stop()

# =========================
# 🚗 FORMULAIRE PRO VENDEUR
# =========================

st.title("🚗 Création d'une cotation")

# --- Identification véhicule
immatriculation = st.text_input("Plaque d'immatriculation")

col1, col2 = st.columns(2)

with col1:
    marque = st.text_input("Marque")
    sous_version = st.text_input("Sous-version")
    generation = st.text_input("Génération")
    finition = st.text_input("Finition")
    carburant = st.text_input("Carburant")
    boite = st.text_input("Boîte")

with col2:
    modele = st.text_input("Modèle / Version")
    portes = st.text_input("Nombre de portes")
    phase = st.text_input("Phase")
    traction = st.text_input("Traction")
    moteur = st.text_input("Motorisation")
    techno_boite = st.text_input("Technologie de boîte")

# --- Infos techniques
st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    date_mec = st.date_input("Date de mise en circulation")
    km = st.number_input("Kilométrage", 0, 300000, 50000)

with col4:
    departement = st.text_input("Département")
    vendeur = st.text_input("Nom vendeur")

# =========================
# 💰 CALCUL
# =========================

st.markdown("---")

if st.button("Calculer la cotation"):

    try:
        annee = date_mec.year
        age = datetime.now().year - annee

        base = 20000

        decote_age = base * 0.08 * age
        km_moyen = age * 15000
        decote_km = (km - km_moyen) * 0.05

        resultat = base - decote_age - decote_km

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except:
        st.error("Erreur dans les données")

# =========================
# 👤 CLIENT
# =========================

st.markdown("---")
st.subheader("Client")

nom_client = st.text_input("Nom client")
email_client = st.text_input("Email")

if st.button("Créer fiche client"):
    st.info(f"Fiche créée pour {nom_client}")
