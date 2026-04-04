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

st.subheader("🚗 Informations véhicule")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

# =========================
# CARACTERISTIQUES
# =========================

st.subheader("⚙️ Caractéristiques")

carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])
permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])

traction = st.text_input("Traction (ex : 4WD)")
motorisation = st.text_input("Motorisation (ex : 2.0 CRDI 136)")

# =========================
# DATE
# =========================

st.subheader("📅 Date de première mise en circulation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1, 13)))

with col2:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

# =========================
# KM
# =========================

st.subheader("📊 Kilométrage")

km = st.number_input("Kilométrage", 0, 300000, 50000)

# =========================
# VENDEUR
# =========================

st.subheader("👤 Informations vendeur")

departement = st.text_input("Département")
vendeur = st.text_input("Nom vendeur")

# =========================
# CALCUL
# =========================

st.subheader("💰 Estimation")

if st.button("Calculer l'estimation"):

    try:
        age = datetime.now().year - annee + (datetime.now().month - mois)/12

        # 🔥 BASE REALISTE SUV / compact
        base = 22000

        # décote réaliste
        valeur = base - (age * 1200)

        # ajustement kilométrage
        km_moyen = age * 15000
        valeur -= (km - km_moyen) * 0.05

        # carburant
        if carburant == "Diesel":
            valeur *= 0.95
        elif carburant == "Hybride":
            valeur *= 1.05
        elif carburant == "Électrique":
            valeur *= 1.1

        # boîte auto
        if boite == "Automatique":
            valeur *= 1.05

        # minimum sécurité
        valeur = max(valeur, 3000)

        # 💥 PRIX MARCHÉ PARTICULIER
        prix_bas = int(valeur * 0.9)
        prix_haut = int(valeur * 1.15)

        # =========================
        # AFFICHAGE PRO
        # =========================

        st.markdown("## 📊 COTATION RÉELLE (TON CAS PRÉCIS)")

        st.markdown(f"""
👉 Avec TON kilométrage ({km} km) + finition + caractéristiques :

### 💰 💥 PRIX MARCHÉ PARTICULIER

➡️ **{prix_bas} € → {prix_haut} €**
""")

    except Exception as e:
        st.error(f"Erreur : {e}")
