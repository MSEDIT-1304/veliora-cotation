import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://ton-lien-stripe.com"
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

# ADMIN sécurisé
users[ADMIN_USERNAME] = {"password": ADMIN_PASSWORD, "expire": None, "trial": False}
save_users(users)

# ---------------- TRIAL ----------------
def create_trial(username, password):
    users = load_users()
    users[username] = {
        "password": password,
        "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "trial": True
    }
    save_users(users)

# ---------------- CHECK ----------------
def check_access(user):
    if user["expire"] is None:
        return True, None

    expire = datetime.strptime(user["expire"], "%Y-%m-%d")
    now = datetime.now()

    if now > expire:
        return False, "expired"

    if expire - now <= timedelta(days=7):
        return True, "warning"

    return True, None

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 Accès Veliora Pro")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

    with tab1:
        user = st.text_input("Utilisateur")
        pwd = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):

            users = load_users()

            # ADMIN
            if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()

            # CLIENT
            if user in users and users[user]["password"] == pwd:

                valid, status = check_access(users[user])

                if not valid:
                    st.error("⛔ Accès expiré")
                    st.markdown(f"[💳 S'abonner]({PAYMENT_LINK})")
                    st.stop()

                if status == "warning":
                    st.warning("⚠️ Expiration proche")

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("Identifiants incorrects")

    with tab2:
        new_user = st.text_input("Créer un utilisateur")
        new_pwd = st.text_input("Mot de passe", type="password")

        if st.button("Créer essai"):
            if new_user in users:
                st.error("Existe déjà")
            else:
                create_trial(new_user, new_pwd)
                st.success("Compte créé")

    st.stop()

# ---------------- APP ----------------

st.write(f"👤 Connecté : {st.session_state.user}")

st.title("🚗 VELIORA COTATION PRO")

st.info("💡 Plus tu remplis d’informations, plus l’estimation sera précise.")

# ---------------- FORMULAIRE COMPLET ----------------

marques = [
    "Audi","BMW","Mercedes","Volkswagen","Peugeot","Renault",
    "Toyota","Hyundai","Kia","Ford","Nissan","Volvo"
]

marque = st.selectbox("Marque", marques)
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")

col1, col2 = st.columns(2)

with col1:
    finition = st.text_input("Finition")
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    motorisation = st.text_input("Motorisation")
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

options = st.multiselect("Options", [
    "GPS","Caméra recul","Radar","Jantes alliage","Cuir",
    "Toit pano","Bluetooth","CarPlay","Régulateur"
])

# ---------------- ESTIMATION ----------------

if st.button("Calculer l'estimation"):

    age = datetime.now().year - int(annee)
    base = 15000

    if marque.lower() in ["mercedes","bmw","audi"]:
        base += 7000

    if "tiguan" in modele.lower():
        base = 26000

    if "ix35" in modele.lower():
        base = 12000

    if "amg" in finition.lower():
        base += 4000

    if boite == "Automatique":
        base += 1500

    if carburant == "Diesel":
        base += 800

    if portes >= 5:
        base += 300

    base -= age * 1200

    if km > 80000:
        base -= 1000

    base += len(options) * 300

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2500)

    st.markdown(f"""
## 📊 COTATION

🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} €  
🔺 Haut : {prix_haut} €
""")
