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
def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire,
        "trial": True
    }

    requests.post(WEBHOOK_URL, json=data)

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

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
    techno = st.selectbox("Technologie de boîte", ["-", "DSG", "EDC", "CVT", "BVA"])
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4"])

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])

places = st.selectbox("Nombre de places", [2,3,4,5,6,7])

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

# 🔥 NOUVEAU : DEPARTEMENT OBLIGATOIRE
departement = st.selectbox(
    "Département",
    [
        "01","02","03","04","05","06","07","08","09",
        "10","11","12","13","14","15","16","17","18","19",
        "21","22","23","24","25","26","27","28","29",
        "30","31","32","33","34","35","36","37","38","39",
        "40","41","42","43","44","45","46","47","48","49",
        "50","51","52","53","54","55","56","57","58","59",
        "60","61","62","63","64","65","66","67","68","69",
        "70","71","72","73","74","75","76","77","78","79",
        "80","81","82","83","84","85","86","87","88","89",
        "90","91","92","93","94","95","971","972","973","974"
    ]
)

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants","Sièges électriques",
        "Régulateur","Radar","Caméra","GPS","Bluetooth",
        "CarPlay","Android Auto","Audio premium","Toit ouvrant",
        "Toit panoramique","LED","Attelage"
    ]
)

commission = st.number_input("Commission (€)", 0, 10000, 1000)
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    base = 11500
    age = datetime.now().year - annee

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 3500
    elif marque.lower() in ["renault","peugeot","citroen"]:
        base += 1200

    if boite == "Automatique":
        base += 1200

    if carburant == "Hybride":
        base += 1500
    elif carburant == "Électrique":
        base += 3000

    base -= age * 550

    if km > 80000:
        base -= 900
    if km > 120000:
        base -= 1300
    if km > 160000:
        base -= 1800

    base += len(options) * 100

    if "captur" in modele.lower():
        base += 800

    # 🔥 BIWIZ
    prix_marche = int(base)

    if prix_marche < 6800:
        prix_marche = 6800

    # 🔥 AJUSTEMENT DÉPARTEMENT
    coef_dep = 1.0

    if departement in ["75","92","93","94","91","77","78","95"]:
        coef_dep = 1.08
    elif departement in ["06","83"]:
        coef_dep = 1.07
    elif departement in ["69","33","31","34","44"]:
        coef_dep = 1.04
    elif departement in ["52","23","15","48","70","58"]:
        coef_dep = 0.92
    elif departement in ["59","62","08"]:
        coef_dep = 0.95

    prix_marche = int(prix_marche * coef_dep)

    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.06)
    prix_garage = int(prix_bas - 1000)

    if commission_pct > 0:
        commission_calc = prix_marche * (commission_pct / 100)
    else:
        commission_calc = commission

    net_bas = int(prix_bas - commission_calc)
    net_marche = int(prix_marche - commission_calc)
    net_haut = int(prix_haut - commission_calc)
    net_garage = int(prix_garage - commission_calc)

    st.markdown(f"### 🔻 Vente rapide : {prix_bas} €  → Net vendeur : {net_bas} €")
    st.markdown(f"### 📊 Prix marché (BIWIZ) : {prix_marche} €  → Net vendeur : {net_marche} €")
    st.markdown(f"### 🔺 Prix annonce : {prix_haut} €  → Net vendeur : {net_haut} €")
    st.markdown(f"### 🟢 Prix Leboncoin (garage) : {prix_garage} €  → Net vendeur : {net_garage} €")
