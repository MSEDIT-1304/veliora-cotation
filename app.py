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

# ---------------- LISTE MARQUES ----------------
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

# ---------------- DATE ----------------
st.markdown("### 📅 Date de première mise en circulation")

col3, col4 = st.columns(2)

with col3:
    mois = st.selectbox("Mois", list(range(1,13)))

with col4:
    annee = st.selectbox("Année", list(range(2000, datetime.now().year + 1)))

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

# ---------------- ESTIMATION ----------------
st.markdown("## 💰 Estimation")

if st.button("Calculer l'estimation"):

    age = datetime.now().year - annee

    base = 12000

    # ---------------- FIX PREMIUM ----------------
    marque_lower = marque.lower()

    if marque_lower in ["mercedes", "bmw", "audi"]:
        base = 22000

    if marque_lower in ["porsche", "tesla"]:
        base = 35000

    # ---------------- TYPE VEHICULE ----------------
    if "suv" in modele.lower() or "tiguan" in modele.lower():
        base += 4000

    if "cla" in modele.lower() or "coup" in modele.lower():
        base += 3000

    # ---------------- FINITION ----------------
    if "amg" in finition.lower():
        base += 5000

    if "rs" in finition.lower() or "gt" in finition.lower():
        base += 6000

    # ---------------- BOITE ----------------
    if boite == "Automatique":
        base += 2000

    # ---------------- CARBURANT ----------------
    if carburant == "Diesel":
        base += 1000

    if carburant == "Hybride":
        base += 2000

    if carburant == "Électrique":
        base += 4000

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

    st.success("✅ Estimation basée sur logique marché vendeur")
