import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Veliora Pro", layout="centered")

# 🔥 CONFIG
PAYMENT_LINK = "https://ton-lien-stripe.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "change_ce_mdp"

FILE_PATH = "users.json"

# ---------------- LOAD USERS ----------------
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

# 🔥 ADMIN PROTECTION
users[ADMIN_USERNAME] = {"password": ADMIN_PASSWORD, "expire": None, "trial": False}
save_users(users)

# ---------------- CREATE TRIAL ----------------
def create_trial_user(username, password):
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

    expire_date = datetime.strptime(user["expire"], "%Y-%m-%d")
    today = datetime.now()

    if today > expire_date:
        return False, "expired"

    if expire_date - today <= timedelta(days=2):
        return True, "warning"

    return True, None

# ---------------- AUTH ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 Accès Veliora Pro")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

    # -------- LOGIN --------
    with tab1:
        username = st.text_input("Utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):

            users = load_users()

            # ADMIN
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.auth = True
                st.session_state.user = username
                st.rerun()

            # USER
            if username in users and users[username]["password"] == password:

                valid, status = check_access(users[username])

                if not valid:
                    st.error("⛔ Accès expiré")

                    if users[username].get("trial", False):
                        st.warning("🎯 Votre essai gratuit est terminé")
                    else:
                        st.warning("💳 Abonnement expiré")

                    st.markdown(f"[👉 S'abonner maintenant]({PAYMENT_LINK})")
                    st.stop()

                if status == "warning":
                    st.warning("⚠️ Votre accès expire bientôt")

                st.session_state.auth = True
                st.session_state.user = username
                st.rerun()

            else:
                st.error("❌ Identifiants incorrects")

    # -------- FREE TRIAL --------
    with tab2:
        st.markdown("### 🎁 Essai gratuit 7 jours")

        new_user = st.text_input("Choisir un identifiant")
        new_pass = st.text_input("Choisir un mot de passe", type="password")

        if st.button("Créer mon accès gratuit"):

            users = load_users()

            if new_user in users:
                st.error("Utilisateur déjà existant")
            else:
                create_trial_user(new_user, new_pass)
                st.success("✅ Compte créé ! Connectez-vous")

    st.stop()

# ---------------- APP ----------------

st.write(f"👤 Connecté : {st.session_state.user}")

st.title("🚗 VELIORA COTATION PRO")

st.info("💡 Plus tu remplis d’informations, plus l’estimation sera précise.")

# ---------------- FORM ----------------
marques_list = [
    "Audi", "BMW", "Citroën", "Dacia", "Fiat", "Ford", "Honda", "Hyundai",
    "Kia", "Mazda", "Mercedes", "Mini", "Nissan", "Opel", "Peugeot",
    "Renault", "Seat", "Skoda", "Toyota", "Volkswagen", "Volvo",
    "Alfa Romeo", "Jeep", "Land Rover", "Porsche", "Tesla"
]

marque = st.selectbox("Marque", marques_list)
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

if st.button("Calculer l'estimation"):

    age = datetime.now().year - int(annee)
    base = 15000

    if marque.lower() in ["mercedes", "bmw", "audi"]:
        base += 8000

    if "tiguan" in modele.lower():
        base = 26000

    if "cla" in modele.lower():
        base = 28000

    if "amg" in finition.lower():
        base += 4000

    if boite == "Automatique":
        base += 1500

    if carburant == "Diesel":
        base += 800

    if portes <= 3:
        base += 500
    if portes >= 5:
        base += 300

    base -= age * 1200

    if km > 80000:
        base -= 1000

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2500)

    st.markdown(f"""
### 📊 Résultat

🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} €  
🔺 Haut : {prix_haut} €
""")
