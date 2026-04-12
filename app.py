import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import base64
import io

# 🔥 IA AJOUT SÉCURISÉ
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
MAKE_PRICE_WEBHOOK = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"

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

    requests.post(WEBHOOK_URL, json=data)

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

rid = st.session_state.reset_id

marque = st.text_input("Marque", key=f"marque_{rid}")
modele = st.text_input("Modèle", key=f"modele_{rid}")
finition = st.text_input("Finition", key=f"finition_{rid}")
motorisation = st.text_input("Motorisation", key=f"moteur_{rid}")

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

departement = st.text_input("Département (ex: 08)")

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    prix_comparables = []

    try:
        query = f"{marque} {modele} {annee} {km} km {carburant} {boite} {departement} garage"

        response = requests.post(
            MAKE_PRICE_WEBHOOK,
            json={"query": query},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()

            if "prices" in data:
                prix_comparables = [int(p) for p in data["prices"] if p > 1000]

    except:
        pass

    # 🚨 DATA PURE
    if len(prix_comparables) < 3:
        st.error("❌ Données insuffisantes (annonces PRO non trouvées)")
        st.stop()

    prix_marche = int(statistics.median(prix_comparables))

    # ===== TABLEAU =====
    st.markdown("### 📊 Comparables (modifiable)")
    df = pd.DataFrame({"Prix (€)": prix_comparables[:10]})
    edited = st.data_editor(df)

    if not edited.empty:
        prix_marche = int(edited["Prix (€)"].median())

    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.08)

    net = prix_marche - commission

    col1, col2, col3 = st.columns(3)

    col1.metric("Bas", prix_bas)
    col2.metric("Marché", prix_marche, f"Net vendeur : {net} €")
    col3.metric("Haut", prix_haut)

    # DOWNLOAD
    buffer = io.StringIO()
    buffer.write(f"{marque} {modele}\nPrix marché: {prix_marche} €\nNet: {net} €")

    st.download_button("📥 Télécharger estimation", buffer.getvalue(), "estimation.txt")
