import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "VelioraAdmin123!"

# ---------------- LOAD USERS ----------------
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    return df

# ---------------- LOGIN ----------------
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
            return False, "expired"

        return True, user.iloc[0]

    return False, "Identifiant incorrect"

# ---------------- WEBHOOK ----------------
def send_to_webhook(username, password):
    expire_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire_date,
        "trial": True
    }

    requests.post(WEBHOOK_URL, json=data)

# ---------------- SESSION ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# ================= MENU =================
menu = st.sidebar.radio(
    "Navigation",
    ["🔐 Connexion", "🏠 Application", "🛠️ Admin", "🚪 Déconnexion"]
)

# ================= LOGOUT =================
if menu == "🚪 Déconnexion":
    st.session_state.auth = False
    st.session_state.admin = False
    st.rerun()

# ================= LOGIN =================
if menu == "🔐 Connexion":

    st.title("🚗 Veliora Pro")

    st.subheader("🎁 Essai gratuit 7 jours")

    new_user = st.text_input("Créer un identifiant", key="new_user")
    new_pwd = st.text_input("Créer un mot de passe", type="password", key="new_pwd")

    if st.button("🚀 Démarrer l'essai gratuit"):
        if new_user and new_pwd:
            send_to_webhook(new_user, new_pwd)
            st.success("Compte créé !")
        else:
            st.error("Remplir les champs")

    st.markdown("---")

    st.subheader("🔐 Connexion")

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):

        if not user or not pwd:
            st.error("Remplis les champs")
            st.stop()

        # ADMIN
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.auth = True
            st.session_state.admin = True
            st.rerun()

        # USER
        ok, data = check_login(user, pwd)

        if ok:
            st.session_state.auth = True
            st.session_state.user = user
            st.session_state.data = data
            st.session_state.admin = False
            st.rerun()

        else:
            if data == "expired":
                st.error("⛔ Abonnement expiré")
                st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")
            else:
                st.error(data)

# ================= ADMIN =================
elif menu == "🛠️ Admin":

    if not st.session_state.admin:
        st.error("⛔ Accès refusé")
        st.stop()

    st.title("🛠️ ADMIN PANEL")
    st.dataframe(load_users())

# ================= APP =================
elif menu == "🏠 Application":

    if not st.session_state.auth:
        st.warning("Veuillez vous connecter")
        st.stop()

    st.write(f"👤 Connecté : {st.session_state.user}")

    st.title("🚗 VELIORA COTATION PRO")

    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")

    if st.button("Calculer"):
        st.success("Estimation OK 🚀")
