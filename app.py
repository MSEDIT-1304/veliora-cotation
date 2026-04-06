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

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

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

user_data = users[st.session_state.user]

# 🔄 RESET AUTOMATIQUE SI EXPIRÉ
if user_data.get("expire"):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")
    if expire_date < datetime.now():
        user_data["expire"] = None
        user_data["trial"] = False
        save_users(users)

# 🎁 7 JOURS GRATUITS (TOUJOURS DISPONIBLE SI PAS D’ACCÈS)
if user_data.get("expire") is None:
    if st.button("🎁 Activer 7 jours gratuits"):
        user_data["expire"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        user_data["trial"] = True
        save_users(users)
        st.success("🎉 Essai gratuit activé")
        st.rerun()

# 🔒 BLOQUAGE SI EXPIRE (cas sécurité)
if user_data.get("expire"):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")

    if expire_date < datetime.now():
        st.error("⛔ Accès expiré")
        st.stop()

# 💡 STATUT
if user_data.get("expire"):
    if user_data.get("trial"):
        st.info("🎁 Essai gratuit actif")
    else:
        st.success("💎 Abonnement actif")
else:
    st.warning("⚠️ Aucun accès actif")

# 💳 PAIEMENT
st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):
    user_data["expire"] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    user_data["trial"] = False
    save_users(users)
    st.success("🎉 Abonnement activé")
    st.rerun()

st.divider()

# ---------------- FORMULAIRE ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

etat = st.selectbox("État", ["Bon état", "Excellent état"])
km = st.number_input("Kilométrage", 0, 400000, 90000)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Calculer l'estimation"):

    base = 17000

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 3000

    if boite == "Automatique":
        base += 1200

    if carburant == "Hybride":
        base += 2500
    elif carburant == "Électrique":
        base += 5000

    if etat == "Excellent état":
        base += 1200
    else:
        base -= 500

    base -= (datetime.now().year - annee) * 900

    if km > 80000:
        base -= 1200

    base *= 0.90

    annonces = [
        (random.randint(20000, 150000), base + random.randint(-2000, 2000))
        for _ in range(5)
    ]

    marche = int(sum([p for _, p in annonces]) / len(annonces))
    prix_moyen = int(base * 0.6 + marche * 0.4)

    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    net = prix_moyen - commission

    st.markdown(f"""
### 💰 Prix
Bas : {prix_bas} €  
Moyen : {prix_moyen} €  
Haut : {prix_haut} €

### 🧾 Net vendeur
{net} €
""")
