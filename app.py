import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os

SCRAPER_API_KEY = "sk_ad_6UkihaYMO3C3ukRwDVFVpjV2"

# SAFE
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

def clean_prices(prices):
    if len(prices) < 5:
        return prices
    prices = sorted(prices)
    q1 = prices[len(prices)//4]
    q3 = prices[(len(prices)*3)//4]
    iqr = q3 - q1
    min_val = q1 - 1.5 * iqr
    max_val = q3 + 1.5 * iqr
    cleaned = [p for p in prices if min_val <= p <= max_val]
    return cleaned if len(cleaned) >= 3 else prices

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
            st.error("SIRET obligatoire")
        elif new_user and new_pass:
            send_to_webhook(new_user, new_pass, societe, siret)
            st.success("Compte créé")
        else:
            st.error("Champs manquants")

    st.markdown("---")

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
        else:
            st.error("Identifiant incorrect")

    st.stop()

# ================= APP =================
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

portes = st.selectbox("Nombre de portes", [2,3,5])
places = st.selectbox("Nombre de places", [2,5,7])

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

departement = st.text_input("Département")

commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 15.0)

st.markdown("[📄 Voir fiche technique Argus](https://www.largus.fr/fiche-technique.html)")

# ================= ESTIMATION =================
if st.button("Calculer l'estimation"):

    modele_txt = f"{marque} {modele} {sous_version} {motorisation}".lower()

    base = 18000

    if "toyota" in modele_txt: base = 26000
    if "c-hr" in modele_txt: base = 30000
    if "bmw" in modele_txt: base = 35000
    if "audi" in modele_txt: base = 33000
    if "mercedes" in modele_txt: base = 36000
    if "peugeot" in modele_txt: base = 20000
    if "renault" in modele_txt: base = 19000
    if "dacia" in modele_txt: base = 16000

    base += (annee - 2020) * 800
    base -= km * 0.03

    if carburant == "Diesel": base *= 0.95
    if boite == "Automatique": base *= 1.05
    if places == 7: base *= 1.08
    if portes == 3: base *= 0.95
    if departement.startswith("75"): base *= 1.1

    prix_bas = base * 0.9
    prix_haut = base * 1.1

    commission = base * (commission_pct / 100)

    net_moyen = base - commission
    net_bas = prix_bas - commission
    net_haut = prix_haut - commission

    df = pd.DataFrame({
        "Type": ["Bas", "Marché", "Haut"],
        "Prix Garage (€)": [int(prix_bas), int(base), int(prix_haut)],
        "Net Vendeur (€)": [int(net_bas), int(net_moyen), int(net_haut)]
    })

    st.dataframe(df)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    st.download_button("📥 Télécharger estimation", buffer.getvalue(), "estimation.csv")
