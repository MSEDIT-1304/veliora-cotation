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
ADMIN_PASS = "TonMotDePasseFort123!"

# ---------------- LOAD USERS ----------------
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    # 🔥 sécurité colonne active
    if "active" not in df.columns:
        df["active"] = True

    if "trial" not in df.columns:
        df["trial"] = True

    return df

# ---------------- LOGIN LOGIC ----------------
def check_login(username, password):
    df = load_users()

    user = df[
        (df["username"] == username.strip()) &
        (df["password"] == password.strip())
    ]

    if user.empty:
        return "error"

    user_data = user.iloc[0]

    expire = user_data["expire"]
    trial = str(user_data["trial"]).upper() == "TRUE"
    active = str(user_data["active"]).upper() == "TRUE"

    if not active:
        return "inactive"

    if datetime.now() > expire:
        return "expired"

    return "ok"

# ---------------- WEBHOOK ----------------
def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire,
        "trial": True,
        "active": True
    }

    requests.post(WEBHOOK_URL, json=data)

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# ================= LOGIN =================
if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 7 jours")

    new_user = st.text_input("Créer un identifiant")
    new_pass = st.text_input("Créer un mot de passe", type="password")

    if st.button("Créer compte"):
        if new_user and new_pass:
            send_to_webhook(new_user, new_pass)
            st.success("Compte créé")
        else:
            st.error("Remplir tous les champs")

    st.markdown("---")

    st.subheader("🔐 Connexion")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged = True
            st.session_state.admin = True
            st.rerun()

        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.session_state.admin = False
            st.rerun()

        elif result == "expired":
            st.error("⛔ Votre accès a expiré")
            st.markdown(f"### 👉 [💳 S'abonner]({STRIPE_LINK})")
            st.stop()

        elif result == "inactive":
            st.error("⛔ Paiement échoué ou abonnement suspendu")
            st.markdown(f"### 👉 [💳 Réactiver mon abonnement]({STRIPE_LINK})")
            st.stop()

        else:
            st.error("Identifiant incorrect")

    st.stop()

# ================= ADMIN DASHBOARD =================
if st.session_state.admin:

    st.title("📊 Dashboard Admin")

    df = load_users()

    total_users = len(df)
    actifs = df[df["active"] == True].shape[0]
    expires = df[df["expire"] < datetime.now()].shape[0]

    st.metric("Utilisateurs", total_users)
    st.metric("Actifs", actifs)
    st.metric("Expirés", expires)

    st.dataframe(df)

    if st.button("Se déconnecter"):
        st.session_state.logged = False
        st.session_state.admin = False
        st.rerun()

    st.stop()

# ================= APP =================

st.title("🚗 VELIORA COTATION PRO")

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.rerun()

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
    techno = st.selectbox("Technologie", ["-", "DSG", "EDC", "CVT", "BVA"])
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4"])

etat = st.selectbox("État", ["Bon état", "Excellent état"])
places = st.selectbox("Places", [2,3,4,5,6,7])
portes = st.selectbox("Portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

departement = st.selectbox("Département", ["75","13","69","59","33","06","44","31","34","Autre"])

options = st.multiselect("Options", ["GPS","Caméra","Cuir","Toit ouvrant","LED","CarPlay"])

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ================= BASE MODELES =================
prix_reference = {
    "captur": 9000,
    "clio": 8000,
    "megane": 8500,
    "3008": 12000,
    "208": 9000,
    "308": 9500
}

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    base = 8500
    modele_clean = modele.lower()

    for key in prix_reference:
        if key in modele_clean:
            base = prix_reference[key]

    age = datetime.now().year - annee
    base -= age * 400

    if km > 80000:
        base -= 700
    if km > 120000:
        base -= 1200

    base += len(options) * 100

    if boite == "Automatique":
        base += 800

    coef_dep = 1.0
    if departement == "75":
        coef_dep = 1.08

    base = int(base * coef_dep)

    annonces = [base*1.05, base*0.98, base*1.02, base, base*0.95]
    moyenne = sum(annonces)/len(annonces)

    prix_marche = int(moyenne * 0.95)

    prix_bas = int(prix_marche * 0.93)
    prix_haut = int(prix_marche * 1.05)

    net_bas = prix_bas - commission
    net_marche = prix_marche - commission
    net_haut = prix_haut - commission

    st.markdown(f"### 🔻 Vente rapide : {prix_bas} € → Net vendeur : {net_bas} €")
    st.markdown(f"### 📊 Prix marché BIWIZ : {prix_marche} € → Net vendeur : {net_marche} €")
    st.markdown(f"### 🔺 Prix haut : {prix_haut} € → Net vendeur : {net_haut} €")
