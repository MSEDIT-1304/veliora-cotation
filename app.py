import streamlit as st
from datetime import datetime

# CONFIG
st.set_page_config(page_title="Veliora Pro", layout="centered")

PASSWORD = "veliora2026"

# SESSION
if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================
# 🔐 PAGE DE CONNEXION
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
# 🚗 APPLICATION PRINCIPALE
# =========================

st.title("🚗 VELIORA Cotation Pro")

# --- Infos véhicule
marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

date_mec = st.date_input("Date de mise en circulation")
km = st.number_input("Kilométrage", 0, 300000, 50000)

st.markdown("---")

# --- Calcul
if st.button("Calculer la cotation"):

    try:
        annee = date_mec.year
        age = datetime.now().year - annee

        # base simple (tu pourras améliorer après)
        base = 20000

        # décote âge
        decote_age = base * 0.08 * age

        # décote km
        km_moyen = age * 15000
        decote_km = (km - km_moyen) * 0.05

        resultat = base - decote_age - decote_km

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except:
        st.error("Erreur dans les données")

# =========================
# 👤 MODE PRO VENDEUR
# =========================

st.markdown("---")
st.subheader("👤 Mode vendeur")

nom = st.text_input("Nom client")
email = st.text_input("Email")

if st.button("Générer fiche client"):
    st.info(f"Fiche créée pour {nom}")
