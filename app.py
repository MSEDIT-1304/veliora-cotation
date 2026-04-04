import streamlit as st
from datetime import datetime
import webbrowser

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Veliora Pro", layout="centered")

# =========================
# DESIGN PRO
# =========================

st.markdown("""
<style>
.main {background-color: #f5f7fb;}
h1 {color: #1f2c56; font-weight: 700;}
.section {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.stButton button {
    background-color: #1f77ff;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("🚗 Informations véhicule")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CARACTERISTIQUES
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("⚙️ Caractéristiques")

col1, col2 = st.columns(2)

with col1:
    carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
    boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])

with col2:
    traction = st.text_input("Traction")
    motorisation = st.text_input("Motorisation")

permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DATE
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📅 Date de première mise en circulation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1, 13)))

with col2:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# KM
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📊 Kilométrage")

km = st.number_input("Kilométrage du véhicule", 0, 300000, 50000)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INFOS VENDEUR
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("👤 Informations vendeur")

departement = st.text_input("Département")
vendeur = st.text_input("Nom vendeur")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CALCUL COTATION
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("💰 Estimation")

if st.button("Calculer l'estimation"):

    try:
        age = datetime.now().year - annee + (datetime.now().month - mois)/12

        base = 18000
        valeur = base * (0.78 ** age)

        km_moyen = age * 15000
        valeur -= (km - km_moyen) * 0.07

        if carburant == "Diesel":
            valeur *= 0.9
        elif carburant == "Hybride":
            valeur *= 1.05
        elif carburant == "Électrique":
            valeur *= 1.08

        if boite == "Automatique":
            valeur *= 1.03

        # 🔥 PRIX MARCHÉ PARTICULIER
        prix_bas = int(valeur * 0.9)
        prix_haut = int(valeur * 1.15)

        # 🔥 AFFICHAGE PRO
        st.markdown("## 📊 COTATION RÉELLE (TON CAS PRÉCIS)")

        st.markdown(f"""
👉 Avec TON kilométrage ({km} km) + finition + caractéristiques :

### 💰 💥 PRIX MARCHÉ PARTICULIER

➡️ **{prix_bas} € → {prix_haut} €**
""")

    except Exception as e:
        st.error(f"Erreur : {e}")

st.markdown('</div>', unsafe_allow_html=True)
