import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Veliora Pro", layout="centered")

# =========================
# DESIGN PRO
# =========================

st.markdown("""
<style>

/* Fond */
.main {
    background-color: #f5f7fb;
}

/* Titre */
h1 {
    color: #1f2c56;
    font-weight: 700;
}

/* Sections */
.section {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    border-radius: 10px !important;
}

/* Bouton */
.stButton button {
    background-color: #1f77ff;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
}

.stButton button:hover {
    background-color: #155edc;
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
# INFOS VENDEUR
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("👤 Informations vendeur")

col1, col2 = st.columns(2)

with col1:
    km = st.number_input("Kilométrage", 0, 300000, 50000)

with col2:
    departement = st.text_input("Département")
    vendeur = st.text_input("Nom vendeur")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CALCUL
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("💰 Résultat")

if st.button("Calculer la cotation"):

    try:
        age = datetime.now().year - annee + (datetime.now().month - mois)/12

        base = 20000

        decote_age = base * 0.08 * age

        km_moyen = age * 15000
        decote_km = (km - km_moyen) * 0.05

        # carburant
        bonus_carburant = 0
        if carburant == "Électrique":
            bonus_carburant = 2000
        elif carburant == "Hybride":
            bonus_carburant = 1000
        elif carburant == "Diesel":
            bonus_carburant = -500

        # boîte
        bonus_boite = 0
        if boite == "Automatique":
            bonus_boite = 800

        # permis
        bonus_permis = 0
        if permis == "Sans permis":
            bonus_permis = -3000

        resultat = base - decote_age - decote_km + bonus_carburant + bonus_boite + bonus_permis

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except Exception as e:
        st.error(f"Erreur : {e}")

st.markdown('</div>', unsafe_allow_html=True)
