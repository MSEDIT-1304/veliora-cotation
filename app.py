import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
PAYMENT_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "TonMotDePasseFort123!"
FILE_PATH = "users.json"

# ---------------- USERS ----------------
def load_users():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

users = load_users()

if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
        "verified": True
    }
    save_users(users)

# ---------------- TRIAL ----------------
def create_trial(username, password):
    users = load_users()
    users[username] = {
        "password": password,
        "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "verified": True
    }
    save_users(users)

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 Accès Veliora Pro")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

    # LOGIN
    with tab1:
        user = st.text_input("Utilisateur")
        pwd = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):

            users = load_users()

            if user in users and users[user]["password"] == pwd:

                expire = users[user]["expire"]

                if expire:
                    expire_date = datetime.strptime(expire, "%Y-%m-%d")
                    if datetime.now() > expire_date:
                        st.error("⛔ Accès expiré")
                        st.markdown(f"[💳 S'abonner]({PAYMENT_LINK})")
                        st.stop()

                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    # TRIAL
    with tab2:
        new_user = st.text_input("Créer un utilisateur")
        new_pwd = st.text_input("Mot de passe", type="password")

        if st.button("Créer essai"):
            if new_user in users:
                st.error("Utilisateur déjà existant")
            else:
                create_trial(new_user, new_pwd)
                st.success("Compte créé")

    st.stop()

# ---------------- APP ----------------
users = load_users()
user_data = users[st.session_state.user]

st.write(f"👤 Connecté : {st.session_state.user}")

st.markdown("## 🔐 Accès professionnel")
st.success("✔️ Accès professionnel validé")

st.divider()

# ---------------- ABONNEMENT ----------------
if st.button("💳 Activer abonnement 1 an"):
    users[st.session_state.user]["expire"] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    save_users(users)
    st.success("🎉 Abonnement actif 1 an")
    st.rerun()

# ---------------- FORMULAIRE ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.selectbox("Marque", ["Audi","BMW","Mercedes","Peugeot","Renault","Volkswagen"])
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")

annee = st.number_input("Année", 2000, datetime.now().year, 2018)
km = st.number_input("Kilométrage", 0, 300000, 80000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
tech_boite = st.selectbox("Technologie boîte", ["BVM5","BVM6","BVA6","BVA7","BVA8"])
traction = st.selectbox("Transmission", ["Traction","Propulsion","4x4","AWD"])

etat = st.selectbox("État du véhicule", ["Excellent","Très bon","Bon","Moyen"])

options = st.multiselect("Options", [
    "Clim automatique","Sièges chauffants AV","Sièges chauffants AV/AR",
    "GPS","CarPlay / Android Auto","Caméra recul",
    "Attelage","Rétros chauffants","Rétros rabattables"
])

commission = st.number_input("Commission (€)", 0, 5000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Estimer"):

    base = 15000

    if marque in ["BMW","Audi","Mercedes"]:
        base += 3000

    base -= (datetime.now().year - annee) * 800
    base -= int(km / 20000) * 500

    if carburant == "Diesel":
        base -= 500

    if boite == "Automatique":
        base += 1000

    if etat == "Excellent":
        base += 1500
    elif etat == "Moyen":
        base -= 1500

    base += len(options) * 200

    # marché simulé
    annonces = []
    for i in range(3):
        km_sim = km + random.randint(-20000, 20000)
        prix_sim = base + random.randint(-1500, 1500)
        annonces.append((km_sim, prix_sim))

    marche = int(sum([p for _, p in annonces]) / len(annonces))

    capacar = base
    biwiz = base * 0.92

    prix_moyen = int(capacar * 0.4 + biwiz * 0.2 + marche * 0.4)
    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    st.markdown("## 📊 Comparatif marché")
    for km_sim, prix_sim in annonces:
        st.write(f"{km_sim} km → {prix_sim} €")

    st.markdown("## 💰 Prix de vente")
    st.write(f"🔻 Bas : {prix_bas} €")
    st.write(f"⚖️ Marché : {prix_moyen} € 🟢 Bonne affaire")
    st.write(f"🔺 Haut : {prix_haut} €")

    st.markdown("## 💸 Net vendeur")
    st.write(f"Bas : {prix_bas - commission} €")
    st.write(f"Moyen : {prix_moyen - commission} €")
    st.write(f"Haut : {prix_haut - commission} €")
