import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os

SCRAPER_API_KEY = "sk_ad_6UkihaYMO3C3ukRwDVFVpjV2"

try:
    get_leboncoin_prices = None  # scraper désactivé
except:
    get_leboncoin_prices = None

try:
    import joblib
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/dhb2yglq1eta549enf7zaw83iltcdkrw"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"

PRICE_HT = 29
TVA = 0.20
PRICE_TTC = 34.80

STRIPE_LINK = "https://buy.stripe.com/00w7sM8UG4xn4TV5HO9fW07"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# 🔥 DATASET PREMIUM COMPLET
BASE_PRICES = {

    "toyota chr": 30000, "toyota chr 2023": 31000, "toyota chr 2024": 32000, "toyota chr 2025": 33000,
    "toyota yaris": 20000, "toyota yaris 2023": 22000, "toyota corolla": 28000,

    "peugeot 208": 18000, "peugeot 208 2022": 19000, "peugeot 208 2023": 20000,
    "peugeot 2008": 24000, "peugeot 3008": 32000,

    "renault clio": 17000, "renault clio 2022": 18000, "renault clio 2023": 19000,
    "renault captur": 23000, "renault megane": 26000,

    "ford focus": 18000,
    "ford focus 2020": 17500,

    # ✅ AJOUT IMPORTANT POUR ÉVITER LES PRIX FAUX
    "renault twingo": 11000,
    "renault twingo 2017": 10500,

    "dacia sandero": 14000, "dacia sandero 2023": 15000, "dacia duster": 22000,

    "bmw serie 1": 30000, "bmw serie 1 2022": 32000, "bmw serie 1 2023": 34000,
    "bmw x1": 31000,
    "bmw x1 2020": 32000,

    "mini countryman": 26000,
    "mini countryman 2019": 25000,

    "audi a3": 32000, "audi a3 2022": 34000, "audi a3 2023": 36000,
    "audi q3": 40000,
    "audi a4 2020": 33300,
    "audi a4": 33300,
    # ✅ CORRECTION AJOUTÉE
    "audi q5": 32000,
    "audi q5 2020": 30000,
    "audi q5 2021": 33000,
    "audi q5 2022": 36000,


    "mercedes classe a": 36000,
    "mercedes classe a 2020": 31000, "mercedes classe a 2015": 22000, "mercedes classe a 2022": 33000, "mercedes classe a 2023": 34000,
    "mercedes gla": 42000,

    "volkswagen golf 2019": 22000, "volkswagen golf 2022": 26000, "volkswagen golf 2023": 27000,
    "volkswagen tiguan 2020": 33000, "volkswagen tiguan 2022": 34700, "volkswagen tiguan 2023": 35700,
    "volkswagen t cross 2020": 22500,
    "volkswagen t cross": 22500,
    
    "renault zoe": 22000,
    "renault zoe 2021": 20000,

    "citroen c4": 18000,
    "citroen c4 2019": 16000,
    "citroen c4 cactus 2019": 17000,

    "kia rio": 16000,
    "kia rio 2020": 18000,

    "renault kadjar": 22000,
    "renault kadjar 2016": 17800,

    "fiat panda": 14000,
    "fiat panda 2018": 17500,

    "fiat 500": 11000,
    "fiat 500 2019": 10000,
    "fiat 500c": 10000,
    "fiat 500c 2019": 10000, "fiat 500c 2020": 10900, "fiat 500c 2021": 11700,
    # 🔥 AJOUT BASES MARCHÉ 2020 / 90000KM

    "nissan qashqai": 24000,
    "nissan qashqai 2021": 22000,

    "hyundai ix35": 13500,
    "hyundai ix35 2016": 11500, "hyundai ix35 2018": 12900, "hyundai ix35 2020": 14700,
    # 🔥 AJOUT BASES MARCHÉ 2020 / 90000KM
    "toyota yaris 2020": 13000,
    "toyota corolla 2020": 20000,

    "peugeot 2008 2020": 15000,
    "peugeot 3008 2020": 20200,
    "peugeot 5008 2020": 19000,

    "renault megane 2020": 17000,
    "renault grand scenic 2020": 21000,

    "volvo xc40 2020": 26000,
    "volvo xc60 2020": 35000,
    "volvo v60 2020": 26000,

}


def ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement=""):
    key = f"{marque} {modele}".lower()

    if any(x in key for x in ["clio","208","yaris","twingo","c1","107"]):
        base = 18000
    elif any(x in key for x in ["3008","5008","tiguan","qashqai"]):
        base = 28000
    elif any(x in key for x in ["audi","bmw","mercedes"]):
        base = 35000
    else:
        base = 22000

    age = max(0, datetime.now().year - annee)
    price = base

    if any(x in key for x in ["x","q","suv","3008","2008","tiguan"]):
        price *= 1.10
    elif any(x in key for x in ["clio","208","yaris","twingo","c1","107"]):
        price *= 0.75

    # 🔥 DÉCOTE RENFORCÉE SELON ÂGE
    price -= age * 1200

    if age > 5:
        price *= 0.75
    if age > 8:
        price *= 0.70
    if age > 10:
        price *= 0.60
    price -= (km / 1000) * 15

    if carburant == "Hybride":
        price *= 1.08
    elif carburant == "Électrique":
        price *= 1.10
    elif carburant == "Diesel":
        price *= 0.95

    if boite == "Automatique":
        price *= 1.03

    if motorisation:
        m = motorisation.lower()
        if any(x in m for x in ["90","100"]):
            price *= 0.95
        elif any(x in m for x in ["130","150"]):
            price *= 1.05
        elif any(x in m for x in ["180","200"]):
            price *= 1.08

    if finition:
        f = finition.lower()
        if any(x in f for x in ["life","access","business"]):
            price *= 0.95
        elif any(x in f for x in ["gt","sport","amg","s line"]):
            price *= 1.08

    return int(max(4000, min(price, 80000)))

def prix_psy(prix):
    if prix < 10000:
        return int(prix / 100) * 100 - 10
    elif prix < 20000:
        return int(prix / 100) * 100 - 10
    else:
        return int(prix / 1000) * 1000 - 10





def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    return df

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

def send_to_webhook(username, password, societe, siret):
    expire = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    data = {
        "username": username,
        "password": password,
        "societe": societe,
        "siret": siret,
        "expire": expire,
        "trial": True
    }

    try:
        requests.post(WEBHOOK_URL, json=data, timeout=10)
    except:
        pass

def clean_prices(prices):
    if len(prices) < 5:
        return prices

    prices = sorted(prices)
    median = statistics.median(prices)

    filtered = [
        p for p in prices
        if (median * 0.6) <= p <= (median * 1.4)
    ]

    if len(filtered) < 3:
        return prices

    return filtered

if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if "reset_id" not in st.session_state:
    st.session_state.reset_id = 0

if "historique" not in st.session_state:
    st.session_state.historique = []

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if st.session_state.admin_logged:
    st.session_state.logged = True

