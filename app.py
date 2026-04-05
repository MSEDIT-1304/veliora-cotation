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

# ADMIN
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
        "trial": False,
        "verified": True
    }

# 🔥 USER TEST AUTO
users["test123"] = {
    "password": "1234",
    "expire": "2026-12-31",
    "trial": True,
    "verified": True,
    "siret": "12345678901234",
    "company": "Test Garage"
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

        users = load_users()

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
st.success("✔️ Accès professionnel activé")

st.markdown("""
✔️ Profil entreprise enregistré  
✔️ Données conformes  
✔️ Accès sécurisé Veliora Pro
""")

st.divider()

# 🔥 BOUTON TEST STRIPE
st.markdown(f"[💳 TESTER PAIEMENT STRIPE]({PAYMENT_LINK})")

# ---------------- TEST RESULT ----------------
st.info("👉 Après paiement, vérifie si ton webhook met à jour ton utilisateur.")
