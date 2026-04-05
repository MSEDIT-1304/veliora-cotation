import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "TonMotDePasseFort123!"
FILE_PATH = "users.json"

# ---------------- USERS ----------------
def load_users():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

users = load_users()

if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
        "trial": False
    }
    save_users(users)

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Accès Veliora Pro")

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):
        if user in users and users[user]["password"] == pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    st.stop()

# ---------------- APP ----------------
st.write(f"👤 Connecté : {st.session_state.user}")

st.markdown("## 🔐 Accès professionnel")
st.success("✔️ Accès actif")

st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):
    users[st.session_state.user]["expire"] = (
        datetime.now() + timedelta(days=365)
    ).strftime("%Y-%m-%d")
    save_users(users)
    st.success("🎉 Abonnement activé pour 1 an")

st.divider()

# ---------------- FORMULAIRE ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")

col1, col2 = st.columns(2)

with col1:
    finition = st.text_input("Finition")
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
    techno = st.selectbox(
        "Technologie de boîte",
        ["-", "DSG", "EDC", "CVT", "BVA", "BVA6", "BVA7", "BVA8"]
    )

with col2:
    motorisation = st.text_input("Motorisation")
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4", "4WD"])
    etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])
    commission = st.number_input("Commission (€)", 0, 10000, 1000)

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

# ---------------- OPTIONS ----------------
options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique",
        "Accès sans clé",
        "Hayon électrique",

        "Sellerie cuir",
        "Sièges chauffants avant",
        "Sièges chauffants avant + arrière",
        "Sièges électriques",

        "Régulateur de vitesse",
        "Régulateur adaptatif",

        "Radar de recul",
        "Bips avant",
        "Bips arrière",
        "Caméra de recul",
        "Caméra 360",

        "GPS / Navigation",

        "Bluetooth",
        "Connexion Apple CarPlay",
        "Connexion Android Auto",

        "Système audio premium",

        "Rétroviseurs chauffants",
        "Rétroviseurs électriques rabattables",

        "Jantes alliage",
        "Toit ouvrant",
        "Toit panoramique",

        "Feux LED",

        "Attelage",

        "Détecteur angle mort"
    ]
)

# ---------------- ESTIMATION ----------------
if st.button("Calculer l'estimation"):

    base = 20000
    age = datetime.now().year - annee

    # SEGMENT
    if "suv" in modele.lower() or "3008" in modele.lower():
        base += 3000
    if "clio" in modele.lower() or "208" in modele.lower():
        base -= 3000

    # PREMIUM
    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 4000

    # BOITE
    if boite == "Automatique":
        base += 1500

    # TECHNO BOITE
    if techno in ["DSG","EDC"]:
        base += 500
    if techno in ["BVA6","BVA7","BVA8"]:
        base += 700

    # CARBURANT
    if carburant == "Diesel":
        base += 500
    elif carburant == "Hybride":
        base += 3000
    elif carburant == "Électrique":
        base += 6000

    # TRANSMISSION
    if traction in ["4x4","4WD"]:
        base += 1200

    # ETAT
    if etat == "Excellent état":
        base += 1500

    # AGE
    base -= age * 800

    # KM
    if km > 80000:
        base -= 800
    if km > 120000:
        base -= 1500

    # OPTIONS pondérées
    bonus = 0
    for opt in options:
        if opt in ["Sellerie cuir","Toit panoramique","Caméra 360","Système audio premium"]:
            bonus += 500
        elif opt in ["GPS / Navigation","Caméra de recul","Sièges chauffants avant"]:
            bonus += 300
        else:
            bonus += 150

    base += bonus

    # PRIX (-650 comme demandé)
    prix_bas = int(base - 1500 - 650)
    prix_moyen = int(base - 650)
    prix_haut = int(base + 2500 - 650)

    # NET VENDEUR
    net_bas = prix_bas - commission
    net_moyen = prix_moyen - commission
    net_haut = prix_haut - commission

    # INDICATEUR
    if prix_moyen < base:
        label = "🟢 Bonne affaire"
    elif prix_moyen < base + 1000:
        label = "🟢 Très bonne affaire"
    else:
        label = "🔴 Prix élevé"

    st.markdown("## 📊 ESTIMATION PRO")

    st.markdown(f"""
### 💰 Prix de vente
🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} € {label}  
🔺 Haut : {prix_haut} €

### 🧾 Prix net vendeur
🔻 Bas : {net_bas} €  
⚖️ Moyen : {net_moyen} €  
🔺 Haut : {net_haut} €
""")