if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")

    st.warning("⚠️ Accès réservé aux professionnels de l’automobile")
    st.info(f"Après 3 jours d'essai : {PRICE_HT}€ HT ({PRICE_TTC}€ TTC) / an")

    st.markdown(f"[💳 S'abonner maintenant ({PRICE_TTC}€ TTC)]({STRIPE_LINK})")

    type_client = st.selectbox("Type d'utilisateur", ["Professionnel auto", "Particulier"])

    new_user = st.text_input("Créer un identifiant")
    new_pass = st.text_input("Créer un mot de passe", type="password")

    societe = st.text_input("Nom de la société")
    siret = st.text_input("Numéro SIRET")

    if st.button("Créer compte"):
        if type_client != "Professionnel auto":
            st.error("Accès réservé aux professionnels")
        elif not societe or not siret:
            st.error("SIRET obligatoire pour créer un compte")
        elif new_user and new_pass:
            send_to_webhook(new_user, new_pass, societe, siret)
            st.success("Compte professionnel créé")
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
            st.markdown(f"[💳 S'abonner ({PRICE_TTC}€ TTC)]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

    st.stop()

st.title("🚗 VELIORA COTATION PRO")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Nouvelle cotation (reset)"):
        st.session_state.reset_id += 1
        st.rerun()

col2a, col2b = st.columns(2)

with col2a:
    st.session_state.show_history = st.toggle("📊 Historique", value=st.session_state.show_history)

with col2b:
    buffer_hist = io.StringIO()
    buffer_hist.write("===== HISTORIQUE ESTIMATIONS =====\n\n")
    for item in st.session_state.historique:
        buffer_hist.write(f"{item['marque']} {item['modele']} {item['finition']}\n")
        buffer_hist.write(f"{item['motorisation']}\n")
        buffer_hist.write(f"{item['annee']} • {item['km']} km\n")
        buffer_hist.write(f"Prix : {item['prix']} €\n")
        buffer_hist.write(f"Date : {item['date']}\n")
        buffer_hist.write("-----------------------------\n")
    st.download_button("📥 Télécharger historique", buffer_hist.getvalue(), "historique.txt")



if st.session_state.show_history:
    st.subheader("📊 Historique des estimations")

    if len(st.session_state.historique) == 0:
        st.info("Aucune estimation pour le moment")
    else:
        for item in st.session_state.historique:
            st.markdown(f"""
**{item['marque']} {item['modele']} {item['finition']}**  
{item['motorisation']}  
{item['annee']} • {item['km']} km  
➡️ **{item['prix']} €**  
🕒 {item['date']}  

---
""")

if st.button("Se déconnecter"):
    st.session_state.logged = False
    st.session_state.admin_logged = False
    st.rerun()

rid = st.session_state.reset_id


# Lien Argus en haut
st.markdown("[📄 Voir fiche technique Argus](https://www.largus.fr/fiche-technique.html)")

rid = st.session_state.reset_id

col1, col2 = st.columns(2)
with col1:
    marque = st.text_input("Marque", key=f"marque_{rid}")
with col2:
    modele = st.text_input("Modèle", key=f"modele_{rid}")

col1, col2 = st.columns(2)
with col1:
    mois = st.text_input("Mois 1ère immatriculation (ex: 03)", key=f"mois_{rid}")
with col2:
    annee = st.number_input("Année", 1990, datetime.now().year, 2019, key=f"annee_{rid}")

col1, col2 = st.columns(2)
with col1:
    finition = st.text_input("Finition", key=f"finition_{rid}")
with col2:
    sous_version = st.text_input("Sous-version", key=f"sous_version_{rid}")

col1, col2 = st.columns(2)
with col1:
    motorisation = st.text_input("Motorisation", key=f"motorisation_{rid}")
with col2:
    carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique","GPL"], key=f"carburant_{rid}")

col1, col2 = st.columns(2)
with col1:
    boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key=f"boite_{rid}")
with col2:
    boite_tech = st.selectbox("Technologie boîte", ["", "BVA6","BVA7","BVA8","BVM5","BVM6"], key=f"boite_tech_{rid}")

col1, col2 = st.columns(2)
with col1:
    portes = st.text_input("Nombre de portes (ex: -, 0, 5)", key=f"portes_{rid}")
with col2:
    places = st.text_input("Nombre de places (ex: -, 0, 5)", key=f"places_{rid}")

col1, col2 = st.columns(2)
with col1:
    options = st.multiselect("Options", [
        "Caméra recul","Bip avant","Bip arrière",
        "Sièges chauffants avant","Sièges chauffants arrière",
        "Hayon électrique","Attelage","Toit panoramique"
    ], key=f"options_{rid}")
with col2:
    km = st.number_input("Kilométrage", 0, 400000, 0, key=f"km_{rid}")

departement = st.text_input("Département (ex: 08)", key=f"dep_{rid}")

