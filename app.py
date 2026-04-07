import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random
import pandas as pd
import requests

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "TonMotDePasseFort123!"

SHEET_URL = "https://docs.google.com/spreadsheets/d/1JWWwLP3IKaG-EIsC3li84eouOFVFnv_C5MxBDQSzf3M/export?format=csv"
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"

# ---------------- USERS (GOOGLE SHEETS) ----------------
def load_users():
    try:
        df = pd.read_csv(SHEET_URL)
        users_dict = {}

        for _, row in df.iterrows():
            users_dict[row["username"]] = {
                "password": row["password"],
                "expire": row["expire"] if pd.notna(row["expire"]) else None,
                "trial": bool(row["trial"])
            }

        return users_dict

    except:
        return {}

# ---------------- SAVE VIA WEBHOOK ----------------
def save_users(username, password, expire, trial):
    try:
        data = {
            "username": username,
            "password": password,
            "expire": expire,
            "trial": trial
        }
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

users = load_users()

# ---------------- ADMIN AUTO ----------------
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
        "trial": False
    }

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

            users[new_user] = {
                "password": new_pwd,
                "expire": expire_date,
                "trial": True
            }

            save_users(new_user, new_pwd, expire_date, True)

            st.session_state.auth = True
            st.session_state.user = new_user
            st.rerun()
        else:
            st.error("Remplir les champs")

    st.markdown("---")

    st.markdown("### 🔐 Déjà client ?")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if user in users and users[user]["password"] == pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    # 🔥 TEST WEBHOOK
    if st.button("TEST WEBHOOK"):
        requests.post(WEBHOOK_URL, json={
            "username": "test",
            "password": "123",
            "expire": "2026-01-01",
            "trial": True
        })
        st.success("Webhook envoyé")

    st.stop()

# ---------------- USER DATA ----------------
user_data = users[st.session_state.user]

# ---------------- VERIFICATION ACCES ----------------
if user_data.get("expire"):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")

    if datetime.now() > expire_date:
        st.error("⛔ Votre accès a expiré")
        st.markdown(f"[💳 S’abonner pour continuer]({PAYMENT_LINK})")
        st.stop()

# ---------------- HEADER ----------------
st.write(f"👤 Connecté : {st.session_state.user}")

# ---------------- INFO TRIAL ----------------
if user_data.get("trial", False):
    expire_date = datetime.strptime(user_data["expire"], "%Y-%m-%d")
    jours_restants = (expire_date - datetime.now()).days
    st.info(f"🎁 Essai gratuit actif – {jours_restants} jour(s) restant(s)")

# ---------------- PAIEMENT ----------------
st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):

    expire_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

    users[st.session_state.user]["expire"] = expire_date
    users[st.session_state.user]["trial"] = False

    save_users(
        st.session_state.user,
        users[st.session_state.user]["password"],
        expire_date,
        False
    )

    st.success("🎉 Abonnement activé pour 1 an")

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

    annonces = []

    for i in range(5):
        km_a = max(10000, km + random.randint(-40000, 40000))
        prix_a = base + random.randint(-2000, 2000)

        if km_a > km:
            prix_a -= (km_a - km) * 0.02
        else:
            prix_a += (km - km_a) * 0.02

        annonces.append((int(km_a), int(prix_a)))

    annonces = sorted(annonces, key=lambda x: x[0])

    prix_moyen = int(sum([p for _, p in annonces]) / len(annonces))
    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    if prix_moyen < prix_moyen - 500:
        badge = "🟢 Bonne affaire"
    elif prix_moyen <= prix_moyen + 800:
        badge = "🟡 Prix marché"
    else:
        badge = "🔴 Trop cher"

    net = prix_moyen - commission

    st.markdown("## 📊 ESTIMATION")

    st.markdown(f"""
### 💰 Prix de vente
🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} € {badge}  
🔺 Haut : {prix_haut} €

### 🧾 Net vendeur
➡️ {net} €
""")

    st.markdown("## 📈 COMPARATIF ANNONCES")

    for km_a, prix_a in annonces:
        st.write(f"🚗 {km_a} km → {prix_a} €")
