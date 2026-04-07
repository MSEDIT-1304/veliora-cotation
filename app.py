import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

# 🔐 ADMIN
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

# =========================
# PAGE ACCUEIL
# =========================
if not st.session_state.auth:

    st.title("🚗 Veliora Pro")

    # ---------- ESSAI GRATUIT ----------
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

    # ---------- LOGIN ----------
    st.subheader("🔐 Déjà client ?")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        # 🔥 ADMIN LOGIN
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.auth = True
            st.session_state.admin = True
            st.rerun()

        # 🔥 USER LOGIN
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

    st.stop()

# =========================
# ADMIN PANEL
# =========================
if st.session_state.get("admin", False):

    st.title("🛠️ ADMIN PANEL")

    df = load_users()

    st.write("### 👥 Utilisateurs")
    st.dataframe(df)

    st.stop()

# =========================
# UTILISATEUR CONNECTÉ
# =========================

st.write(f"👤 Connecté : {st.session_state.user}")

user_data = st.session_state.data

expire_date = user_data["expire"]
jours_restants = (expire_date - datetime.now()).days

# ---------- TRIAL ----------
if user_data["trial"]:
    st.info(f"🎁 Essai actif – {jours_restants} jour(s) restant(s)")

# ---------- SI EXPIRÉ ----------
if datetime.now() > expire_date:
    st.error("⛔ Abonnement expiré")
    st.link_button("💳 S’abonner (99€/an)", STRIPE_LINK)
    st.stop()

st.divider()

# =========================
# APP ORIGINALE (INTOUCHÉE)
# =========================

st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois de mise en circulation", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
    techno = st.selectbox("Technologie de boîte", ["-", "DSG", "EDC", "CVT", "BVA", "BVA6", "BVA7", "BVA8"])
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4", "4WD"])

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants avant","Sièges chauffants avant + arrière",
        "Sièges électriques","Régulateur de vitesse","Régulateur adaptatif",
        "Radar de recul","Bips avant","Bips arrière","Caméra de recul","Caméra 360",
        "GPS / Navigation","Bluetooth","Connexion Apple CarPlay","Connexion Android Auto",
        "Système audio premium","Rétroviseurs chauffants","Rétroviseurs électriques rabattables",
        "Jantes alliage","Toit ouvrant","Toit panoramique","Feux LED","Attelage","Détecteur angle mort"
    ]
)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

if st.button("Calculer l'estimation"):

    base = 17000
    age = datetime.now().year - annee

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 3000

    if boite == "Automatique":
        base += 1200

    if techno in ["DSG","EDC"]:
        base += 400
    if techno in ["BVA6","BVA7","BVA8"]:
        base += 500

    if carburant == "Diesel":
        base += 300
    elif carburant == "Hybride":
        base += 2500
    elif carburant == "Électrique":
        base += 5000

    if traction in ["4x4","4WD"]:
        base += 800

    if etat == "Excellent état":
        base += 1200
    else:
        base -= 500

    base -= age * 900

    if km > 80000:
        base -= 1200
    if km > 120000:
        base -= 2000

    base += len(options) * 100
    base *= 0.90

    prix = int(base)
    net = prix - commission

    st.markdown(f"### 💰 Prix estimé : {prix} €")
    st.markdown(f"### 🧾 Net vendeur : {net} €")
