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

    new_user = st.text_input("Créer un identifiant")
    new_pwd = st.text_input("Créer un mot de passe", type="password")

    if st.button("🚀 Démarrer l'essai gratuit"):
        if new_user and new_pwd:
            send_to_webhook(new_user, new_pwd)
            st.success("Compte créé !")
        else:
            st.error("Remplir les champs")

    st.markdown("---")

    st.subheader("🔐 Connexion")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.auth = True
            st.session_state.admin = True
            st.rerun()

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

    user_data = st.session_state.data
    expire_date = user_data["expire"]

    if datetime.now() > expire_date:
        st.error("⛔ Abonnement expiré")
        st.link_button("💳 S’abonner (99€/an)", STRIPE_LINK)
        st.stop()

    # ===== APP COMPLETE =====

    st.title("🚗 VELIORA COTATION PRO")

    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")
    sous_version = st.text_input("Sous-version")
    finition = st.text_input("Finition")
    motorisation = st.text_input("Motorisation")

    col1, col2 = st.columns(2)

    with col1:
        mois = st.selectbox("Mois", list(range(1,13)))
        annee = st.number_input("Année", 1990, datetime.now().year, 2019)
        carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

    with col2:
        boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
        techno = st.selectbox("Technologie", ["-", "DSG", "EDC", "CVT", "BVA", "BVA6", "BVA7", "BVA8"])
        traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4", "4WD"])

    etat = st.selectbox("État", ["Bon état", "Excellent état"])
    portes = st.selectbox("Portes", [1,2,3,4,5])
    km = st.number_input("Kilométrage", 0, 400000, 90000)

    options = st.multiselect("Options", [
        "GPS","Cuir","Toit ouvrant","Caméra","LED","CarPlay","Android Auto"
    ])

    commission = st.number_input("Commission", 0, 10000, 1000)

    if st.button("Calculer"):

        base = 17000
        age = datetime.now().year - annee

        if marque.lower() in ["bmw","audi","mercedes"]:
            base += 3000

        if boite == "Automatique":
            base += 1200

        if carburant == "Électrique":
            base += 5000

        base -= age * 900
        base -= km / 100

        base += len(options) * 100
        base *= 0.9

        prix = int(base)
        net = prix - commission

        st.success(f"Prix : {prix} €")
        st.success(f"Net : {net} €")
