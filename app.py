import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import requests

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

SHEET_URL = "https://docs.google.com/spreadsheets/d/1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M/export?format=csv"
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"

# ---------------- LOAD USERS ----------------
def load_users():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        return pd.DataFrame(columns=["username", "password", "expire", "trial"])

# ---------------- LOGIN CHECK ----------------
def check_login(username, password):
    df = load_users()

    user = df[(df["username"] == username) & (df["password"] == password)]

    if user.empty:
        return False, None

    expire_date = pd.to_datetime(user.iloc[0]["expire"])

    if pd.Timestamp.now() > expire_date:
        return False, "expired"

    return True, user.iloc[0]

# ---------------- SESSION ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

# ---------------- PAGE ACCUEIL ----------------
if not st.session_state.auth:

    st.title("🚗 Veliora Pro")

    st.markdown("### 🎁 Essai gratuit 7 jours")

    new_user = st.text_input("Créer un identifiant")
    new_pwd = st.text_input("Créer un mot de passe", type="password")

    if st.button("🚀 Démarrer l'essai gratuit"):
        if new_user and new_pwd:

            expire_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            data = {
                "username": new_user,
                "password": new_pwd,
                "expire": expire_date,
                "trial": True
            }

            requests.post(WEBHOOK_URL, json=data)

            st.success("Compte créé ! Attends 2 secondes puis connecte-toi.")

        else:
            st.error("Remplir les champs")

    st.markdown("---")

    st.markdown("### 🔐 Déjà client ?")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        ok, data = check_login(user, pwd)

        if ok:
            st.session_state.auth = True
            st.session_state.user = user
            st.session_state.data = data
            st.rerun()

        elif data == "expired":
            st.error("⛔ Accès expiré")
            st.markdown(f"[💳 S’abonner]({PAYMENT_LINK})")

        else:
            st.error("Identifiants incorrects")

    # TEST WEBHOOK
    if st.button("TEST WEBHOOK"):
        requests.post(WEBHOOK_URL, json={
            "username": "test",
            "password": "123",
            "expire": "2026-01-01",
            "trial": True
        })
        st.success("Webhook envoyé")

    st.stop()

# ---------------- USER CONNECTÉ ----------------
st.write(f"👤 Connecté : {st.session_state.user}")

user_data = st.session_state.data

# ---------------- INFO TRIAL ----------------
expire_date = pd.to_datetime(user_data["expire"])
jours_restants = (expire_date - pd.Timestamp.now()).days

if user_data["trial"]:
    st.info(f"🎁 Essai actif – {jours_restants} jour(s) restant(s)")

# ---------------- PAIEMENT ----------------
st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):

    expire_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

    data = {
        "username": st.session_state.user,
        "password": user_data["password"],
        "expire": expire_date,
        "trial": False
    }

    requests.post(WEBHOOK_URL, json=data)

    st.success("🎉 Abonnement activé")

st.divider()

# ---------------- FORMULAIRE ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois de mise en circulation", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
    techno = st.selectbox("Technologie de boîte", ["-", "DSG", "EDC", "CVT", "BVA", "BVA6", "BVA7", "BVA8"])
    traction = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4", "4WD"])

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])

portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants avant","Sièges chauffants avant + arrière",
        "Sièges électriques","Régulateur de vitesse","Régulateur adaptatif",
        "Radar de recul","Bips avant","Bips arrière","Caméra de recul","Caméra 360",
        "GPS / Navigation","Bluetooth","Connexion Apple CarPlay","Connexion Android Auto",
        "Système audio premium","Rétroviseurs chauffants","Rétroviseurs électriques rabattables",
        "Jantes alliage","Toit ouvrant","Toit panoramique","Feux LED","Attelage","Détecteur angle mort"
    ]
)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Calculer l'estimation"):

    base = 17000
    age = datetime.now().year - annee

    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 3000

    if boite == "Automatique":
        base += 1200

    if techno in ["DSG","EDC"]:
        base += 400
    if techno in ["BVA6","BVA7","BVA8"]:
        base += 500

    if carburant == "Diesel":
        base += 300
    elif carburant == "Hybride":
        base += 2500
    elif carburant == "Électrique":
        base += 5000

    if traction in ["4x4","4WD"]:
        base += 800

    if etat == "Excellent état":
        base += 1200
    else:
        base -= 500

    base -= age * 900

    if km > 80000:
        base -= 1200
    if km > 120000:
        base -= 2000

    base += len(options) * 100
    base *= 0.90

    prix = int(base)
    net = prix - commission

    st.markdown(f"### 💰 Prix estimé : {prix} €")
    st.markdown(f"### 🧾 Net vendeur : {net} €")
