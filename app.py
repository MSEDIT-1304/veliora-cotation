import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os

SCRAPER_API_KEY = "sk_ad_6UkihaYMO3C3ukRwDVFVpjV2"

try:
    from leboncoin_scraper import get_leboncoin_prices
except:
    get_leboncoin_prices = None

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

def clean_prices(prices):
    if len(prices) < 5:
        return prices

    prices = sorted(prices)
    median = statistics.median(prices)

    filtered = [
        p for p in prices
        if (median * 0.6) <= p <= (median * 1.4)
    ]

    if len(filtered) < 3:
        return prices

    return filtered

# 🔥 IA AJUSTEMENT
def adjust_price_ai(prix, marque, annee, km, carburant):

    score = 1.0

    age = datetime.now().year - annee

    if age <= 1:
        score += 0.20
    elif age <= 3:
        score += 0.10
    elif age >= 7:
        score -= 0.15

    if km < 30000:
        score += 0.15
    elif km < 60000:
        score += 0.05
    elif km > 120000:
        score -= 0.20

    if carburant == "Hybride":
        score += 0.10
    elif carburant == "Électrique":
        score += 0.15
    elif carburant == "Diesel":
        score -= 0.05

    m = marque.lower()

    if "toyota" in m:
        score += 0.10
    elif "bmw" in m or "mercedes" in m or "audi" in m:
        score += 0.15
    elif "dacia" in m:
        score -= 0.10

    return int(prix * score)

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

rid = st.session_state.reset_id

marque = st.text_input("Marque", key=f"marque_{rid}")
modele = st.text_input("Modèle", key=f"modele_{rid}")
sous_version = st.text_input("Sous-version", key=f"sous_version_{rid}")
finition = st.text_input("Finition", key=f"finition_{rid}")
motorisation = st.text_input("Motorisation", key=f"motorisation_{rid}")

mois = st.text_input("Mois", key=f"mois_{rid}")
annee = st.number_input("Année", 1990, datetime.now().year, 2019, key=f"annee_{rid}")

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key=f"carburant_{rid}")
boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key=f"boite_{rid}")

km = st.number_input("Kilométrage", 0, 400000, 90000, key=f"km_{rid}")

if st.button("Calculer l'estimation"):

    prix_comparables = get_leboncoin_prices(" ".join([marque, modele, str(annee)]))

    prix_comparables = [p for p in prix_comparables if p > 2000]

    if annee >= 2023:
        prix_comparables = [p for p in prix_comparables if p > 25000]
    elif annee >= 2021:
        prix_comparables = [p for p in prix_comparables if p > 20000]

    if km < 30000:
        prix_comparables = [p for p in prix_comparables if p > 25000]

    prix_comparables = clean_prices(prix_comparables)

    prix_marche = int((statistics.median(prix_comparables) * 0.7) + (statistics.mean(prix_comparables) * 0.3))

    prix_marche = adjust_price_ai(prix_marche, marque, annee, km, carburant)

    st.success(f"💰 Prix marché estimé : {prix_marche} €")
