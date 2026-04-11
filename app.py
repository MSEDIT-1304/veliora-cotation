import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import base64

# 🔥 IA AJOUT SÉCURISÉ (NE BUG PLUS)
try:
    import joblib
    import os
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
MAKE_PRICE_WEBHOOK = "TON_WEBHOOK_MAKE_ICI"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# ---------------- RESET FUNCTION ----------------
def reset_form():
    keys = [
        "marque","modele","sous_version","finition","motorisation",
        "mois","annee","carburant","boite","techno","traction",
        "etat","places","portes","km","departement","options",
        "commission","commission_pct"
    ]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]

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
    user = df[(df["username"] == username.strip()) & (df["password"] == password.strip())]
    if not user.empty:
        expire = user.iloc[0]["expire"]
        if datetime.now() > expire:
            return "expired"
        return "ok"
    return "error"

# ---------------- WEBHOOK ----------------
def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    data = {"username": username, "password": password, "expire": expire, "trial": True}
    requests.post(WEBHOOK_URL, json=data)

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if st.session_state.admin_logged:
    st.session_state.logged = True

# ================= LOGIN =================
if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")
    st.info("Après 3 jours d'essai, accès complet : 99€/an.")
    st.markdown(f"[💳 S'abonner maintenant]({STRIPE_LINK})")

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

# 🔥 RESET BOUTON (FONCTIONNEL)
if st.button("🔄 Nouvelle cotation"):
    reset_form()
    st.rerun()

# ===== INPUTS AVEC KEY =====
marque = st.text_input("Marque", key="marque")
modele = st.text_input("Modèle", key="modele")
sous_version = st.text_input("Sous-version", key="sous_version")
finition = st.text_input("Finition", key="finition")
motorisation = st.text_input("Motorisation", key="motorisation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1,13)), key="mois")
    annee = st.number_input("Année", 1990, datetime.now().year, 2019, key="annee")
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key="carburant")

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key="boite")
    techno = st.selectbox("Technologie de boîte", ["-","DSG","EDC","CVT","BVA","BVM","BVA6","BVA8","BVA9","BVM6","BVM7","7G-Tronic","9G-Tronic"], key="techno")
    traction = st.selectbox("Transmission", ["-","Traction","Propulsion","4x4","4WD","4x4 permanent","4x4 enclenchable"], key="traction")

etat = st.selectbox("État du véhicule", ["Bon état","Excellent état"], key="etat")
places = st.selectbox("Nombre de places", [2,3,4,5,6,7], key="places")
portes = st.selectbox("Nombre de portes", [1,2,3,4,5], key="portes")
km = st.number_input("Kilométrage", 0, 400000, 90000, key="km")

departement = st.selectbox("Département", ["01","02","03","04","05"], key="departement")

options = st.multiselect("Options du véhicule", ["GPS","Bluetooth","Caméra"], key="options")

commission = st.number_input("Commission (€)", 0, 10000, 1000, key="commission")
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0, key="commission_pct")

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    base = 13500
    age = datetime.now().year - annee
    base -= age * 400

    if km > 80000:
        base -= 600

    prix_calcul = int(base)

    # 🔥 MAKE LEBONCOIN
    prix_marche_api = None
    try:
        r = requests.post(MAKE_PRICE_WEBHOOK, json={
            "marque": marque,
            "modele": modele,
            "annee": annee,
            "km": km
        })
        data = r.json()
        if "prix_marche" in data:
            prix_marche_api = int(data["prix_marche"])
    except:
        pass

    if prix_marche_api:
        prix_marche = prix_marche_api
    else:
        prix_marche = prix_calcul

    # 🔥 PURETECH PRO
    if "puretech" in motorisation.lower():
        prix_marche *= 0.80
        if km > 80000:
            prix_marche *= 0.85
        if km > 120000:
            prix_marche *= 0.75
        if annee < 2016:
            prix_marche *= 0.85

    prix_marche = int(prix_marche)

    st.metric("Prix marché", f"{prix_marche} €")
