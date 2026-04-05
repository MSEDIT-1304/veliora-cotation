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

marques = [
    "Audi","BMW","Mercedes","Volkswagen","Peugeot","Renault","Citroën","DS",
    "Toyota","Hyundai","Kia","Ford","Nissan","Honda","Mazda","Volvo",
    "Skoda","Seat","Cupra","Fiat","Alfa Romeo","Jeep","Dacia","Opel"
]

marque = st.selectbox("Marque", marques)
modele = st.text_input("Modèle")
sous_version = st.text_input("Finition / Sous-version (ex: AMG, GT Line...)")

annee = st.number_input("Année", 1990, datetime.now().year, 2018)
km = st.number_input("Kilométrage", 0, 400000, 90000)

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
motorisation = st.text_input("Motorisation")

portes = st.selectbox("Portes", [1,2,3,4,5])
transmission = st.selectbox("Transmission", ["Traction","Propulsion","4WD"])

options = st.multiselect("Options", ["GPS","Caméra","Cuir","Toit pano","Audio"])

# ---------------- CALCUL ----------------

if st.button("🚀 Estimer"):

    with st.spinner("Analyse du marché..."):
        time.sleep(1)

    age = datetime.now().year - annee

    # PRIX NEUF
    prix_neuf = 25000

    if marque.lower() in ["bmw","audi","mercedes"]:
        prix_neuf = 45000

    if marque.lower() == "dacia":
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

    # 🔥 SOUS-VERSION (ULTRA IMPORTANT)
    v = sous_version.lower()

    if any(x in v for x in [
        "amg","rs","gti","gtd","m ","m sport","gt","cupra","vrs"
    ]):
        valeur *= 1.18

    elif any(x in v for x in [
        "line","s line","gt line","r line","allure","shine",
        "intens","initiale","business","exclusive"
    ]):
        valeur *= 1.08

    elif any(x in v for x in [
        "access","trend","life","active","essential"
    ]):
        valeur *= 0.93

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

    # AJUSTEMENT MARCHÉ
    valeur *= 1.05

    # CORRECTION PRIX
    valeur -= 1000

    if valeur < 3000:
        valeur = 3000

    # PRIX VENDEUR
    prix_bas = int(valeur * 0.92)
    prix_moyen = int(valeur + 700)
    prix_haut = int(prix_moyen + 700)

    # VERDICT
    if prix_bas < valeur * 0.9:
        verdict = "🔥 Très bonne affaire"
    elif prix_bas < valeur:
        verdict = "✅ Bonne affaire"
    else:
        verdict = "⚠️ Prix élevé"

    # RESULTAT
    st.markdown(f"""
## 💰 PRIX NET VENDEUR

- Bas : **{prix_bas} €**
- Moyen : **{prix_moyen} €**
- Haut : **{prix_haut} €**

### {verdict}
""")

    if sous_version:
        st.success(f"✔️ Finition détectée : {sous_version}")
