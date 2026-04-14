import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os

SCRAPER_API_KEY = "sk_ad_6UkihaYMO3C3ukRwDVFVpjV2"

# ✅ SAFE (évite crash)
def get_leboncoin_prices(query, km=None, carburant=None, boite=None):
    return []

try:
    import joblib
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/dhb2yglq1eta549enf7zaw83iltcdkrw"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"

PRICE_HT = 99
TVA = 0.20
PRICE_TTC = 118.80

STRIPE_LINK = "https://buy.stripe.com/00w8wQ9YK8NDcmn9Y49fW05"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")
    return df

def check_login(username, password):
    df = load_users()
    user = df[(df["username"] == username.strip()) & (df["password"] == password.strip())]

    if not user.empty:
        expire = user.iloc[0]["expire"]
        if datetime.now() > expire:
            return "expired"
        return "ok"
    return "error"

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

if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

if st.session_state.admin_logged:
    st.session_state.logged = True

if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")

    st.warning("⚠️ Accès réservé aux professionnels de l’automobile")
    st.info(f"Après 3 jours d'essai : {PRICE_HT}€ HT ({PRICE_TTC}€ TTC) / an")

    st.markdown(f"[💳 S'abonner maintenant ({PRICE_TTC}€ TTC)]({STRIPE_LINK})")

    type_client = st.selectbox("Type d'utilisateur", ["Professionnel auto", "Particulier"])

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
            st.markdown(f"[💳 S'abonner ({PRICE_TTC}€ TTC)]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

    st.stop()

st.title("🚗 VELIORA COTATION PRO")

if st.button("🔄 Nouvelle cotation (reset)"):
    st.session_state.reset_id += 1
    st.rerun()

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
    st.rerun()

rid = st.session_state.reset_id

marque = st.text_input("Marque", key=f"marque_{rid}")
modele = st.text_input("Modèle", key=f"modele_{rid}")
sous_version = st.text_input("Sous-version", key=f"sous_version_{rid}")
finition = st.text_input("Finition", key=f"finition_{rid}")
motorisation = st.text_input("Motorisation", key=f"motorisation_{rid}")

portes = st.selectbox("Nombre de portes", [2, 3, 5], key=f"portes_{rid}")
places = st.selectbox("Nombre de places", [2, 5, 7], key=f"places_{rid}")

mois = st.text_input("Mois 1ère immatriculation", key=f"mois_{rid}")
annee = st.number_input("Année", 1990, datetime.now().year, 2019, key=f"annee_{rid}")

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key=f"carburant_{rid}")
boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key=f"boite_{rid}")

km = st.number_input("Kilométrage", 0, 400000, 90000, key=f"km_{rid}")
departement = st.text_input("Département", key=f"dep_{rid}")

commission = st.number_input("Commission (€)", 0, 10000, 1000, key=f"comm_{rid}")

if st.button("Calculer l'estimation"):

    prix_base = 15000

    prix_base += (annee - 2015) * 500
    prix_base -= km * 0.02

    if carburant == "Diesel":
        prix_base *= 0.95

    if boite == "Automatique":
        prix_base *= 1.05

    if places == 7:
        prix_base *= 1.08

    if portes == 3:
        prix_base *= 0.95

    if departement.startswith("75") or departement.startswith("92"):
        prix_base *= 1.1

    prix_bas = prix_base * 0.9
    prix_haut = prix_base * 1.1

    marge = 0.15

    net_bas = prix_bas / (1 + marge)
    net_moyen = prix_base / (1 + marge)
    net_haut = prix_haut / (1 + marge)

    st.success(f"""
💰 PRIX MARCHÉ GARAGE

➡️ Prix marché : {int(prix_base)} €
➡️ Prix bas : {int(prix_bas)} €
➡️ Prix haut : {int(prix_haut)} €

💵 NET VENDEUR

➡️ Net vendeur marché : {int(net_moyen)} €
➡️ Net vendeur bas : {int(net_bas)} €
➡️ Net vendeur haut : {int(net_haut)} €
""")
