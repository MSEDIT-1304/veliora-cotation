import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time

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

# ---------------- AUTH ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 Accès Veliora Pro")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit"])

    with tab1:
        user = st.text_input("Utilisateur", key="login_user")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter", key="btn_login"):
            users = load_users()

            if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()

            if user in users and users[user]["password"] == pwd:
                valid, _ = check_access(users[user])
                if not valid:
                    st.error("Accès expiré")
                    st.markdown(f"[S'abonner]({PAYMENT_LINK})")
                    st.stop()

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    with tab2:
        new_user = st.text_input("Créer un utilisateur", key="trial_user")
        new_pwd = st.text_input("Mot de passe", type="password", key="trial_pwd")

        if st.button("Créer essai", key="btn_trial"):
            users = load_users()
            if new_user in users:
                st.error("Utilisateur déjà existant")
            else:
                create_trial(new_user, new_pwd)
                st.success("Compte créé")

    st.stop()

# ---------------- APP ----------------

st.title("🚗 VELIORA COTATION EXPERT")

marques = [
    "Audi","BMW","Mercedes","Volkswagen","Peugeot","Renault","Citroën","DS",
    "Toyota","Hyundai","Kia","Ford","Nissan","Honda","Mazda","Volvo",
    "Skoda","Seat","Cupra","Fiat","Alfa Romeo","Jeep","Dacia","Opel"
]

marque = st.selectbox("Marque", marques)
modele = st.text_input("Modèle")
annee = st.number_input("Année", 1990, datetime.now().year, 2018)
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
motorisation = st.text_input("Motorisation")
portes = st.selectbox("Portes", [1,2,3,4,5])

options = st.multiselect("Options", ["GPS","Caméra","Cuir","Toit pano","Audio"])

# ---------------- CALCUL ----------------

if st.button("🚀 Estimer"):

    with st.spinner("Analyse marché..."):
        time.sleep(1)

    age = datetime.now().year - annee

    # SEGMENT
    modele_lower = modele.lower()
    if "suv" in modele_lower or "3008" in modele_lower:
        prix_neuf = 32000
    elif "clio" in modele_lower or "208" in modele_lower:
        prix_neuf = 18000
    else:
        prix_neuf = 25000

    # PREMIUM
    if marque.lower() in ["bmw","audi","mercedes"]:
        prix_neuf *= 1.5

    # DÉCOTE
    valeur = prix_neuf * 0.8
    for i in range(age):
        valeur *= 0.9

    # KM
    km_moyen = age * 15000
    valeur += (km_moyen - km) * 0.02

    # PORTES
    if portes <= 2:
        valeur *= 0.93
    elif portes == 5:
        valeur *= 1.03

    # BOITE
    if boite == "Automatique":
        valeur *= 1.05

    # CARBURANT
    if carburant == "Diesel":
        valeur *= 0.95
    if carburant == "Électrique":
        valeur *= 1.2

    # OPTIONS
    valeur += len(options) * 150

    if valeur < 3000:
        valeur = 3000

    prix_bas = int(valeur * 0.9)
    prix_haut = int(valeur * 1.1)
    reprise = int(valeur * 0.8)

    # SCORE
    score = 50
    if km < km_moyen:
        score += 10
    if boite == "Automatique":
        score += 5
    if carburant == "Électrique":
        score += 10

    # VERDICT
    if score > 70:
        verdict = "🔥 Bonne affaire"
    elif score > 55:
        verdict = "✅ Prix correct"
    else:
        verdict = "⚠️ Surcoté"

    st.markdown(f"""
## 💰 {prix_bas} € - {prix_haut} €
### Reprise pro : {reprise} €
### Score : {score}/100
### {verdict}
""")
