# (début inchangé)

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics

try:
    import joblib
    import os
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

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

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if st.session_state.admin_logged:
    st.session_state.logged = True

# LOGIN inchangé
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

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
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

    techno = st.selectbox("Technologie de boîte", ["-","DSG","EDC","CVT","BVA","BVM","BVA6","BVA8","BVA9","BVM6","BVM7","7G-Tronic","9G-Tronic"])

    traction = st.selectbox("Transmission", ["-","Traction","Propulsion","4x4","4WD","4x4 permanent","4x4 enclenchable"])

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])
places = st.selectbox("Nombre de places", [2,3,4,5,6,7])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

departement = st.selectbox("Département", [...])  # inchangé

options = st.multiselect("Options du véhicule", [...])  # inchangé

commission = st.number_input("Commission (€)", 0, 10000, 1000)
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    base = 13500
    age = datetime.now().year - annee

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 4000
    elif marque.lower() in ["renault","peugeot","citroen"]:
        base += 1800

    if boite == "Automatique":
        base += 1500

    if carburant == "Hybride":
        base += 1800
    elif carburant == "Électrique":
        base += 3500

    base -= age * 400

    if km > 80000:
        base -= 600
    if km > 120000:
        base -= 900
    if km > 160000:
        base -= 1200

    base += len(options) * 120

    if "captur" in modele.lower():
        base += 1200

    # 🔥 AJOUT INTELLIGENCE COTATION
    premium_brands = ["bmw","audi","mercedes","lexus","porsche"]
    if marque.lower() in premium_brands:
        base *= 1.08

    finition_haute = ["gt line","s line","amg","m sport","initiale","allure","exclusive"]
    if any(f in finition.lower() for f in finition_haute):
        base += 1800

    if any(x in motorisation.lower() for x in ["hybride","electrique","électrique"]):
        base += 1200

    options_premium = ["cuir","toit","bose","harman","camera","caméra"]
    for opt in options:
        if any(p in opt.lower() for p in options_premium):
            base += 250

    modele_recherche = ["3008","5008","qashqai","tucson","sportage","2008"]
    if any(m in modele.lower() for m in modele_recherche):
        base += 1500

    prix_calcul = int(base)

    if model:
        try:
            prix_ia = int(model.predict([[annee, km]])[0])
            prix_calcul = int((prix_calcul * 0.55) + (prix_ia * 0.45))
        except:
            pass

    # (reste inchangé)
