import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import base64

# 🔥 IA AJOUT SÉCURISÉ (NE BUG PLUS)
try:
    import joblib
    import os
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ---------------- CONFIG ----------------
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
MAKE_PRICE_WEBHOOK = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"

# ✅ IMPORTANT : webhook différent pour prix
MAKE_PRICE_WEBHOOK = "https://hook.eu1.make.com/XXXXX_PRIX"

SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# ---------------- LOAD USERS ----------------
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    return df

# ---------------- LOGIN ----------------
def check_login(username, password):
    df = load_users()

    user = df[
        (df["username"] == username.strip()) &
        (df["password"] == password.strip())
    ]

    if not user.empty:
        expire = user.iloc[0]["expire"]

        if datetime.now() > expire:
            return "expired"

        return "ok"

    return "error"

# ---------------- WEBHOOK ----------------
def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "expire": expire,
        "trial": True
    }

    requests.post(WEBHOOK_URL, json=data)

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# 🔥 RESET ID (clé dynamique indispensable)
if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

if st.session_state.admin_logged:
    st.session_state.logged = True

# ================= LOGIN =================
if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")

    st.info("Après 3 jours d'essai, accès complet : 99€/an.")
    st.markdown(f"[💳 S'abonner maintenant]({STRIPE_LINK})")

    new_user = st.text_input("Créer un identifiant")
    new_pass = st.text_input("Créer un mot de passe", type="password")

    if st.button("Créer compte"):
        if new_user and new_pass:
            send_to_webhook(new_user, new_pass)
            st.success("Compte créé")
        else:
            st.error("Remplir tous les champs")

    st.markdown("---")

    st.subheader("🔐 Connexion")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user.strip() == ADMIN_USER and pwd.strip() == ADMIN_PASS:
            st.session_state.logged = True
            st.session_state.admin_logged = True
            st.rerun()

        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.rerun()

        elif result == "expired":
            st.error("⛔ Abonnement expiré")
            st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

    st.stop()

# ================= APP =================

st.title("🚗 VELIORA COTATION PRO")

# 🔥 RESET QUI FONCTIONNE VRAIMENT
if st.button("🔄 Nouvelle cotation (reset)"):
    st.session_state.reset_id += 1
    st.rerun()

# 🔐 LOGOUT
if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
    st.rerun()

# ================= INPUTS =================

rid = st.session_state.reset_id

marque = st.text_input("Marque", key=f"marque_{rid}")
modele = st.text_input("Modèle", key=f"modele_{rid}")
sous_version = st.text_input("Sous-version", key=f"sous_{rid}")
finition = st.text_input("Finition", key=f"finition_{rid}")
motorisation = st.text_input("Motorisation", key=f"moteur_{rid}")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1,13)), key=f"mois_{rid}")
    annee = st.number_input("Année", 1990, datetime.now().year, 2019, key=f"annee_{rid}")
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key=f"carb_{rid}")

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key=f"boite_{rid}")

    techno = st.selectbox(
        "Technologie de boîte",
        ["-","DSG","EDC","CVT","BVA","BVM","BVA6","BVA8","BVA9","BVM6","BVM7","7G-Tronic","9G-Tronic"],
        key=f"tech_{rid}"
    )

    traction = st.selectbox(
        "Transmission",
        ["-","Traction","Propulsion","4x4","4WD","4x4 permanent","4x4 enclenchable"],
        key=f"traction_{rid}"
    )

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"], key=f"etat_{rid}")
places = st.selectbox("Nombre de places", [2,3,4,5,6,7], key=f"places_{rid}")
portes = st.selectbox("Nombre de portes", [1,2,3,4,5], key=f"portes_{rid}")
km = st.number_input("Kilométrage", 0, 400000, 90000, key=f"km_{rid}")

departement = st.selectbox(
    "Département",
    ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
     "16","17","18","19","21","22","23","24","25","26","27","28","29","30","31",
     "32","33","34","35","36","37","38","39","40","41","42","43","44","45","46",
     "47","48","49","50","51","52","53","54","55","56","57","58","59","60","61",
     "62","63","64","65","66","67","68","69","70","71","72","73","74","75","76",
     "77","78","79","80","81","82","83","84","85","86","87","88","89","90","91",
     "92","93","94","95","971","972","973","974"],
    key=f"dep_{rid}"
)

options = st.multiselect(
    "Options du véhicule",
    [
        "Climatisation automatique","Accès sans clé","Hayon électrique",
        "Sellerie cuir","Sièges chauffants","Sièges chauffants avant","Sièges chauffants arrière",
        "Sièges électriques","Régulateur","Radar","Bip de recul","Radar arrière","Radar avant",
        "Caméra","Caméra de recul","GPS","Bluetooth","USB","CarPlay","Android Auto",
        "Connexion Apple","Connexion Android","Audio premium","Toit ouvrant",
        "Toit panoramique","LED","Rétroviseurs électriques","Rétroviseurs rabattables électriquement",
        "Attelage"
    ],
    key=f"options_{rid}"
)

commission = st.number_input("Commission (€)", 0, 10000, 1000, key=f"com_{rid}")
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0, key=f"comp_{rid}")

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    base = 13500
    age = datetime.now().year - annee

    base -= age * 400

    if km > 80000:
        base -= 600
    if km > 120000:
        base -= 900

    base += len(options) * 120

    prix_calcul = int(base)

    # ===== API MAKE CORRIGÉE =====
    prix_marche_api = None

    try:
        query = f"{marque} {modele} {annee} {km} km"

        response = requests.post(
            MAKE_PRICE_WEBHOOK,
            json={"query": query},
            timeout=15
        )

        st.write("DEBUG STATUS:", response.status_code)
        st.write("DEBUG TEXT:", response.text)

        if response.status_code == 200:
            data = response.json()

            if "prix_marche" in data and data["prix_marche"] > 3000:
                prix_marche_api = int(data["prix_marche"])

    except Exception as e:
        st.error(f"Erreur API : {e}")

    prix_annonces = [
        prix_calcul * 0.85,
        prix_calcul * 0.9,
        prix_calcul * 0.95,
        prix_calcul * 1.05,
        prix_calcul * 1.1
    ]

    if prix_marche_api:
        prix_marche = prix_marche_api
    else:
        prix_marche = int(statistics.median(prix_annonces))

    moteur = motorisation.lower()

    if "puretech" in moteur:
        prix_marche *= 0.80

        if km > 80000:
            prix_marche *= 0.85
        if km > 120000:
            prix_marche *= 0.75
        if annee < 2016:
            prix_marche *= 0.85

    prix_marche = int(prix_marche)

    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.08)

    if commission_pct > 0:
        commission_calc = prix_marche * (commission_pct / 100)
    else:
        commission_calc = commission

    net_bas = int(prix_bas - commission_calc)
    net_marche = int(prix_marche - commission_calc)
    net_haut = int(prix_haut - commission_calc)

    st.markdown("---")
    st.markdown("## 📊 Résultat de l'estimation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🔻 Vente rapide", f"{prix_bas} €", f"Net vendeur : {net_bas} €")

    with col2:
        st.metric("⭐ Prix marché", f"{prix_marche} €", f"Net vendeur : {net_marche} €")

    with col3:
        st.metric("🔺 Prix haut", f"{prix_haut} €", f"Net vendeur : {net_haut} €")
