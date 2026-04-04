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
# OPTIONS
# =========================

st.subheader("✨ Options supplémentaires")

options = st.text_area(
    "Exemples : sièges chauffants, caméra de recul, attelage, GPS, toit ouvrant..."
)

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

        base = 22000
        valeur = base - (age * 1200)

        km_moyen = age * 15000
        valeur -= (km - km_moyen) * 0.05

        # carburant
        if carburant == "Diesel":
            valeur *= 0.95
        elif carburant == "Hybride":
            valeur *= 1.05
        elif carburant == "Électrique":
            valeur *= 1.1

        # boîte
        if boite == "Automatique":
            valeur *= 1.05

        # =========================
        # BONUS OPTIONS 🔥
        # =========================

        bonus = 0

        options_lower = options.lower()

        if "cuir" in options_lower:
            bonus += 500
        if "gps" in options_lower or "navigation" in options_lower:
            bonus += 300
        if "camera" in options_lower:
            bonus += 300
        if "attelage" in options_lower:
            bonus += 200
        if "chauffant" in options_lower:
            bonus += 200
        if "toit ouvrant" in options_lower:
            bonus += 400
        if "led" in options_lower:
            bonus += 200

        valeur += bonus

        # sécurité
        valeur = max(valeur, 3000)

        # =========================
        # PRIX MARCHÉ
        # =========================

        prix_bas = int(valeur * 0.85)
        prix_moyen = int(valeur)
        prix_haut = int(valeur * 1.20)

        # =========================
        # AFFICHAGE
        # =========================

        st.markdown("## 📊 COTATION RÉELLE (TON CAS PRÉCIS)")

        st.markdown(f"""
👉 Avec TON kilométrage ({km} km) + finition + caractéristiques :

### 🔻 Prix bas (vente rapide / état moyen)
➡️ **{prix_bas} €**

### ⚖️ Prix marché (normal)
➡️ **{prix_moyen} €**

### 🔺 Prix haut (véhicule propre / optimisé)
➡️ **{prix_haut} €**
""")

        if bonus > 0:
            st.info(f"✨ Impact des options : +{bonus} €")

    except Exception as e:
        st.error(f"Erreur : {e}")
