import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random

st.set_page_config(page_title="Veliora Pro", layout="wide")

# ---------------- DESIGN PREMIUM ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.good {
    color: #22c55e;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

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
    users[ADMIN_USERNAME] = {"password": ADMIN_PASSWORD}
    save_users(users)

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🚗 Veliora Pro")
    st.markdown("### 💎 Estimation professionnelle automobile")

    tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

    with tab1:
        user = st.text_input("Utilisateur", key="login_user")
        pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

        if st.button("Se connecter"):
            if user in users and users[user]["password"] == pwd:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    with tab2:
        new_user = st.text_input("Créer un utilisateur", key="trial_user")
        new_pwd = st.text_input("Mot de passe", type="password", key="trial_pwd")

        if st.button("Créer essai"):
            users[new_user] = {"password": new_pwd}
            save_users(users)
            st.success("Compte créé")

    st.markdown(f"💳 **Abonnement : 99€/AN (offre lancement)**")
    st.markdown(f"[👉 S'abonner maintenant]({PAYMENT_LINK})")

    st.stop()

# ---------------- APP ----------------

st.title("🚗 VELIORA COTATION PRO")

col1, col2 = st.columns(2)

with col1:
    marques = ["Audi","BMW","Mercedes","Peugeot","Renault","Volkswagen","Autre"]
    marque_select = st.selectbox("Marque", marques)

    if marque_select == "Autre":
        marque = st.text_input("Saisir la marque")
    else:
        marque = marque_select

    modele = st.text_input("Modèle")
    sous_version = st.text_input("Sous-version")

with col2:
    mois = st.selectbox("Mois", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    km = st.number_input("Kilométrage", 0, 300000, 90000)

etat = st.selectbox("État", ["Excellent","Très bon","Bon","Correct"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
tech = st.selectbox("Technologie boîte", ["BVA6","BVA7","BVA8"])
traction = st.selectbox("Transmission", ["-","4WD","4x4"])

options = st.multiselect("Options", [
    "Clim auto","Cuir","GPS","Caméra","CarPlay",
    "Toit ouvrant","LED","Attelage","Radar","Audio premium"
])

commission = st.number_input("Commission (€)", 0, 5000, 1000)

# ---------------- ESTIMATION ----------------

if st.button("Calculer estimation"):

    age = datetime.now().year - annee

    base = 18000
    base -= age * 850
    base -= (km / 10000) * 220

    if marque in ["Audi","BMW","Mercedes"]:
        base += 1800

    if boite == "Automatique":
        base += 1200

    if traction != "-":
        base += 1200

    base += len(options) * 150

    # 🔥 SIMULATION MARCHÉ TYPE LEBONCOIN
    annonces = []
    for i in range(8):
        km_fake = km + random.randint(-30000, 30000)
        prix = int(base + random.randint(-1800, 1800))
        annonces.append((km_fake, prix))

    marche = int(sum([p for _, p in annonces]) / len(annonces))

    capacar = base
    biwiz = base * 0.92

    prix_moyen = int(capacar * 0.4 + biwiz * 0.2 + marche * 0.4)

    prix_bas = prix_moyen - 1200
    prix_haut = prix_moyen + 1200

    net = prix_moyen - commission

    # ---------------- AFFICHAGE ----------------

    st.markdown("## 📊 Résultat estimation")

    st.markdown(f"""
    <div class="card">
    🔻 Bas : {prix_bas} €<br>
    ⚖️ Marché : {prix_moyen} € <span class="good">Bonne affaire</span><br>
    🔺 Haut : {prix_haut} €<br><br>
    💰 Net vendeur : {net} €
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Comparaison marché")

    for km_fake, prix in annonces:
        st.write(f"{km_fake} km → {prix} €")
