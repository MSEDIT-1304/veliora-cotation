import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ================= CONFIG =================

PAYMENT_LINK = "https://buy.stripe.com/test_7sYcN67QC1lbcmneek9fW00"
USERS_FILE = "users.json"

# ================= USERS =================

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# 🔥 ADMIN FIXE
users["admin"] = {
    "password": "admin123",
    "expire": "2099-01-01"
}
save_users(users)

# ================= SESSION =================

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "user_logged" not in st.session_state:
    st.session_state["user_logged"] = None

# ================= LOGIN =================

st.title("🔐 Accès Veliora Pro")

login_user = st.text_input("Utilisateur")
login_pwd = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if login_user in users and users[login_user]["password"] == login_pwd:
        st.session_state["auth"] = True
        st.session_state["user_logged"] = login_user
        st.success("Connexion réussie")
        st.rerun()
    else:
        st.error("Identifiants incorrects")

# ================= ESSAI =================

st.markdown("### 🚀 Essai gratuit 7 jours")

new_user = st.text_input("Créer un utilisateur")
new_pwd = st.text_input("Créer un mot de passe", type="password")

if st.button("Activer essai 7 jours"):
    if new_user and new_pwd:
        users[new_user] = {
            "password": new_pwd,
            "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        }
        save_users(users)
        st.success("Essai activé")
    else:
        st.warning("Remplir les champs")

# ================= STOP =================

if not st.session_state["auth"]:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

user = st.session_state["user_logged"]
st.success(f"Connecté : {user}")

user_data = users.get(user, {})
expire = user_data.get("expire")

if expire:
    expire_date = datetime.strptime(expire, "%Y-%m-%d")

    if datetime.now() > expire_date:
        st.error("⛔ Essai expiré")

        st.markdown(f"[💳 S'abonner 99€/an]({PAYMENT_LINK})")

        if st.button("J'ai payé"):
            users[user]["expire"] = (
                datetime.now() + timedelta(days=365)
            ).strftime("%Y-%m-%d")

            save_users(users)

            st.success("Abonnement activé")
            st.rerun()

        st.stop()

    else:
        st.success(f"✅ Accès actif jusqu'au {expire}")

# ================= LOGOUT =================

if st.button("Se déconnecter"):
    st.session_state["auth"] = False
    st.session_state["user_logged"] = None
    st.rerun()
