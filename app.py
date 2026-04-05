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

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

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

                valid, status = check_access(users[user])

                if not valid:
                    st.error("⛔ Accès expiré")
                    st.markdown(f"[💳 S'abonner]({PAYMENT_LINK})")
                    st.stop()

                if status == "warning":
                    st.warning("⚠️ Votre accès expire bientôt")

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("❌ Identifiants incorrects")

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

st.write(f"👤 Connecté : {st.session_state.user}")

st.title("🚗 VELIORA COTATION PRO")
st.info("💡 Remplis les infos pour obtenir une estimation réaliste du marché.")

# ---------------- FORM ----------------

marques = [
    "Audi","BMW","Mercedes","Volkswagen","Peugeot","Renault",
    "Toyota","Hyundai","Kia","Ford","Nissan","Volvo"
]

marque = st.selectbox("Marque", marques, key="marque")
modele = st.text_input("Modèle", key="modele")
annee = st.number_input("Année", 1990, datetime.now().year, 2018, key="annee")
km = st.number_input("Kilométrage", 0, 400000, 90000, key="km")

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key="carburant")
boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key="boite")

motorisation = st.text_input("Motorisation (ex: 1.5 dCi 110)", key="motorisation")
portes = st.selectbox("Nombre de portes", [3, 5], key="portes")

options = st.multiselect(
    "Options",
    [
        "Climatisation","GPS","Caméra recul","Caméra 360",
        "Cuir","Toit panoramique","Sièges chauffants","Audio premium"
    ],
    key="options"
)

# ---------------- CALCUL ----------------

st.markdown("###")

if st.button("🚀 Calculer mon estimation", use_container_width=True, key="btn_calc"):

    with st.spinner("Analyse du marché en cours..."):
        time.sleep(1.2)

    age = datetime.now().year - int(annee)

    # 🔥 PRIX NEUF ESTIMÉ
    prix_neuf = 25000

    if marque.lower() in ["bmw", "mercedes", "audi"]:
        prix_neuf = 45000

    if "clio" in modele.lower() or "208" in modele.lower():
        prix_neuf = 18000

    if "3008" in modele.lower() or "tiguan" in modele.lower():
        prix_neuf = 32000

    if carburant == "Électrique":
        prix_neuf += 8000

    if carburant == "Hybride":
        prix_neuf += 4000

    # 🔥 DÉCOTE PRO
    valeur = prix_neuf * 0.8
    for i in range(max(age - 1, 0)):
        valeur *= 0.90

    # 🔥 KM
    km_moyen = age * 15000
    ecart_km = km - km_moyen

    if ecart_km > 0:
        valeur -= (ecart_km / 10000) * 500
    else:
        valeur += abs(ecart_km / 10000) * 300

    # 🔥 MOTORISATION
    motorisation_lower = motorisation.lower()

    if "90" in motorisation_lower or "100" in motorisation_lower:
        valeur *= 0.95
    elif "110" in motorisation_lower or "120" in motorisation_lower:
        valeur *= 1.00
    elif "130" in motorisation_lower or "150" in motorisation_lower:
        valeur *= 1.05
    elif "200" in motorisation_lower or "gt" in motorisation_lower:
        valeur *= 1.10

    # 🔥 PORTES
    if portes == 3:
        valeur *= 0.95
    elif portes == 5:
        valeur *= 1.02

    # 🔥 OPTIONS
    bonus = 0
    for opt in options:
        if opt in ["Toit panoramique", "Caméra 360"]:
            bonus += 300
        elif opt in ["GPS", "Caméra recul"]:
            bonus += 150
        else:
            bonus += 80

    valeur += bonus

    # 🔥 AJUSTEMENTS
    if boite == "Automatique":
        valeur *= 1.05

    if carburant == "Diesel":
        valeur *= 0.95

    if valeur < 3000:
        valeur = 3000

    prix_bas = int(valeur * 0.9)
    prix_haut = int(valeur * 1.1)
    prix_conseille = int((prix_bas + prix_haut) / 2)

    # ---------------- RESULTAT ----------------

    st.markdown("---")

    st.markdown(f"""
    <div style="
    padding:25px;
    border-radius:15px;
    background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
    text-align:center;
    ">

    <h2>📊 COTATION MARCHÉ</h2>
    <p>{marque} {modele} • {annee}</p>

    <h1>{prix_bas} € - {prix_haut} €</h1>

    <p>Prix marché particulier</p>

    </div>
    """, unsafe_allow_html=True)

    st.success("✔️ Estimation basée sur un modèle pro (décote réelle + marché)")
    st.info(f"💡 Prix conseillé de vente rapide : {prix_conseille} €")

    st.markdown(f"""
### 🔍 Résumé véhicule
- {marque} {modele}
- {annee} • {km} km
- {carburant} • {boite}
- {motorisation}
- {portes} portes
""")
