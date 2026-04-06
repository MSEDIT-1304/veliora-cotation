import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random

st.set_page_config(page_title="Veliora Pro", layout="wide")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"
FILE_PATH = "users.json"

# ---------------- USERS ----------------
def load_users():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    return json.load(open(FILE_PATH))

def save_users(data):
    json.dump(data, open(FILE_PATH, "w"))

users = load_users()

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 Accès Veliora Pro")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

    # -------- CONNEXION --------
    with tab1:
        user = st.text_input("Utilisateur", key="login_user")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter"):
            if user in users and users[user]["password"] == pwd:

                expire = users[user].get("expire")

                if expire:
                    expire_date = datetime.strptime(expire, "%Y-%m-%d")

                    if datetime.now() > expire_date:
                        st.error("⛔ Accès expiré")
                        st.markdown(f"[💳 S'abonner 99€/an]({PAYMENT_LINK})")
                        st.stop()

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    # -------- ESSAI GRATUIT --------
    with tab2:
        new_user = st.text_input("Créer un utilisateur", key="trial_user")
        new_pwd = st.text_input("Mot de passe", type="password", key="trial_pwd")

        if st.button("Créer essai"):
            if new_user in users:
                st.error("Utilisateur déjà existant")
            else:
                users[new_user] = {
                    "password": new_pwd,
                    "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                }
                save_users(users)
                st.success("✅ Essai gratuit activé pour 7 jours")

    st.markdown("💳 Offre lancement : **99€/AN**")

    st.stop()

# ---------------- SESSION ----------------
user = st.session_state.user
data = users[user]

# ---------------- CHECK EXPIRE ----------------
expire = data.get("expire")

if expire:
    expire_date = datetime.strptime(expire, "%Y-%m-%d")

    if datetime.now() > expire_date:
        st.error("⛔ Abonnement expiré")
        st.markdown(f"[💳 Renouveler 99€/an]({PAYMENT_LINK})")
        st.stop()

# ---------------- HEADER ----------------
st.title("🚗 VELIORA COTATION PRO")
st.write(f"👤 Connecté : {user}")

# ---------------- STRIPE ----------------
st.markdown(f"[💳 S'abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer 1 an"):
    users[user]["expire"] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    save_users(users)
    st.success("🎉 Abonnement actif 1 an")
    st.rerun()

st.divider()

# ---------------- FORMULAIRE COMPLET ----------------

col1, col2 = st.columns(2)

with col1:
    marque = st.text_input("Marque (libre)")
    modele = st.text_input("Modèle")
    version = st.text_input("Sous-version")

with col2:
    mois = st.selectbox("Mois", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2018)
    km = st.number_input("Kilométrage", 0, 400000, 90000)

etat = st.selectbox("État du véhicule", ["Excellent","Très bon","Bon","Correct"])

boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

technologie = st.selectbox("Technologie de boîte", ["BVA6","BVA7","BVA8"])

traction = st.selectbox("Transmission", ["-","4WD","4x4"])

departement = st.text_input("Département")

options = st.multiselect("Options", [
    "Climatisation automatique",
    "Sellerie cuir",
    "GPS",
    "Caméra de recul",
    "Caméra 360",
    "CarPlay / Android Auto",
    "Toit ouvrant",
    "Toit panoramique",
    "Feux LED",
    "Attelage",
    "Radar de recul",
    "Audio premium",
    "Sièges chauffants avant",
    "Sièges chauffants AV/AR",
    "Rétros chauffants",
    "Rétros rabattables électriques"
])

commission = st.number_input("Commission (€)", 0, 5000, 1000)

# ---------------- AJUSTEMENT DÉPARTEMENT ----------------
def ajustement_dep(dep):
    premium = ["75","92","93","94"]
    haut = ["06","74","33","69","13"]
    moyen = ["59","44","31","34","83","67"]
    faible = ["02","08","10","18","23"]
    tres_faible = ["15","19","46","48"]

    if dep in premium:
        return 1500
    elif dep in haut:
        return 1200
    elif dep in moyen:
        return 800
    elif dep in faible:
        return -500
    elif dep in tres_faible:
        return -1000
    return 0

# ---------------- ESTIMATION ----------------
if st.button("Calculer estimation"):

    age = datetime.now().year - annee

    base = 20000
    base -= age * 900
    base -= (km / 10000) * 250

    if marque.lower() in ["audi","bmw","mercedes","tesla"]:
        base += 2500

    if boite == "Automatique":
        base += 1200

    if traction != "-":
        base += 1200

    if etat == "Excellent":
        base += 1500
    elif etat == "Très bon":
        base += 800
    elif etat == "Correct":
        base -= 800

    base += len(options) * 150

    base += ajustement_dep(departement)

    # -------- SIMULATION MARCHÉ --------
    annonces = []
    for i in range(8):
        km_fake = km + random.randint(-30000, 30000)
        prix = int(base + random.randint(-2000, 2000))
        annonces.append((km_fake, prix))

    marche = int(sum([p for _, p in annonces]) / len(annonces))

    # -------- FUSION INTELLIGENTE --------
    capacar = base
    biwiz = base * 0.92

    prix_moyen = int(capacar * 0.4 + biwiz * 0.2 + marche * 0.4)

    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    net = prix_moyen - commission

    # -------- AFFICHAGE --------
    st.markdown("## 📊 Résultat")

    st.success(f"⚖️ Prix marché : {prix_moyen} € → 🟢 Bonne affaire")

    st.write(f"🔻 Bas : {prix_bas} €")
    st.write(f"🔺 Haut : {prix_haut} €")

    st.write(f"💰 Net vendeur : {net} €")

    st.markdown("## 📈 Comparatif annonces")

    for km_fake, prix in annonces:
        st.write(f"{km_fake} km → {prix} €")