col1, col2 = st.columns(2)
with col1:
    commission = st.number_input("Commission (€)", 0, 10000, 0, key=f"comm_{rid}")
with col2:
    commission_pct = st.number_input("Commission (%)", 0.0, 100.0, 0.0, key=f"comm_pct_{rid}")

if st.button("Calculer l'estimation"):

    prix_ai = ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement)

    prix_comparables = []

    if get_leboncoin_prices:
        try:
            query = f"{marque} {modele} {motorisation} {annee}"
            prix_comparables = get_leboncoin_prices(query, km, carburant, boite)
            st.info(f"Leboncoin PRO : {len(prix_comparables)} annonces")
        except:
            pass

    if len(prix_comparables) >= 5:

        prix_comparables = clean_prices(prix_comparables)

        median_price = statistics.median(prix_comparables)

        # 🔥 HYBRIDE PRO : on vérifie si le scraper est cohérent
        if (prix_ai * 0.75) < median_price < (prix_ai * 1.25):
            prix_marche = int((prix_ai * 0.75) + (median_price * 0.25))
        else:
            prix_marche = prix_ai

    else:
        prix_marche = prix_ai



    st.session_state.historique.insert(0, {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "marque": marque,
        "modele": modele,
        "finition": finition,
        "motorisation": motorisation,
        "annee": annee,
        "km": km,
        "prix": prix_psy(prix_marche)
    })

    st.session_state.historique = st.session_state.historique[:20]

    prix_vente = prix_psy(prix_marche)

    # 🔥 LOGIQUE PRIX COHÉRENTE PRO
    def arrondi_10(x):
        return int(round(x / 10) * 10)

    base = prix_vente

    # BAS
    prix_bas_min = arrondi_10(base * 0.90)
    prix_bas_max = base - 1

    # MARCHÉ
    prix_marche_min = base
    prix_marche_max = arrondi_10(base * 1.03)

    # HAUT
    prix_haut_min = prix_marche_max + 1
    prix_haut_max = arrondi_10(base * 1.10)

    if commission_pct > 0:
        commission_calc = prix_marche * (commission_pct / 100)
    else:
        commission_calc = commission

    net_marche = int(prix_marche - commission_calc)

    st.markdown("━━━━━━━━━━━━━━━━━━")
    st.markdown("### 💰 PRIX MARCHÉ MOYEN GARAGE")
    st.markdown(f"### {prix_vente} €  |  Net vendeur : {net_marche} €")
    st.caption(f"Prix marché estimé : {prix_marche} €")
    st.markdown("━━━━━━━━━━━━━━━━━━")
    st.markdown("---")
    st.markdown(f"📉 BAS : {prix_bas_min} € → {prix_bas_max} €")
    st.markdown(f"🎯 MARCHÉ : {prix_marche_min} € → {prix_marche_max} €")
    st.markdown(f"📈 HAUT : {prix_haut_min} € → {prix_haut_max} €")

    buffer = io.StringIO()
    buffer.write("===== ESTIMATION VÉHICULE =====\n")
    buffer.write(f"Marque : {marque}\n")
    buffer.write(f"Modèle : {modele}\n")
    buffer.write(f"Sous-version : {sous_version}\n")
    buffer.write(f"Finition : {finition}\n")
    buffer.write(f"Motorisation : {motorisation}\n")
    buffer.write(f"Année : {annee}\n")
    buffer.write(f"Kilométrage : {km} km\n")
    buffer.write(f"Carburant : {carburant}\n")
    buffer.write(f"Boîte : {boite}\n")
    buffer.write(f"\n===== PRIX =====\n")
    buffer.write(f"Prix affiché (vente) : {prix_vente} €\n")
    buffer.write(f"Prix bas : {prix_bas_min} € à {prix_bas_max} €\n")
    buffer.write(f"Prix marché : {prix_marche_min} € à {prix_marche_max} €\n")
    buffer.write(f"Prix haut : {prix_haut_min} € à {prix_haut_max} €\n")

