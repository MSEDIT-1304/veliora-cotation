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
    user = df[(df["username"] == username.strip()) & (df["password"] == password.strip())]

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

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):

        # ADMIN
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged = True
            st.session_state.admin = True
            st.rerun()

        # USER
        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.session_state.user = user
            st.session_state.admin = False
            st.rerun()

        elif result == "expired":
            st.error("⛔ Abonnement expiré")
            st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

    st.stop()

# ================= ADMIN =================
if st.session_state.admin:

    st.title("🛠 ADMIN PANEL")

    if st.button("Se déconnecter"):
        st.session_state.logged = False
        st.session_state.admin = False
        st.rerun()

    st.dataframe(load_users())
    st.stop()

# ================= APP =================

st.title("🚗 VELIORA COTATION PRO")

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.rerun()

# -------- INFOS VEHICULE --------
marque = st.text_input("Marque")
modele = st.text_input("Modèle")
annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
places = st.selectbox("Nombre de places", [2,3,4,5,6,7])
portes = st.selectbox("Portes", [2,3,4,5])

departement = st.text_input("Département")

etat = st.selectbox("État", ["Bon état","Très bon état","Excellent état"])

options = st.multiselect("Options", [
    "GPS","Cuir","Toit ouvrant","Caméra","LED","CarPlay","Android Auto",
    "Régulateur","Radar","Sièges chauffants","Toit panoramique"
])

# -------- COMMISSION --------
col1, col2 = st.columns(2)
with col1:
    commission_euro = st.number_input("Commission (€)", 0, 10000, 1000)
with col2:
    commission_pct = st.number_input("Commission (%)", 0, 100, 0)

# ================= CALCUL =================
if st.button("Calculer estimation"):

    base = 20000

    # Premium
    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 4000

    # Age
    age = datetime.now().year - annee
    base -= age * 800

    # Kilométrage
    base -= km * 0.05

    # Boîte
    if boite == "Automatique":
        base += 1500

    # Carburant
    if carburant == "Hybride":
        base += 2000
    elif carburant == "Électrique":
        base += 5000

    # Options
    base += len(options) * 150

    # État
    if etat == "Très bon état":
        base += 1000
    elif etat == "Excellent état":
        base += 2000

    # Département (marché dynamique)
    if departement in ["75","92","78","69","13"]:
        base += 1500

    # ---- PRIX ----
    prix_bas = int(base * 0.85)
    prix_marche = int(base)
    prix_haut = int(base * 1.15)
    prix_pro = int(base * 0.75)

    # ---- COMMISSION ----
    commission_total = commission_euro + (prix_marche * commission_pct / 100)
    net = prix_marche - commission_total

    # ---- AFFICHAGE ----
    st.markdown(f"## 🔻 Prix bas : {prix_bas} €")
    st.markdown(f"## ⚖️ Prix marché : {prix_marche} €")
    st.markdown(f"## 🔺 Prix haut : {prix_haut} €")

    st.markdown("---")

    st.markdown(f"### 🏢 Estimation PRO : {prix_pro} €")

    st.markdown("---")

    st.markdown(f"### 💰 Net vendeur : {int(net)} €")
