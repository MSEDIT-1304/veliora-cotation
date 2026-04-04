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

# ---------------- LISTE MARQUES ----------------
marques_list = [
    "Audi", "BMW", "Citroën", "Dacia", "Fiat", "Ford", "Honda", "Hyundai",
    "Kia", "Mazda", "Mercedes", "Mini", "Nissan", "Opel", "Peugeot",
    "Renault", "Seat", "Skoda", "Toyota", "Volkswagen", "Volvo",
    "Alfa Romeo", "Jeep", "Land Rover", "Porsche", "Tesla"
]

# ---------------- FORM ----------------
st.markdown("### 🔎 Informations véhicule")

# -------- MARQUE INTELLIGENTE --------
input_marque = st.text_input("Marque (tape au moins 3 lettres)")

suggestions = []
if len(input_marque) >= 3:
    suggestions = [m for m in marques_list if m.lower().startswith(input_marque.lower())]

if suggestions:
    marque = st.selectbox("Suggestions marques", suggestions)
else:
    marque = input_marque

col1, col2 = st.columns(2)

with col1:
    modele = st.text_input("Modèle")
    sous_version = st.text_input("Sous-version")

with col2:
    finition = st.text_input("Finition")
    motorisation = st.text_input("Motorisation")

carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])
permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])

# ---------------- DATE ----------------
st.markdown("### 📅 Date de première mise en circulation")

col3, col4 = st.columns(2)

with col3:
    mois = st.selectbox("Mois", list(range(1,13)))
with col4:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

# ---------------- INFOS ----------------
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

# ---------------- VENDEUR ----------------
st.markdown("### 👤 Informations vendeur")

nom_vendeur = st.text_input("Nom vendeur")
departement = st.text_input("Département")

# ---------------- ESTIMATION ----------------
st.markdown("## 💰 Estimation")

if st.button("Calculer l'estimation"):

    age = datetime.now().year - annee

    # ---------------- BASE ----------------
    base = 20000

    # carburant
    if carburant == "Diesel":
        base += 2000
    if carburant == "Hybride":
        base += 3000
    if carburant == "Électrique":
        base += 5000

    # boîte
    if boite == "Automatique":
        base += 1500

    # âge
    base -= age * 1200

    # km
    if km > 100000:
        base -= 2000
    if km > 150000:
        base -= 3000

    # options
    base += len(options) * 300

    # sécurité prix mini
    if base < 5000:
        base = 5000

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2000)

    # ---------------- RESULTAT ----------------
    st.markdown("## 📊 COTATION RÉELLE (ESTIMATION MARCHÉ)")

    st.markdown(f"""
👉 Avec TON véhicule :

### 🔻 Prix bas
➡️ {prix_bas} €

### ⚖️ Prix marché
➡️ {prix_moyen} €

### 🔺 Prix haut
➡️ {prix_haut} €
""")

    st.success("✅ Estimation basée sur logique marché France")
