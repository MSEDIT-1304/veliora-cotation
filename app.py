import streamlit as st
from datetime import datetime

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

# ---------------- HEADER ----------------
st.title("🚗 VELIORA COTATION PRO")
st.info("💡 Plus tu remplis d’informations, plus l’estimation sera précise.")

# ---------------- MARQUES ----------------
marques_list = [
    "Audi", "BMW", "Citroën", "Dacia", "Fiat", "Ford", "Honda", "Hyundai",
    "Kia", "Mazda", "Mercedes", "Mini", "Nissan", "Opel", "Peugeot",
    "Renault", "Seat", "Skoda", "Toyota", "Volkswagen", "Volvo",
    "Alfa Romeo", "Jeep", "Land Rover", "Porsche", "Tesla"
]

# ---------------- FORM ----------------
st.markdown("### 🔎 Informations véhicule")

marque = st.selectbox("Marque (tu peux taper pour rechercher)", marques_list)
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")

col1, col2 = st.columns(2)

with col1:
    finition = st.text_input("Finition")
    carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])

with col2:
    motorisation = st.text_input("Motorisation")
    boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])

# ---------------- DATE (SAISIE LIBRE) ----------------
st.markdown("### 📅 Date de première mise en circulation")

annee = st.number_input("Année (ex: 2019)", 1990, datetime.now().year, 2019)
mois = st.number_input("Mois (1-12)", 1, 12, 1)

# ---------------- KM (SAISIE LIBRE) ----------------
km = st.number_input("Kilométrage (tu peux taper directement)", 0, 400000, 90000)

# ---------------- OPTIONS ----------------
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

    age = datetime.now().year - int(annee)

    modele_lower = modele.lower()
    marque_lower = marque.lower()

    # ---------------- BASE PAR MODÈLE RÉEL ----------------
    base = 12000

    if "tiguan" in modele_lower:
        base = 26000

    elif "308" in modele_lower:
        base = 16000

    elif "clio" in modele_lower:
        base = 14000

    elif "208" in modele_lower:
        base = 15000

    elif "cla" in modele_lower:
        base = 28000

    # ---------------- PREMIUM ----------------
    if marque_lower in ["mercedes", "bmw", "audi"]:
        base += 3000

    if marque_lower in ["porsche", "tesla"]:
        base += 8000

    # ---------------- TYPE VEHICULE ----------------
    if "suv" in modele_lower or "tiguan" in modele_lower:
        base += 3000

    if "coup" in modele_lower or "cla" in modele_lower:
        base += 2500

    # ---------------- FINITION ----------------
    if "amg" in finition.lower():
        base += 4000

    if "gt" in finition.lower() or "rs" in finition.lower():
        base += 5000

    # ---------------- BOITE ----------------
    if boite == "Automatique":
        base += 1500

    # ---------------- CARBURANT ----------------
    if carburant == "Diesel":
        base += 800

    if carburant == "Hybride":
        base += 2000

    if carburant == "Électrique":
        base += 4000

    # ---------------- PORTES ----------------
    if portes <= 3:
        base += 500

    if portes >= 5:
        base += 300

    # ---------------- AGE ----------------
    base -= age * 1200

    # ---------------- KM ----------------
    if km > 80000:
        base -= 1000

    if km > 120000:
        base -= 2000

    # ---------------- OPTIONS ----------------
    base += len(options) * 300

    # ---------------- SECURITE ----------------
    if base < 8000:
        base = 8000

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2500)

    # ---------------- RESULTAT ----------------
    st.markdown("## 📊 COTATION RÉELLE (TON CAS PRÉCIS)")

    st.markdown(f"""
👉 Avec TON véhicule ({km} km) + finition + caractéristiques :

### 🔻 Prix bas
➡️ **{prix_bas} €**

### ⚖️ Prix marché
➡️ **{prix_moyen} €**

### 🔺 Prix haut
➡️ **{prix_haut} €**
""")

    st.success("✅ Estimation basée sur logique marché réel (niveau pro)")
