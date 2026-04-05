import streamlit as st
from datetime import datetime
import json
import os
import time

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
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
    st.title("🔐 Accès Veliora Pro")

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):
        users = load_users()
        if user in users and users[user]["password"] == pwd:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    st.stop()

# ---------------- APP ----------------

st.title("🚗 VELIORA COTATION VENDEUR")

st.caption("Exemples : Audi, BMW, Peugeot, Tesla…")

# 🔥 MARQUE / MODELE
marque = st.text_input("Marque")
modele = st.text_input("Modèle")

# 🔥 FINITION + SOUS VERSION
finition = st.text_input("Finition (ex : GT Line, S Line, Business...)")
sous_version = st.text_input("Sous-version / Options (ex : Pack Tech, Full options...)")

# 🔥 DATE MISE EN CIRCULATION
col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois mise en circulation", list(range(1, 13)))

with col2:
    annee = st.number_input("Année mise en circulation", 1990, datetime.now().year, 2018)

# 🔥 AUTRES INFOS
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
motorisation = st.text_input("Motorisation")

portes = st.selectbox("Portes", [1,2,3,4,5])
transmission = st.selectbox("Transmission", ["Traction","Propulsion","4WD"])

options = st.multiselect("Options", ["GPS","Caméra","Cuir","Toit pano","Audio"])

# ---------------- CALCUL ----------------

if st.button("🚀 Estimer"):

    if not marque or not modele:
        st.warning("Merci de renseigner marque et modèle")
        st.stop()

    marque = marque.strip().lower()

    with st.spinner("Analyse du marché..."):
        time.sleep(1)

    # 🔥 AGE PRÉCIS
    today = datetime.now()
    age = today.year - annee
    if today.month < mois:
        age -= 1

    # PRIX NEUF
    prix_neuf = 25000

    if marque in ["bmw","audi","mercedes"]:
        prix_neuf = 45000

    if marque == "dacia":
        prix_neuf = 18000

    if "suv" in modele.lower() or "3008" in modele.lower():
        prix_neuf += 5000

    if "clio" in modele.lower() or "208" in modele.lower():
        prix_neuf = 18000

    # DÉCOTE
    if age <= 1:
        valeur = prix_neuf * 0.85
    elif age <= 3:
        valeur = prix_neuf * 0.72
    elif age <= 5:
        valeur = prix_neuf * 0.62
    elif age <= 8:
        valeur = prix_neuf * 0.52
    else:
        valeur = prix_neuf * 0.42

    # KM
    km_moyen = age * 15000
    valeur += (km_moyen - km) * 0.025

    # MOTORISATION
    m = motorisation.lower()
    if "150" in m or "gt" in m:
        valeur *= 1.08
    elif "90" in m:
        valeur *= 0.95

    # PORTES
    if portes <= 2:
        valeur *= 0.93
    elif portes == 5:
        valeur *= 1.03

    # TRANSMISSION
    if transmission == "4WD":
        valeur *= 1.08
    elif transmission == "Propulsion":
        valeur *= 1.03

    # FINITION
    f = finition.lower()
    if any(x in f for x in ["amg","rs","gti","m","gt"]):
        valeur *= 1.18
    elif any(x in f for x in ["line","business","allure","shine"]):
        valeur *= 1.08

    # SOUS VERSION
    sv = sous_version.lower()
    if "full" in sv:
        valeur *= 1.05
    elif "pack" in sv:
        valeur *= 1.03

    # BOITE
    if boite == "Automatique":
        valeur *= 1.05

    # CARBURANT
    if carburant == "Diesel":
        valeur *= 0.95
    elif carburant == "Électrique":
        valeur *= 1.20

    # OPTIONS
    valeur += len(options) * 120

    # AJUSTEMENT
    valeur *= 1.05
    valeur -= 1000

    if valeur < 3000:
        valeur = 3000

    # PRIX
    prix_bas = int(valeur * 0.92)
    prix_moyen = int(valeur + 700)
    prix_haut = int(prix_moyen + 700)

    # VERDICT
    if prix_bas < valeur * 0.9:
        verdict = "Très bonne affaire"
        badge = "🟢✔️✔️"
    elif prix_bas < valeur:
        verdict = "Bonne affaire"
        badge = "🟢✔️"
    else:
        verdict = "Prix élevé"
        badge = "🔴⚠️"

    # RESULTAT
    st.markdown(f"""
## 💰 PRIX NET VENDEUR

**Bas** : {prix_bas} €  
**Moyen** : {prix_moyen} € {badge}  
**Haut** : {prix_haut} €  

### {verdict}
""")

    if finition:
        st.success(f"✔️ Finition : {finition}")
    if sous_version:
        st.success(f"✔️ Sous-version : {sous_version}")
