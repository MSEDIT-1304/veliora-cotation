import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Veliora Pro", layout="centered")

PASSWORD = "veliora2026"

# =========================
# LOGIN
# =========================

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 VELIORA COTATION PRO")
    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True
        st.rerun()

    st.stop()

# =========================
# TITRE
# =========================

st.title("🚗 Veliora Cotation Pro")

# =========================
# INFOS VEHICULE
# =========================

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

col1, col2 = st.columns(2)

with col1:
    carburant = st.text_input("Carburant (essence, diesel, hybride, électrique)")
    boite = st.text_input("Boîte (manuelle ou automatique)")

with col2:
    traction = st.text_input("Traction")
    motorisation = st.text_input("Motorisation")

# =========================
# DATE PREMIERE MISE EN CIRCULATION
# =========================

st.markdown("### 📅 Date de première mise en circulation")

col_date1, col_date2 = st.columns(2)

with col_date1:
    mois = st.selectbox("Mois", list(range(1, 13)))

with col_date2:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

# =========================
# INFOS COMPLEMENTAIRES
# =========================

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    km = st.number_input("Kilométrage", 0, 300000, 50000)

with col4:
    departement = st.text_input("Département")
    vendeur = st.text_input("Nom vendeur")

# =========================
# CALCUL
# =========================

st.markdown("---")

if st.button("Calculer la cotation"):

    try:
        age = datetime.now().year - annee + (datetime.now().month - mois)/12

        base = 20000

        decote_age = base * 0.08 * age

        km_moyen = age * 15000
        decote_km = (km - km_moyen) * 0.05

        bonus_carburant = 0
        if carburant:
            if "electrique" in carburant.lower():
                bonus_carburant = 2000
            elif "hybride" in carburant.lower():
                bonus_carburant = 1000
            elif "diesel" in carburant.lower():
                bonus_carburant = -500

        bonus_boite = 0
        if boite:
            if "auto" in boite.lower():
                bonus_boite = 800

        resultat = base - decote_age - decote_km + bonus_carburant + bonus_boite

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except Exception as e:
        st.error(f"Erreur : {e}")
