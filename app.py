import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os

# ✅ AJOUT PLAYWRIGHT
from leboncoin_scraper import get_leboncoin_prices

# 🔥 IA AJOUT SÉCURISÉ

try:
    import joblib
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------

WEBHOOK_URL = "https://hook.eu1.make.com/dhb2yglq1eta549enf7zaw83iltcdkrw"
MAKE_PRICE_WEBHOOK = "https://hook.eu1.make.com/dhb2yglq1eta549enf7zaw83iltcdkrw"

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

    return df

# ---------------- LOGIN ----------------

def check_login(username, password):
    df = load_users()

    user = df[
        (df["username"] == username.strip()) &
        (df["password"] == password.strip())
    ]

    if not user.empty:
        expire = user.iloc[0]["expire"]

        if datetime.now() > expire:
            return "expired"

        return "ok"

    return "error"

# ---------------- WEBHOOK ----------------

def send_to_webhook(username, password, societe, siret):
    expire = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "societe": societe,
        "siret": siret,
        "expire": expire,
        "trial": True
    }

    try:
        requests.post(WEBHOOK_URL, json=data, timeout=10)
    except:
        pass

# ---------------- SESSION ----------------

if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

if st.session_state.admin_logged:
    st.session_state.logged = True

# ================= LOGIN =================

if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")

    st.warning("⚠️ Accès réservé aux professionnels de l’automobile")

    st.info("Après 3 jours d'essai, accès complet : 99€/an.")
    st.markdown(f"[💳 S'abonner maintenant]({STRIPE_LINK})")

    type_client = st.selectbox(
        "Type d'utilisateur",
        ["Professionnel auto", "Particulier"]
    )

    new_user = st.text_input("Créer un identifiant")
    new_pass = st.text_input("Créer un mot de passe", type="password")

    societe = st.text_input("Nom de la société")
    siret = st.text_input("Numéro SIRET")

    if st.button("Créer compte"):
        if type_client != "Professionnel auto":
            st.error("Accès réservé aux professionnels")
        elif not societe or not siret:
            st.error("SIRET obligatoire pour créer un compte")
        elif new_user and new_pass:
            send_to_webhook(new_user, new_pass, societe, siret)
            st.success("Compte professionnel créé")
        else:
            st.error("Remplir tous les champs")

    st.markdown("---")

    st.subheader("🔐 Connexion")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user.strip() == ADMIN_USER and pwd.strip() == ADMIN_PASS:
            st.session_state.logged = True
            st.session_state.admin_logged = True
            st.rerun()

        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.rerun()

        elif result == "expired":
            st.error("⛔ Abonnement expiré")
            st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

    st.stop()

# ================= APP =================

st.title("🚗 VELIORA COTATION PRO")

if st.button("🔄 Nouvelle cotation (reset)"):
    st.session_state.reset_id += 1
    st.rerun()

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
    st.rerun()

rid = st.session_state.reset_id

# ================= INPUTS =================

marque = st.text_input("Marque", key=f"marque_{rid}")
modele = st.text_input("Modèle", key=f"modele_{rid}")

col1, col2 = st.columns(2)

with col1:
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

km = st.number_input("Kilométrage", 0, 400000, 90000)
departement = st.text_input("Département (ex: 08)")

commission = st.number_input("Commission (€)", 0, 10000, 1000)
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    prix_comparables = []

    try:
        query = f"{marque} {modele} {annee} {km} km {carburant} {boite} {departement}"

        response = requests.post(
            MAKE_PRICE_WEBHOOK,
            json={"query": query},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if "prices" in data:
                prix_comparables = [int(p) for p in data["prices"] if p > 1000]

    except:
        pass

    if len(prix_comparables) < 3:
        st.error("❌ Données insuffisantes")
        st.stop()

    prix_marche = int(statistics.median(prix_comparables))

    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.08)

    if commission_pct > 0:
        commission_calc = prix_marche * (commission_pct / 100)
    else:
        commission_calc = commission

    net_marche = int(prix_marche - commission_calc)

    st.success(f"💰 Prix estimé : {prix_marche} €")
    st.info(f"Net vendeur : {net_marche} €")

    buffer = io.StringIO()
    buffer.write(f"{marque} {modele}\n")
    buffer.write(f"Prix marché: {prix_marche} €\n")

    st.download_button("📥 Télécharger estimation", buffer.getvalue(), "estimation.txt")
