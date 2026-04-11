import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import base64

# 🔥 IA AJOUT SÉCURISÉ (IDENTIQUE)
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

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
    st.rerun()

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
sous_version = st.text_input("Sous-version")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1,13)))
    annee = st.number_input("Année", 1990, datetime.now().year, 2019)
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])

with col2:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"])

    techno = st.selectbox(
        "Technologie de boîte",
        [
            "-","DSG","EDC","CVT","BVA","BVM",
            "BVA6","BVA8","BVA9",
            "BVM6","BVM7",
            "7G-Tronic","9G-Tronic"
        ]
    )

    traction = st.selectbox(
        "Transmission",
        [
            "-","Traction","Propulsion","4x4",
            "4WD","4x4 permanent","4x4 enclenchable"
        ]
    )

etat = st.selectbox("État du véhicule", ["Bon état", "Excellent état"])
places = st.selectbox("Nombre de places", [2,3,4,5,6,7])
portes = st.selectbox("Nombre de portes", [1,2,3,4,5])
km = st.number_input("Kilométrage", 0, 400000, 90000)

departement = st.selectbox(
    "Département",
    ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
     "16","17","18","19","21","22","23","24","25","26","27","28","29","30","31",
     "32","33","34","35","36","37","38","39","40","41","42","43","44","45","46",
     "47","48","49","50","51","52","53","54","55","56","57","58","59","60","61",
     "62","63","64","65","66","67","68","69","70","71","72","73","74","75","76",
     "77","78","79","80","81","82","83","84","85","86","87","88","89","90","91",
     "92","93","94","95","971","972","973","974"]
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
    ]
)

commission = st.number_input("Commission (€)", 0, 10000, 1000)
commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

# ================= 🔥 CALCUL CORRIGÉ UNIQUEMENT =================

def calcul_cotation_realiste(marque, modele, annee, km, carburant, boite, finition, motorisation):

    age = datetime.now().year - annee
    base = 20000

    if marque.lower() in ["bmw","audi","mercedes","lexus"]:
        base *= 1.4
    elif marque.lower() in ["volkswagen","toyota"]:
        base *= 1.15
    elif marque.lower() in ["peugeot","renault","hyundai","kia"]:
        base *= 1.05
    elif marque.lower() in ["dacia","fiat","citroen"]:
        base *= 0.9

    if any(x in modele.lower() for x in ["q3","q5","x1","x3","3008","5008","tiguan","ix35","qashqai"]):
        base *= 1.30
    elif any(x in modele.lower() for x in ["208","clio","c3","yaris","polo"]):
        base *= 0.80

    base *= (0.94 ** age)

    if km < 50000:
        base *= 1.2
    elif km < 100000:
        base *= 1.05
    elif km < 150000:
        base *= 0.95
    elif km < 200000:
        base *= 0.85
    else:
        base *= 0.70

    if carburant == "Diesel":
        base *= 1.05
    elif carburant == "Hybride":
        base *= 1.15
    elif carburant == "Électrique":
        base *= 1.20

    if boite == "Automatique":
        base *= 1.08

    if any(x in finition.lower() for x in ["gt","amg","rs","m","sport"]):
        base *= 1.15
    if any(x in finition.lower() for x in ["business","access","trend"]):
        base *= 0.92

    if any(x in motorisation.lower() for x in ["150","180","200","220"]):
        base *= 1.1

    return int(base)

# ================= EXECUTION =================

if st.button("Calculer l'estimation"):

    prix_calcul = calcul_cotation_realiste(
        marque, modele, annee, km, carburant, boite, finition, motorisation
    )

    if model:
        try:
            prix_ia = int(model.predict([[annee, km]])[0])
            prix_calcul = int((prix_calcul * 0.6) + (prix_ia * 0.4))
        except:
            pass

    prix_annonces = [
        prix_calcul * 0.9,
        prix_calcul * 0.95,
        prix_calcul,
        prix_calcul * 1.05,
        prix_calcul * 1.1
    ]

    prix_marche = int(statistics.median(prix_annonces))

    coef_dep = 1.0
    if departement in ["75","92","93","94","91","77","78","95"]:
        coef_dep = 1.08
    elif departement in ["06","83"]:
        coef_dep = 1.07
    elif departement in ["69","33","31","34","44"]:
        coef_dep = 1.04
    elif departement in ["52","23","15","48","70","58"]:
        coef_dep = 0.92
    elif departement in ["59","62","08"]:
        coef_dep = 0.95

    prix_marche = int(prix_marche * coef_dep)

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

    annonce = f"""
🚗 {marque} {modele}
📅 {annee} | {km} km
⚙️ {motorisation} | {finition}

💰 Prix conseillé : {prix_marche} €
"""
    st.text_area("📋 Annonce prête à copier", annonce)

    contenu = f"""
ESTIMATION VELIORA

{marque} {modele}
{annee} - {km} km

Prix marché : {prix_marche} €
Net vendeur : {net_marche} €
"""

    b64 = base64.b64encode(contenu.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="estimation_veliora.txt">📄 Télécharger estimation</a>'
    st.markdown(href, unsafe_allow_html=True)
