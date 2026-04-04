import streamlit as st
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- PASSWORD ----------------
PASSWORD = "veliora2026"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 VELIORA COTATION PRO")

    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True
        st.rerun()

    st.stop()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.big-title {font-size:32px; font-weight:700;}
.section {margin-top:30px;}
.result-box {
    background:#f5f7fa;
    padding:20px;
    border-radius:10px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='big-title'>🚗 VELIORA COTATION PRO</div>", unsafe_allow_html=True)
st.info("💡 Plus tu remplis d’informations, plus l’estimation sera précise.")

# ---------------- FORM ----------------
st.markdown("### 🔎 Informations véhicule")

col1, col2 = st.columns(2)

with col1:
    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")
    sous_version = st.text_input("Sous-version")

with col2:
    finition = st.text_input("Finition")
    motorisation = st.text_input("Motorisation")

carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])
permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])

st.markdown("### 📅 Date de première mise en circulation")

col3, col4 = st.columns(2)

with col3:
    mois = st.selectbox("Mois", list(range(1,13)))
with col4:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

km = st.number_input("Kilométrage", 0, 400000, 90000)

options = st.multiselect(
    "Options",
    [
        "GPS",
        "Caméra de recul",
        "Attelage",
        "Sièges chauffants",
        "Jantes alliage",
        "Bluetooth",
        "Régulateur"
    ]
)

# ---------------- ESTIMATION ----------------
st.markdown("## 💰 Estimation")

if st.button("Calculer l'estimation"):

    age = datetime.now().year - annee

    # ---------------- BASE PRIX PAR TYPE ----------------
    base = 20000

    if carburant == "Diesel":
        base += 2000
    if carburant == "Hybride":
        base += 3000
    if carburant == "Électrique":
        base += 5000

    if boite == "Automatique":
        base += 1500

    # ---------------- AJUSTEMENTS AGE ----------------
    base -= age * 1200

    # ---------------- AJUSTEMENTS KM ----------------
    if km > 100000:
        base -= 2000
    if km > 150000:
        base -= 3000

    # ---------------- OPTIONS ----------------
    base += len(options) * 300

    # ---------------- CORRECTION MARCHÉ ----------------
    # évite prix absurdes
    if base < 5000:
        base = 5000

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2000)

    # ---------------- AFFICHAGE ----------------
    st.markdown("## 📊 COTATION RÉELLE (ESTIMATION MARCHÉ)")

    st.markdown(f"""
    👉 Avec ton véhicule :

    ### 🔻 Prix bas
    ➡️ {prix_bas} €

    ### ⚖️ Prix marché
    ➡️ {prix_moyen} €

    ### 🔺 Prix haut
    ➡️ {prix_haut} €
    """)

    st.success("✅ Estimation basée sur logique marché France (approximative)")
