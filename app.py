import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Veliora Pro", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

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

def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire,
        "trial": True
    }

    requests.post(WEBHOOK_URL, json=data)

if "logged" not in st.session_state:
    st.session_state.logged = False

# LOGIN
if not st.session_state.logged:

    st.title("🚗 Veliora Pro")

    new_user = st.text_input("Créer un identifiant")
    new_pass = st.text_input("Créer un mot de passe", type="password")

    if st.button("Créer compte"):
        if new_user and new_pass:
            send_to_webhook(new_user, new_pass)
            st.success("Compte créé")

    st.markdown("---")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged = True
            st.rerun()

        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.rerun()

        elif result == "expired":
            st.error("Abonnement expiré")
        else:
            st.error("Identifiant incorrect")

    st.stop()

# APP
st.title("🚗 COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

departement = st.selectbox("Département", ["75","13","69","59","33","06","44","31","34","Autre"])

commission = st.number_input("Commission (€)", 0, 10000, 1000)

prix_reference = {
    "captur": 9000,
    "clio": 8000,
    "megane": 8500,
    "3008": 12000,
    "208": 9000,
    "308": 9500
}

if st.button("Calculer l'estimation"):

    modele_clean = modele.lower()
    base = 8500

    for key in prix_reference:
        if key in modele_clean:
            base = prix_reference[key]

    age = datetime.now().year - annee
    base -= age * 400

    if km > 80000:
        base -= 700
    if km > 120000:
        base -= 1200

    coef_dep = 1.0
    if departement == "75":
        coef_dep = 1.08
    elif departement == "13":
        coef_dep = 1.05
    elif departement == "69":
        coef_dep = 1.04
    elif departement == "59":
        coef_dep = 0.95

    base = int(base * coef_dep)

    annonces = [base*1.05, base*0.98, base*1.02, base, base*0.95]
    moyenne = sum(annonces)/len(annonces)

    prix_marche = int(moyenne * 0.95)

    prix_bas = int(prix_marche * 0.93)
    prix_haut = int(prix_marche * 1.05)

    net_bas = prix_bas - commission
    net_marche = prix_marche - commission
    net_haut = prix_haut - commission

    st.markdown(f"### Vente rapide : {prix_bas} € → Net : {net_bas} €")
    st.markdown(f"### Prix marché BIWIZ : {prix_marche} € → Net : {net_marche} €")
    st.markdown(f"### Prix haut : {prix_haut} € → Net : {net_haut} €")
