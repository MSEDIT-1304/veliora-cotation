import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/test_7sYcN67QC1lbcmneek9fW00"
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
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
        "trial": False,
        "verified": True,
        "siret": "ADMIN",
        "company": "ADMIN"
    }
    save_users(users)

# ---------------- TRIAL ----------------
def create_trial(username, password, siret, company):
    users = load_users()
    users[username] = {
        "password": password,
        "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "trial": True,
        "verified": False,
        "siret": siret,
        "company": company
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

    # LOGIN
    with tab1:
        user = st.text_input("Utilisateur", key="login_user")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter"):

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

                if not users[user].get("verified", False):
                    st.error("⛔ Compte non validé")
                    st.info("📩 Validation après réception et contrôle du KBIS")
                    st.stop()

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("Identifiants incorrects")

    # TRIAL
    with tab2:
        new_user = st.text_input("Créer un utilisateur", key="trial_user")
        new_pwd = st.text_input("Mot de passe", type="password", key="trial_pwd")
        company = st.text_input("Nom de l'entreprise")
        siret = st.text_input("Numéro SIRET")

        if st.button("Créer essai"):
            if new_user in users:
                st.error("Utilisateur déjà existant")
            elif not siret or len(siret) != 14 or not siret.isdigit():
                st.error("SIRET invalide (14 chiffres)")
            elif not company:
                st.error("Nom d'entreprise obligatoire")
            else:
                create_trial(new_user, new_pwd, siret.strip(), company)
                st.success("Compte créé, connectez-vous")

    st.stop()

# ---------------- APP ----------------

users = load_users()
user_data = users[st.session_state.user]

st.write(f"👤 Connecté : {st.session_state.user}")

# UX PRO
st.markdown("## 🔐 Accès professionnel")

if user_data.get("verified"):
    st.success("✔️ Accès professionnel validé")
    st.markdown("""
✔️ Profil entreprise enregistré  
✔️ Vérification validée  
✔️ Accès sécurisé Veliora Pro
""")
else:
    st.warning("⏳ Vérification du profil en cours")
    st.markdown("""
✔️ Profil entreprise enregistré  
✔️ Vérification en cours  
✔️ Accès sécurisé Veliora Pro  
""")

st.divider()

# 💳 PAIEMENT
st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

# 🔥 ACTIVATION SIMPLE
if st.button("✅ J’ai payé → Activer mon abonnement"):
    users = load_users()
    users[st.session_state.user]["expire"] = (
        datetime.now() + timedelta(days=30)
    ).strftime("%Y-%m-%d")
    save_users(users)
    st.success("🎉 Abonnement activé pour 30 jours")

st.divider()

# ---------------- APP METIER ----------------

st.title("🚗 VELIORA COTATION PRO")
st.info("💡 Plus tu remplis d’informations, plus l’estimation sera précise.")

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

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants","Sièges électriques",
        "Régulateur de vitesse","Régulateur adaptatif","Radar de recul",
        "Caméra de recul","Caméra 360","GPS / Navigation",
        "Bluetooth","CarPlay / Android Auto","Système audio premium",
        "Jantes alliage","Toit ouvrant","Toit panoramique",
        "Feux LED","Attelage","Détecteur angle mort"
    ]
)

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

    if "cla" in modele.lower():
        base = 28000

    if "amg" in finition.lower():
        base += 4000

    if boite == "Automatique":
        base += 1500

    if carburant == "Diesel":
        base += 800

    if portes <= 3:
        base += 400
    elif portes == 5:
        base += 200

    base -= age * 1200

    if km > 80000:
        base -= 1000

    bonus = 0
    for opt in options:
        if opt in ["Sellerie cuir","Toit panoramique","Caméra 360","Système audio premium"]:
            bonus += 500
        elif opt in ["GPS / Navigation","Caméra de recul","Sièges chauffants"]:
            bonus += 300
        else:
            bonus += 150

    base += bonus

    prix_bas = int(base - 1500)
    prix_moyen = int(base)
    prix_haut = int(base + 2500)

    st.markdown(f"""
## 📊 COTATION RÉELLE

🔻 Prix bas : {prix_bas} €  
⚖️ Prix marché : {prix_moyen} €  
🔺 Prix haut : {prix_haut} €
""")
