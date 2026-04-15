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

# 🔥 DATASET INTELLIGENT (prix récents marché)
BASE_PRICES = {
    "toyota chr": 30000,
    "toyota chr 2024": 32000,
    "toyota chr 2025": 33000,

    "peugeot 208": 18000,
    "peugeot 208 2023": 20000,

    "renault clio": 17000,
    "renault clio 2023": 19000,

    "dacia sandero": 14000,
    "bmw serie 1": 30000,
    "audi a3": 32000
}

def ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite):

    key_exact = f"{marque} {modele} {annee}".lower()
    key_base = f"{marque} {modele}".lower()

    base = BASE_PRICES.get(key_exact, BASE_PRICES.get(key_base, 22000))

    score = 1.0

    age = datetime.now().year - annee

    if age <= 1:
        score += 0.30
    elif age <= 3:
        score += 0.18
    elif age >= 7:
        score -= 0.20

    if km < 30000:
        score += 0.20
    elif km < 60000:
        score += 0.10
    elif km > 120000:
        score -= 0.25

    if carburant == "Hybride":
        score += 0.12
    elif carburant == "Électrique":
        score += 0.18
    elif carburant == "Diesel":
        score -= 0.05

    if boite == "Automatique":
        score += 0.05

    if finition:
        f = finition.lower()
        if "design" in f:
            score += 0.05
        elif "premium" in f:
            score += 0.08

    if motorisation:
        m = motorisation.lower()
        if "225" in m:
            score += 0.10
        elif "180" in m:
            score += 0.05

    # 🔥 BOOST VEHICULE RECENT + KM COHERENT
    if annee >= 2023 and km < 60000:
        score += 0.15

    return int(base * score)

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

mois = st.text_input("Mois 1ère immatriculation (ex: 03)", key=f"mois_{rid}")
annee = st.number_input("Année", 1990, datetime.now().year, 2019, key=f"annee_{rid}")

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key=f"carburant_{rid}")
boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key=f"boite_{rid}")

boite_tech = st.selectbox("Technologie boîte", ["", "BVA6","BVA7","BVA8","BVM5","BVM6"], key=f"boite_tech_{rid}")
traction = st.selectbox("Transmission", ["", "4x2","4x4","4WD","Traction","Propulsion"], key=f"traction_{rid}")

portes = st.selectbox("Nombre de portes", [2,3,4,5], key=f"portes_{rid}")
places = st.selectbox("Nombre de places", [2,3,5,7], key=f"places_{rid}")

options = st.multiselect("Options", [
    "Caméra recul","Bip avant","Bip arrière",
    "Sièges chauffants avant","Sièges chauffants arrière",
    "Hayon électrique","Attelage","Toit panoramique"
], key=f"options_{rid}")

st.markdown("[📄 Voir fiche technique Argus](https://www.largus.fr/fiche-technique.html)")

km = st.number_input("Kilométrage", 0, 400000, 90000, key=f"km_{rid}")
departement = st.text_input("Département (ex: 08)", key=f"dep_{rid}")

commission = st.number_input("Commission (€)", 0, 10000, 1000, key=f"comm_{rid}")
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0, key=f"comm_pct_{rid}")

if st.button("Calculer l'estimation"):

    prix_ai = ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite)

    prix_comparables = []

    if get_leboncoin_prices:
        try:
            query = f"{marque} {modele} {motorisation} {annee}"
            prix_comparables = get_leboncoin_prices(query)
            st.info(f"Leboncoin PRO : {len(prix_comparables)} annonces")
        except:
            pass

    if len(prix_comparables) >= 3:
        prix_comparables = clean_prices(prix_comparables)

        median_price = statistics.median(prix_comparables)
        mean_price = statistics.mean(prix_comparables)
        prix_scrap = int((median_price * 0.7) + (mean_price * 0.3))

        prix_marche = int((prix_ai * 0.85) + (prix_scrap * 0.15))
    else:
        prix_marche = prix_ai

    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.08)

    if commission_pct > 0:
        commission_calc = prix_marche * (commission_pct / 100)
    else:
        commission_calc = commission

    net_bas = int(prix_bas - commission_calc)
    net_marche = int(prix_marche - commission_calc)
    net_haut = int(prix_haut - commission_calc)

    st.success(f"💰 Prix marché GARAGE : {prix_marche} € | Net vendeur : {net_marche} €")
    st.info(f"📉 Prix bas GARAGE : {prix_bas} € | Net vendeur : {net_bas} €")
    st.info(f"📈 Prix haut GARAGE : {prix_haut} € | Net vendeur : {net_haut} €")

    buffer = io.StringIO()
    buffer.write(f"{marque} {modele} {sous_version} {finition} {motorisation}\n")
    buffer.write(f"Prix marché garage: {prix_marche} €\n")

    st.download_button("📥 Télécharger estimation", buffer.getvalue(), "estimation.txt")
