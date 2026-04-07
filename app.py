import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random

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

# ---------------- USER DATA ----------------
user_data = users[st.session_state.user]

# ---------------- HEADER ----------------
st.write(f"👤 Connecté : {st.session_state.user}")

# ---------------- TRIAL 7 JOURS ----------------
if not user_data.get("trial", False) and not user_data.get("expire"):
    if st.button("🎁 Essai gratuit 7 jours"):
        users[st.session_state.user]["trial"] = True
        users[st.session_state.user]["expire"] = (
            datetime.now() + timedelta(days=7)
        ).strftime("%Y-%m-%d")
        save_users(users)
        st.success("🚀 Essai gratuit activé pour 7 jours !")
        st.rerun()

# ---------------- VERIFICATION ACCES ----------------
if user_data.get("expire"):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")

    if datetime.now() > expire_date:
        st.error("⛔ Votre accès a expiré")
        st.markdown(f"[💳 S’abonner pour continuer]({PAYMENT_LINK})")
        st.stop()

# ---------------- INFO TRIAL ----------------
if user_data.get("trial", False):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")
    jours_restants = (expire_date - datetime.now()).days
    st.info(f"🎁 Essai gratuit actif – {jours_restants} jour(s) restant(s)")

# ---------------- PAIEMENT ----------------
st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):
    users[st.session_state.user]["expire"] = (
        datetime.now() + timedelta(days=365)
    ).strftime("%Y-%m-%d")
    users[st.session_state.user]["trial"] = False
    save_users(users)
    st.success("🎉 Abonnement activé pour 1 an")

st.divider()

# ---------------- FORMULAIRE ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois de mise en circulation", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
    techno = st.selectbox("Technologie de boîte", ["-", "DSG", "EDC", "CVT", "BVA", "BVA6", "BVA7", "BVA8"])
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4", "4WD"])

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants avant","Sièges chauffants avant + arrière",
        "Sièges électriques","Régulateur de vitesse","Régulateur adaptatif",
        "Radar de recul","Bips avant","Bips arrière","Caméra de recul","Caméra 360",
        "GPS / Navigation","Bluetooth","Connexion Apple CarPlay","Connexion Android Auto",
        "Système audio premium","Rétroviseurs chauffants","Rétroviseurs électriques rabattables",
        "Jantes alliage","Toit ouvrant","Toit panoramique","Feux LED","Attelage","Détecteur angle mort"
    ]
)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Calculer l'estimation"):

    base = 17000
    age = datetime.now().year - annee

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 3000

    if boite == "Automatique":
        base += 1200

    if techno in ["DSG","EDC"]:
        base += 400
    if techno in ["BVA6","BVA7","BVA8"]:
        base += 500

    if carburant == "Diesel":
        base += 300
    elif carburant == "Hybride":
        base += 2500
    elif carburant == "Électrique":
        base += 5000

    if traction in ["4x4","4WD"]:
        base += 800

    if etat == "Excellent état":
        base += 1200
    else:
        base -= 500

    base -= age * 900

    if km > 80000:
        base -= 1200
    if km > 120000:
        base -= 2000

    base += len(options) * 100

    base *= 0.90

    annonces = []

    for i in range(5):
        km_a = max(10000, km + random.randint(-40000, 40000))
        prix_a = base + random.randint(-2000, 2000)

        if km_a > km:
            prix_a -= (km_a - km) * 0.02
        else:
            prix_a += (km - km_a) * 0.02

        annonces.append((int(km_a), int(prix_a)))

    annonces = sorted(annonces, key=lambda x: x[0])

    prix_moyen = int(sum([p for _, p in annonces]) / len(annonces))
    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    if prix_moyen < prix_moyen - 500:
        badge = "🟢 Bonne affaire"
    elif prix_moyen <= prix_moyen + 800:
        badge = "🟡 Prix marché"
    else:
        badge = "🔴 Trop cher"

    net = prix_moyen - commission

    st.markdown("## 📊 ESTIMATION")

    st.markdown(f"""
### 💰 Prix de vente
🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} € {badge}  
🔺 Haut : {prix_haut} €

### 🧾 Net vendeur
➡️ {net} €
""")

    st.markdown("## 📈 COMPARATIF ANNONCES")

    for km_a, prix_a in annonces:
        st.write(f"🚗 {km_a} km → {prix_a} €")
