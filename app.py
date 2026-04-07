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

# 🔥 ADMIN FORCÉ
users["admin"] = {
    "password": "admin123",
    "expire": "2099-01-01"
}
save_users(users)

# ================= SESSION =================

if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN =================

st.title("🔐 Accès Veliora Pro")

user = st.text_input("Utilisateur", key="user")
pwd = st.text_input("Mot de passe", type="password", key="pwd")

if st.button("Se connecter", key="login_btn"):
    if user in users and users[user]["password"] == pwd:
        st.session_state.auth = True
        st.session_state.user = user
        st.success("Connexion réussie")
        st.rerun()
    else:
        st.error("Identifiants incorrects")

# ================= STOP =================

if not st.session_state.auth:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

st.write(f"Connecté : {st.session_state.user}")

user_data = users.get(st.session_state.user, {})
expire = user_data.get("expire")

if expire:
    expire_date = datetime.strptime(expire, "%Y-%m-%d")

    if datetime.now() > expire_date:
        st.error("⛔ Accès expiré")
        st.markdown(f"[💳 S'abonner]({PAYMENT_LINK})")
        st.stop()
    else:
        st.success(f"Accès actif jusqu'au {expire}")

# ================= LOGOUT =================

if st.button("Se déconnecter"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()
