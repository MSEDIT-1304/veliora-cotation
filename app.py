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

st.info("ℹ️ Pour une estimation la plus précise possible, renseignez un maximum d’informations sur le véhicule (options, état, motorisation...).")

# =========================
# INFOS VEHICULE
# =========================

st.subheader("🚗 Informations véhicule")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")

# =========================
# CARACTERISTIQUES
# =========================

st.subheader("⚙️ Caractéristiques")

carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])
permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])

# 🔥 NOMBRE DE PORTES AJOUTÉ
portes = st.selectbox("Nombre de portes", ["3 portes", "5 portes"])

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

st.subheader("✨ Options du véhicule")

options_list = [
    "Jantes alliage",
    "Attelage",
    "Caméra de recul",
    "GPS / Navigation",
    "Sièges chauffants avant",
    "Sièges chauffants avant + arrière",
    "Connexion téléphone / Bluetooth",
    "Android Auto / Apple CarPlay",
    "Toit ouvrant",
    "Feux LED / Xénon",
    "Sellerie cuir",
    "Radar de recul",
    "Régulateur de vitesse",
]

options_selected = st.multiselect("Sélectionne les options", options_list)

# =========================
# ETAT VEHICULE
# =========================

st.subheader("🚘 État du véhicule")

etat = st.selectbox(
    "État général",
    ["Mauvais", "Correct", "Bon", "Excellent"]
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
        modele_lower = modele.lower()

        # TYPE VEHICULE
        if any(x in modele_lower for x in ["clio", "208", "c3", "polo"]):
            base = 16000
        elif any(x in modele_lower for x in ["308", "megane", "golf"]):
            base = 19000
        elif any(x in modele_lower for x in ["3008", "qashqai", "tiguan", "ix35"]):
            base = 24000
        elif any(x in modele_lower for x in ["bmw", "audi", "mercedes"]):
            base = 35000
        else:
            base = 18000

        valeur = base - (age * 1400)

        km_moyen = age * 15000
        valeur -= (km - km_moyen) * 0.06

        # carburant
        if carburant == "Diesel":
            valeur *= 0.92
        elif carburant == "Hybride":
            valeur *= 1.03
        elif carburant == "Électrique":
            valeur *= 1.05

        # boîte
        if boite == "Automatique":
            valeur *= 1.03

        # 🔥 IMPACT PORTES
        if portes == "3 portes":
            valeur *= 0.95   # moins recherché
        elif portes == "5 portes":
            valeur *= 1.02   # plus recherché

        # OPTIONS
        bonus = 0

        for opt in options_selected:
            if opt == "Jantes alliage":
                bonus += 150
            elif opt == "Sellerie cuir":
                bonus += 300
            elif opt == "Toit ouvrant":
                bonus += 300
            elif opt == "GPS / Navigation":
                bonus += 200
            elif opt == "Caméra de recul":
                bonus += 200
            elif opt == "Attelage":
                bonus += 150
            elif opt == "Sièges chauffants avant":
                bonus += 150
            elif opt == "Sièges chauffants avant + arrière":
                bonus += 200
            elif opt == "Android Auto / Apple CarPlay":
                bonus += 200
            elif opt == "Connexion téléphone / Bluetooth":
                bonus += 100
            elif opt == "Feux LED / Xénon":
                bonus += 150
            elif opt == "Radar de recul":
                bonus += 100
            elif opt == "Régulateur de vitesse":
                bonus += 100

        valeur += bonus

        # ETAT
        if etat == "Mauvais":
            valeur *= 0.75
        elif etat == "Correct":
            valeur *= 0.90
        elif etat == "Bon":
            valeur *= 1.00
        elif etat == "Excellent":
            valeur *= 1.10

        valeur = max(valeur, 3000)

        # PRIX FINAL
        prix_bas = int(valeur * 0.85)
        prix_moyen = int(valeur)
        prix_haut = int(valeur * 1.15)

        # AFFICHAGE
        st.markdown("## 📊 COTATION RÉELLE (TON CAS PRÉCIS)")

        st.markdown(f"""
👉 Avec TON kilométrage ({km} km) + état du véhicule :

### 🔻 Prix bas
➡️ **{prix_bas} €**

### ⚖️ Prix marché
➡️ **{prix_moyen} €**

### 🔺 Prix haut
➡️ **{prix_haut} €**
""")

        if bonus > 0:
            st.info(f"✨ Impact des options : +{bonus} €")

    except Exception as e:
        st.error(f"Erreur : {e}")
