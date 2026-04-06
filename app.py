import streamlit as st
from datetime import datetime
import json
import os
import random

st.set_page_config(page_title="Veliora Pro", layout="wide")

# ---------------- DESIGN PREMIUM ----------------
st.markdown("""
<style>
body {background: linear-gradient(135deg,#0f172a,#1e293b); color:white;}
.card {
    background:#1e293b;
    padding:25px;
    border-radius:15px;
    margin-bottom:20px;
    box-shadow:0 4px 15px rgba(0,0,0,0.3);
}
.title {font-size:26px;font-weight:bold;}
.good {color:#22c55e;font-weight:bold;}
.warning {color:#facc15;font-weight:bold;}
.bad {color:#ef4444;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ---------------- USERS ----------------
FILE_PATH = "users.json"

def load_users():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    return json.load(open(FILE_PATH))

users = load_users()

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🚗 Veliora Pro")

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Connexion"):
        if user in users and users[user]["password"] == pwd:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    st.stop()

# ---------------- BASE FRANCE ----------------
def get_dep_adjustment(dep):
    premium = ["75","92","93","94"]
    haut = ["06","74","33","69","13"]
    moyen = ["59","44","31","34","83","67"]
    faible = ["02","08","10","18","23","36","52","58","70","87"]
    tres_faible = ["15","19","46","48","55","89"]

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

# ---------------- UI ----------------
st.markdown('<div class="title">🚗 Estimation professionnelle</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")
    version = st.text_input("Version")

with col2:
    mois = st.selectbox("Mois", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2018)
    km = st.number_input("Kilométrage", 0, 300000, 90000)

etat = st.selectbox("État", ["Excellent","Très bon","Bon","Correct"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
tech = st.selectbox("Technologie boîte", ["BVA6","BVA7","BVA8"])
traction = st.selectbox("Transmission", ["-","4WD","4x4"])

departement = st.text_input("Département")

options = st.multiselect("Options", [
    "Clim auto","Cuir","GPS","Caméra","CarPlay",
    "Toit ouvrant","LED","Attelage","Radar","Audio premium"
])

commission = st.number_input("Commission (€)", 0, 5000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Calculer estimation"):

    age = datetime.now().year - annee

    base = 20000

    # décote
    base -= age * 900
    base -= (km / 10000) * 250

    # premium
    if marque.lower() in ["audi","bmw","mercedes","tesla","porsche"]:
        base += 2500

    # équipements
    if boite == "Automatique":
        base += 1200
    if traction != "-":
        base += 1200
    base += len(options) * 150

    # état
    if etat == "Excellent":
        base += 1500
    elif etat == "Très bon":
        base += 800
    elif etat == "Correct":
        base -= 800

    # département
    base += get_dep_adjustment(departement)

    # ---------------- SIMULATION MARCHÉ ----------------
    annonces = []
    for i in range(8):
        km_fake = km + random.randint(-30000, 30000)
        prix = int(base + random.randint(-2000, 2000))
        annonces.append((km_fake, prix))

    marche = int(sum([p for _, p in annonces]) / len(annonces))

    # multi-source
    capacar = base
    biwiz = base * 0.92

    prix_moyen = int(capacar * 0.4 + biwiz * 0.2 + marche * 0.4)
    prix_bas = prix_moyen - 1500
    prix_haut = prix_moyen + 1500

    net = prix_moyen - commission

    # badge
    if prix_moyen < marche - 500:
        badge = "🟢 Bonne affaire"
    elif prix_moyen <= marche + 800:
        badge = "🟡 Prix marché"
    else:
        badge = "🔴 Trop cher"

    # ---------------- AFFICHAGE ----------------

    st.markdown("## 📊 Résultat")

    st.markdown(f"""
    <div class="card">
    🔻 Bas : {prix_bas} €<br>
    ⚖️ Marché : {prix_moyen} € <span class="good">{badge}</span><br>
    🔺 Haut : {prix_haut} €<br><br>
    💰 Net vendeur : {net} €
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📈 Annonces comparables")

    for km_fake, prix in annonces:
        st.write(f"{km_fake} km → {prix} €")
