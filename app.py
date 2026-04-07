import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# ==============================
# CONFIG
# ==============================
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"

# ==============================
# LOAD USERS FROM GOOGLE SHEETS
# ==============================
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    # Nettoyage important
    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    return df

# ==============================
# CHECK LOGIN
# ==============================
def check_login(username, password):
    df = load_users()

    user = df[
        (df["username"] == username.strip()) &
        (df["password"] == password.strip())
    ]

    if not user.empty:
        expire_date = user.iloc[0]["expire"]

        if pd.isna(expire_date):
            return False, "Compte invalide"

        if datetime.now() > expire_date:
            return False, "Abonnement expiré"

        return True, "Connexion réussie"

    return False, "Identifiant incorrect"

# ==============================
# SEND TO MAKE (ESSAI GRATUIT)
# ==============================
def send_to_webhook(username, password):
    expire_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire_date,
        "trial": True
    }

    requests.post(WEBHOOK_URL, json=data)

# ==============================
# UI
# ==============================
st.title("🚗 Veliora Pro")

# ------------------------------
# ESSAI GRATUIT
# ------------------------------
st.subheader("🎁 Essai gratuit 7 jours")

new_user = st.text_input("Créer un identifiant")
new_pass = st.text_input("Créer un mot de passe", type="password")

if st.button("🚀 Démarrer l'essai gratuit"):
    if new_user and new_pass:
        send_to_webhook(new_user, new_pass)
        st.success("Compte créé ! Vérifie dans Google Sheets.")
    else:
        st.error("Remplis tous les champs")

# ------------------------------
# LOGIN
# ------------------------------
st.subheader("🔐 Déjà client ?")

login_user = st.text_input("Utilisateur")
login_pass = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    success, message = check_login(login_user, login_pass)

    if success:
        st.success("✅ Accès autorisé")
        st.write("Bienvenue sur Veliora Pro 🚀")
    else:
        st.error(message)

# ------------------------------
# TEST WEBHOOK
# ------------------------------
if st.button("TEST WEBHOOK"):
    send_to_webhook("test999", "123")
    st.success("Webhook envoyé")
