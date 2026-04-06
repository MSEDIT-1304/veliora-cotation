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

# ADMIN
if ADMIN_USERNAME not in users:
    users[ADMIN_USERNAME] = {
        "password": ADMIN_PASSWORD,
        "expire": None,
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
        user = st.text_input("Utilisateur", key="login_user")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter"):
            users = load_users()

            if user in users and users[user]["password"] == pwd:
                st.session_state.auth = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    # TRIAL
    with tab2:
        new_user = st.text_input("Créer un utilisateur", key="trial_user")
        new_pwd = st.text_input("Mot de passe", type="password", key="trial_pwd")

        if st.button("Créer essai"):
            users = load_users()

            if new_user in users:
                st.error("Utilisateur déjà existant")
            else:
                users[new_user] = {
                    "password": new_pwd,
                    "expire": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "verified": True
                }
                save_users(users)
                st.success("Compte créé")

    st.stop()

# ---------------- APP ----------------

st.title("🚗 VELIORA COTATION PRO")

marque = st.selectbox("Marque", ["Audi","BMW","Mercedes","Peugeot","Renault","Volkswagen"])
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
mois = st.selectbox("Mois", list(range(1,13)))
km = st.number_input("Kilométrage", 0, 300000, 90000)

etat = st.selectbox("État du véhicule", ["Excellent","Très bon","Bon","Correct"])

boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
tech_boite = st.selectbox("Technologie boîte", ["BVA6","BVA7","BVA8"])

traction = st.selectbox("Transmission", ["-","4WD","4x4"])

options = st.multiselect("Options", [
    "Sièges chauffants avant","Sièges chauffants AV/AR","Attelage",
    "CarPlay / Android Auto","Rétros chauffants","Rétros rabattables",
    "Clim auto","GPS","Caméra","Cuir","Toit ouvrant"
])

commission = st.number_input("Commission (€)", 0, 5000, 1000)

# ---------------- ESTIMATION ----------------

if st.button("Calculer estimation"):

    age = datetime.now().year - annee

    base = 20000

    base -= age * 900
    base -= (km / 10000) * 250

    if marque in ["Audi","BMW","Mercedes"]:
        base += 2000

    if boite == "Automatique":
        base += 1200

    if traction in ["4WD","4x4"]:
        base += 1500

    if etat == "Excellent":
        base += 1500
    elif etat == "Très bon":
        base += 800

    # options
    base += len(options) * 150

    # ---------------- MARCHÉ SIMULÉ ----------------
    annonces = []
    for i in range(5):
        km_fake = km + random.randint(-30000, 30000)
        prix = int(base + random.randint(-2000, 2000))
        annonces.append((km_fake, prix))

    marche = int(sum([p for _, p in annonces]) / len(annonces))

    capacar = base
    biwiz = base * 0.92

    # 🔥 FUSION INTELLIGENTE
    prix_moyen = int(capacar * 0.4 + biwiz * 0.2 + marche * 0.4)

    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    net_bas = prix_bas - commission
    net_moyen = prix_moyen - commission
    net_haut = prix_haut - commission

    # ---------------- AFFICHAGE ----------------

    st.markdown("## 📊 PRIX DE VENTE")
    st.write(f"🔻 Bas : {prix_bas} €")
    st.write(f"⚖️ Marché : {prix_moyen} € 🟢 Bonne affaire")
    st.write(f"🔺 Haut : {prix_haut} €")

    st.markdown("## 💰 PRIX NET VENDEUR")
    st.write(f"Bas : {net_bas} €")
    st.write(f"Moyen : {net_moyen} €")
    st.write(f"Haut : {net_haut} €")

    st.markdown("## 📊 COMPARAISON MARCHÉ")
    for km_fake, prix in annonces:
        st.write(f"{km_fake} km → {prix} €")
