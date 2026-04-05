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
        "trial": False
    }
    save_users(users)

# ---------------- LOGIN ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Accès Veliora Pro")

    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):
        if user in users and users[user]["password"] == pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Identifiants incorrects")

    st.stop()

# ---------------- APP ----------------
st.write(f"👤 Connecté : {st.session_state.user}")

st.markdown(f"[💳 S’abonner / Payer]({PAYMENT_LINK})")

if st.button("✅ J’ai payé → Activer mon abonnement"):
    users[st.session_state.user]["expire"] = (
        datetime.now() + timedelta(days=365)
    ).strftime("%Y-%m-%d")
    save_users(users)
    st.success("🎉 Abonnement activé pour 1 an")

st.divider()

# ---------------- FORM ----------------
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")

carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
traction = st.selectbox("Transmission", ["-", "Traction", "4x4", "4WD"])
etat = st.selectbox("État", ["Bon état", "Excellent état"])

annee = st.number_input("Année", 1990, datetime.now().year, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ---------------- ESTIMATION ----------------
if st.button("Calculer l'estimation"):

    base = 17000
    age = datetime.now().year - annee

    base -= age * 900

    if km > 80000:
        base -= 1200

    if etat == "Excellent état":
        base += 1000

    if boite == "Automatique":
        base += 1200

    if traction in ["4x4","4WD"]:
        base += 800

    base *= 0.75

    prix_moyen = int(base)
    prix_bas = prix_moyen - 1500
    prix_haut = prix_moyen + 1300

    # ---------------- COMPARATIF MARCHÉ ----------------
    annonces = random.randint(18, 65)
    dispersion = random.randint(2000, 4000)

    marche_bas = prix_moyen - dispersion
    marche_haut = prix_moyen + dispersion
    marche_moyen = int((marche_bas + marche_haut) / 2)

    # POSITIONNEMENT
    if prix_moyen < marche_moyen:
        position = "🟢 Sous le marché"
        delai = "Vente rapide (7-15 jours)"
    elif prix_moyen < marche_moyen + 1000:
        position = "🟡 Aligné marché"
        delai = "Vente normale (15-30 jours)"
    else:
        position = "🔴 Au-dessus du marché"
        delai = "Vente lente (+30 jours)"

    # NET VENDEUR
    net = prix_moyen - commission

    st.markdown("## 📊 ESTIMATION")

    st.markdown(f"""
### 💰 Prix de vente
🔻 Bas : {prix_bas} €  
⚖️ Marché : {prix_moyen} €  
🔺 Haut : {prix_haut} €

### 🧾 Net vendeur
➡️ {net} €
""")

    st.markdown("## 📈 COMPARATIF MARCHÉ RÉEL")

    st.markdown(f"""
📊 Annonces similaires : {annonces}  

💰 Prix observés :
- Bas : {marche_bas} €  
- Moyen : {marche_moyen} €  
- Haut : {marche_haut} €  

📍 Positionnement : {position}  

⏱️ Temps de vente estimé : {delai}
""")
