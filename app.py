
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

WEBHOOK_URL = "https://hook.eu1.make.com/942mf8fk2jehv637xc3s0tsjsxrad0gu"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"

PRICE_HT = 29
TVA = 0.20
PRICE_TTC = 34.80

STRIPE_LINK = "https://buy.stripe.com/00w7sM8UG4xn4TV5HO9fW07"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# 🔥 DATASET PREMIUM COMPLET
BASE_PRICES = {

    # 2020 / 90 000 km base marché PRO (médiane)

    "renault megane 2020": 11536,
    "peugeot 208 2020": 10959,
    "peugeot 2008 2020": 13266,
    "peugeot 3008 2020": 17500,
    "peugeot 5008 2020": 18500,
    "toyota yaris 2020": 12112,
    "toyota corolla 2020": 16727,
    "volvo xc40 2020": 21918,
    "volvo xc60 2020": 25379,
    "volvo v60 2020": 20764,
    "hyundai i20 2020": 10959,
    "volkswagen polo 2020": 12689,
    "hyundai tucson 2020": 19500,
    "hyundai ix35 2016": 10382,
    "kia sportage 2020": 19000,
    "audi q3 2020": 20000,
    "audi q5 2020": 26000,
    "audi q7 2020": 35000,
    "bmw x1 2020": 20000,
    "bmw x3 2020": 24000,
    "bmw x5 2020": 33000,
    "bmw serie 1 2020": 17000,
    "bmw serie 3 2020": 21000,
    "audi a1 2020": 14000,
    "audi a3 2020": 17000,
    "mercedes classe a 2020": 20000,
    "mercedes classe b 2020": 18000,
    "mini cooper 2020": 18746,
    "opel corsa 2020": 10382,
    "opel grandland 2020": 15862,
    "opel grandland x 2020": 15285,

    
    # 🔥 AJOUT LISTE UTILISATEUR (médianes 2020 / 90 000 km)
    "renault clio v 2020": 10959,
    "renault captur ii 2020": 13554,
    "renault kadjar 2020": 15285,
    "peugeot 308 2020": 12978,
    "citroen c3 2020": 10382,
    "citroen c5 aircross 2020": 17304,
    "volkswagen golf 8 2020": 17592,
    "volkswagen tiguan 2020": 22500,
    "seat leon 2020": 13554,
    "seat ateca 2020": 19000,
    "skoda octavia 2020": 14708,
    "skoda karoq 2020": 19000,
    "ford fiesta 2020": 10382,
    "ford focus 2020": 12978,
    "ford kuga 2020": 17880,
    "nissan qashqai 2020": 18500,
    "nissan juke 2020": 13554,
    "mazda cx-30 2020": 18457,
    "mazda 3 2020": 15862,
    "honda civic 2020": 16438,
    "honda cr-v 2020": 22495,
    "kia ceed 2020": 13554,
    "kia xceed 2020": 15862,

    
    # 🔥 NOUVEAUX MODELES AJOUTÉS (médianes)
    "hyundai i10 2020": 9228,
    "hyundai i30 2020": 13266,
    "hyundai kona 2020": 15862,
    "hyundai santa fe 2020": 27974,
    "hyundai ioniq 2020": 17592,
    "hyundai bayon 2020": 14708,
    "renault megane 5 2020": 11536,
    "renault koleos 2020": 21053,
    "renault talisman 2020": 14131,
    "renault scenic 4 2020": 13554,
    "renault grand scenic 2020": 14708,
    "renault arkana 2020": 17880,
    "renault twingo 3 2020": 9228,
    "seat ibiza 2020": 11536,
    "seat leon 2020": 16150,
    "seat arona 2020": 13554,
    "seat ateca 2020": 18457,
    "seat tarraco 2020": 23360,
    "citroen c1 2020": 8652,
    "citroen c3 2020": 10382,
    "citroen c3 aircross 2020": 12689,
    "citroen c4 2020": 13843,
    "citroen c5 aircross 2020": 17015,

    
    # 🔥 SKODA AJOUT (corrigé +12%)
    "skoda fabia 2020": 10959,
    "skoda scala 2020": 12689,
    "skoda octavia 2020": 14420,
    "skoda kamiq 2020": 13843,
    "skoda karoq 2020": 14996,
    "skoda kodiaq 2020": 21341,
    "skoda superb 2020": 17880,

    # fallback générique
    "renault megane": 27686,
    "peugeot 208": 19611,
    "peugeot 2008": 25379,
    "peugeot 3008": 34608,
    "peugeot 5008": 32300,
    "toyota yaris": 20764,
    "toyota corolla": 25379,
    "volvo xc40": 46144,
    "volvo xc60": 57680,
    "volvo v60": 48451,
    "hyundai i20": 18457,
    "hyundai i20 2023": 12000,
    "volkswagen polo": 20764,
    "hyundai tucson": 34608,
    "kia sportage": 32300,
    "audi q3": 43836,
    "audi q5": 57680,
    "audi q7": 80752,
    "bmw x1": 39222,
    "bmw x3": 57680,
    "bmw x5": 86520,
    "bmw serie 1": 36915,
    "bmw serie 3": 48451,
    "audi a1": 28840,
    "audi a3": 38068,
    "mercedes classe a": 38068,
    "mercedes classe b": 32300,
    "mini cooper": 32300,
    "opel corsa": 17304,
    "opel grandland": 29993,
    "opel grandland x": 28840
}











# 🔥 KM ADJUST PRO (90k référence)
    "i20":1100,
KM_ADJUST = {
    "twingo":1500,"c1":1500,"i10":1500,"corsa":1500,"fiesta":1500,"clio":1500,"208":1500,
    "polo":1500,"ibiza":1500,"megane":1500,
    "308":2000,"focus":2000,"ceed":2000,"i30":2000,"2008":2000,
    "3008":2500,"5008":2500,"qashqai":2500,"karoq":2500,"ateca":2500,"golf":2500,
    "x1":2500,"xc40":2500,
    "tucson":3000,"sportage":3000,"kuga":3000,"c5 aircross":3000,
    "a3":3000,"serie 1":3000,
    "classe a":3500,"serie 3":3500,"x3":3500,"q5":3500,
    "xc60":4000,
    "x5":5500,"q7":5500
}





# 🔥 GLOBAL YEAR ADJUST (PRO 2025)
GLOBAL_YEAR = {
    2021: 0.08,
    2022: 0.12,
    2023: 0.05,
    2024: 0.10,
    2025: 0.20
}

# 🔥 YEAR ADJUST PRO (base 2020)
YEAR_ADJUST = {
    "x5": {"2019": -0.10, "2021": 0.15, "2023": 0.36},
    "q7": {"2019": -0.10, "2021": 0.15, "2023": 0.36},

    "corsa": {"2019": -0.09, "2021": 0.17, "2023": 0.40},
    "clio": {"2019": -0.09, "2021": 0.17, "2023": 0.40},
    "208": {"2019": -0.09, "2021": 0.17, "2023": 0.40},

    "3008": {"2019": -0.08, "2021": 0.19, "2023": 0.42},
    "5008": {"2019": -0.08, "2021": 0.19, "2023": 0.42},

    "x3": {"2019": -0.11, "2021": 0.17, "2023": 0.42},
    "q5": {"2019": -0.11, "2021": 0.17, "2023": 0.42},

    "c1": {"2019": -0.10, "2021": 0.15, "2023": 0.44},
    "i10": {"2019": -0.10, "2021": 0.15, "2023": 0.44},
    "twingo": {"2019": -0.10, "2021": 0.15, "2023": 0.44},
}




# 🔥 FINITION ADJUST PRO
FINITION_ADJUST = {
    "c1": (0.12,0.18),"i10": (0.12,0.18),"twingo": (0.12,0.18),

    "corsa": (0.15,0.22),"fiesta": (0.15,0.22),"c3": (0.15,0.22),"clio": (0.15,0.22),
    "208": (0.15,0.22),"i20": (0.15,0.22),"ibiza": (0.15,0.22),"polo": (0.15,0.22),

    "megane": (0.18,0.25),"308": (0.18,0.25),"focus": (0.18,0.25),
    "ceed": (0.18,0.25),"i30": (0.18,0.25),"golf": (0.18,0.25),

    "3008": (0.20,0.30),"5008": (0.22,0.32),"qashqai": (0.20,0.30),
    "tucson": (0.20,0.30),"sportage": (0.20,0.30),

    "a3": (0.18,0.28),"serie 1": (0.18,0.28),"classe a": (0.18,0.28),

    "serie 3": (0.20,0.30),"x3": (0.25,0.35),"q5": (0.25,0.35),
    "x5": (0.30,0.45),"q7": (0.30,0.45)
}




# 🔥 OPTIONS LUXE ADJUST PRO
OPTIONS_ADJUST = {
    "toit panoramique": (0.05,0.10),
    "sieges chauffants": (0.03,0.06),
    "sieges electriques": (0.04,0.08),
    "cuir": (0.06,0.12),
    "gps": (0.04,0.08),
    "camera recul": (0.02,0.04),
    "camera 360": (0.04,0.07),
    "adas": (0.05,0.10),
    "regulateur adaptatif": (0.04,0.08),
    "audio premium": (0.03,0.06),
    "jantes": (0.02,0.05),
    "keyless": (0.03,0.06),
    "hayon electrique": (0.03,0.06),
    "sieges ventiles": (0.04,0.07),
    "hud": (0.03,0.06),
    "suspension pilotee": (0.05,0.10)
}




# 🔥 OPTIONS YEAR ADJUST PRO
OPTIONS_YEAR = {
    "toit panoramique": {"2019":0.04,"2021":0.07,"2023":0.10},
    "sieges chauffants": {"2019":0.02,"2021":0.04,"2023":0.06},
    "sieges electriques": {"2019":0.03,"2021":0.05,"2023":0.08},
    "cuir": {"2019":0.05,"2021":0.08,"2023":0.12},
    "gps": {"2019":0.03,"2021":0.06,"2023":0.09},
    "camera recul": {"2019":0.01,"2021":0.03,"2023":0.04},
    "camera 360": {"2019":0.03,"2021":0.05,"2023":0.07},
    "adas": {"2019":0.04,"2021":0.07,"2023":0.10},
    "regulateur adaptatif": {"2019":0.03,"2021":0.06,"2023":0.09},
    "audio premium": {"2019":0.02,"2021":0.04,"2023":0.06},
    "jantes": {"2019":0.01,"2021":0.03,"2023":0.05},
    "keyless": {"2019":0.02,"2021":0.04,"2023":0.06},
    "hayon electrique": {"2019":0.02,"2021":0.04,"2023":0.06},
    "sieges ventiles": {"2019":0.03,"2021":0.05,"2023":0.07},
    "hud": {"2019":0.02,"2021":0.04,"2023":0.06},
    "suspension pilotee": {"2019":0.04,"2021":0.07,"2023":0.10}
}












# 🔥 AWD / 4x4 ADJUST PRO
AWD_ADJUST = {
    "citadine": (0.08,0.15),
    "compacte": (0.06,0.12),
    "suv": (0.07,0.15),
    "premium": (0.08,0.12),
    "electrique": (0.10,0.20)
}

# 🔥 GEO ADJUST (DEPARTEMENT)
GEO_ADJUST = {
    "75": {"citadine":0.12,"compacte":0.12,"suv":0.14,"premium":0.18,"electrique":0.20},
    "92": {"citadine":0.10,"compacte":0.10,"suv":0.12,"premium":0.16,"electrique":0.18},
    "69": {"citadine":0.06,"compacte":0.07,"suv":0.09,"premium":0.12,"electrique":0.14},
    "13": {"citadine":0.06,"compacte":0.07,"suv":0.09,"premium":0.12,"electrique":0.15},
    "33": {"citadine":0.05,"compacte":0.06,"suv":0.08,"premium":0.10,"electrique":0.13},
    "44": {"citadine":0.04,"compacte":0.05,"suv":0.07,"premium":0.09,"electrique":0.11},
    "01": {"citadine":0.03,"compacte":0.04,"suv":0.06,"premium":0.08,"electrique":0.10},
    "08": {"citadine":-0.05,"compacte":-0.05,"suv":-0.07,"premium":-0.09,"electrique":-0.10},
    "23": {"citadine":-0.08,"compacte":-0.07,"suv":-0.09,"premium":-0.12,"electrique":-0.15}
}

# 🔥 DEPRECIATION YEARS < 2020
DEPRECIATION_THERMIQUE = {
    2019: -0.07, 2018: -0.14, 2017: -0.20,
    2016: -0.27, 2015: -0.35, 2014: -0.42
}

DEPRECIATION_ELECTRIC = {
    2019: -0.10, 2018: -0.18, 2017: -0.28,
    2016: -0.38, 2015: -0.48, 2014: -0.55
}

# 🔥 ELECTRIC VEHICLES DATASET (BASE PRIX PAR ANNEE)
ELECTRIC_BASE = {
    "tesla model 3": {"2019":24000,"2020":27000,"2021":29000,"2022":31000,"2023":30000,"2024":27000,"2025":25000},
    "tesla model y": {"2021":38000,"2022":40000,"2023":38000,"2024":34000,"2025":30000},
    "mg4": {"2022":22000,"2023":21000,"2024":19000,"2025":17000},
    "mg zs ev": {"2019":16000,"2020":18000,"2021":19000,"2022":20000,"2023":19000,"2024":17000,"2025":15000},
    "zoe": {"2019":12000,"2020":14000,"2021":15000,"2022":16000,"2023":15000,"2024":13000,"2025":11000},
    "e-208": {"2020":17000,"2021":19000,"2022":20000,"2023":19000,"2024":17000,"2025":15000},
    "id.3": {"2020":22000,"2021":24000,"2022":25000,"2023":24000,"2024":21000,"2025":18000},
    "kona ev": {"2019":20000,"2020":22000,"2021":24000,"2022":25000,"2023":24000,"2024":22000,"2025":20000},
    "e-niro": {"2019":21000,"2020":23000,"2021":25000,"2022":26000,"2023":25000,"2024":23000,"2025":21000}
}

# 🔥 ESSENCE vs DIESEL ADJUST PRO
FUEL_ADJUST = {
    "corsa": 0.03,"fiesta": 0.03,"c3": 0.03,"fabia": 0.03,"clio": 0.03,"208": 0.03,"i20": 0.03,"ibiza": 0.03,
    "megane": 0.05,"308": 0.05,"polo": 0.04,"scala": 0.04,"c3 aircross": 0.05,"2008": 0.05,"captur": 0.05,
    "arona": 0.04,"kamiq": 0.04,"juke": 0.05,
    "3008": 0.06,"grandland": 0.06,"octavia": 0.05,"kona": 0.05,"xceed": 0.05,
    "qashqai": 0.06,"karoq": 0.06,"5008": 0.07,"sportage": 0.06,"golf": 0.05,
    "tucson": 0.06,"ateca": 0.06,"kuga": 0.06,"superb": 0.06,"arkana": 0.05,"cx-30": 0.05,
    "c5 aircross": 0.06,
    "a1": 0.04,"a3": 0.05,"serie 1": 0.06,"classe a": 0.05,"classe b": 0.05,
    "serie 3": 0.06,"v60": 0.06,"x1": 0.06,"xc40": 0.06,"q3": 0.06,
    "xc60": 0.07,"x3": 0.07,"q5": 0.07,
    "koleos": 0.07,"kodiaq": 0.07,"cr-v": 0.07,"tarraco": 0.07,"santa fe": 0.07,
    "x5": 0.08,"q7": 0.08
}


def ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement="", options=None, transmission=None):

    if options is None:
        options = []

    key = f"{marque} {modele}".lower()
    key_full = f"{marque} {modele} {annee}".lower()

    # BASE DATASET
    # 🔥 ELECTRIC OVERRIDE
    base = None

    for k,v in ELECTRIC_BASE.items():
        if k in key:
            year_key = str(annee)
            if year_key in v:
                base = v[year_key]
                break

    if base is None:
        for k, v in BASE_PRICES.items():
            if all(word in key_full for word in k.split()):
                base = v
                break

    if base is None:
        if any(x in key for x in ["mercedes","bmw","audi"]):
            base = 30000
        elif any(x in key for x in ["3008","qashqai","tiguan","kadjar","ix35"]):
            base = 20000
        else:
            base = 15000

    price = base

    # 🔥 BOOST MARCHÉ SUV
    if any(x in key for x in ["3008","5008","tiguan","qashqai","karoq","ateca","tucson","sportage"]):
        price *= 1.05

    # 🔥 YEAR PRO PAR MODELE
    year_adjust = 0
    for k,v in YEAR_ADJUST.items():
        if k in key:
            if str(annee) in v:
                year_adjust = v[str(annee)]
            break

    if year_adjust != 0:
        price *= (1 + year_adjust)
    elif annee in GLOBAL_YEAR:
        price *= (1 + GLOBAL_YEAR[annee])

    # 🔥 DEPRECIATION PRE 2020
    if annee < 2020:
        if carburant == "Électrique":
            if annee in DEPRECIATION_ELECTRIC:
                price *= (1 + DEPRECIATION_ELECTRIC[annee])
        else:
            if annee in DEPRECIATION_THERMIQUE:
                price *= (1 + DEPRECIATION_THERMIQUE[annee])


    # KM
    # 🔥 ELECTRIC KM SPECIFIC
    if carburant == "Électrique":
        if km <= 60000:
            price *= 1.12
        elif km >= 120000:
            price *= 0.85

    # 🔥 KM PRO PAR MODELE

    if annee >= 2024:
        price *= 1.05
    if km < 10000 and annee >= 2022:
        price *= 1.12
    km_ref = 90000
    delta_km = km - km_ref

    adjust = 2000
    for k,v in KM_ADJUST.items():
        if k in key:
            adjust = v
            break

    price -= (delta_km / 30000) * adjust

    # 🔥 CARBURANT PRO PAR MODELE
    if carburant == "Diesel":
        diesel_bonus = 0
        for k,v in FUEL_ADJUST.items():
            if k in key:
                diesel_bonus = v
                break
        price *= (1 + diesel_bonus)

    elif carburant == "Hybride":
        price *= 1.02

    elif carburant == "Électrique":
        price *= 1.03

    # BOITE
    if boite == "Automatique":
        price *= 1.02

    # 🔥 FINITION PRO PAR MODELE
    f = finition.lower() if finition else ""
    if finition:
        f = finition.lower()

        min_adj, max_adj = (0.15,0.25)

        for k,v in FINITION_ADJUST.items():
            if k in key:
                min_adj, max_adj = v
                break

        if any(x in f for x in ["access","life","business","trend","base"]):
            price *= (1 - min_adj)

        elif any(x in f for x in ["gt","sport","line","plus","tech","style","carat","intens","allure","shine"]):
            price *= (1 + (min_adj/2))

        elif any(x in f for x in ["amg","m sport","rs","s line","exclusive","luxe"]):
            price *= (1 + max_adj)

        # 🔥 BOOST finition SUV premium
    if any(x in key for x in ["3008","tiguan","qashqai","tucson","sportage"]) and any(x in f for x in ["carat","gt","allure","intens","shine"]):
        price *= 1.03

        # 🔥 OPTIONS PRO
    if carburant == "Électrique":
        for opt in options:
            o = opt.lower()
            if "autonomie" in o:
                price *= 1.15
            if "awd" in o or "dual" in o:
                price *= 1.12
            if "autopilot" in o:
                price *= 1.08
            if "pompe" in o:
                price *= 1.05
            if "premium" in o:
                price *= 1.08

    total_option_bonus = 0

    if options:
        for opt in options:
            o = opt.lower()
            for k,v in OPTIONS_ADJUST.items():
                if k in o:
                    year_key = str(annee)
                    if k in OPTIONS_YEAR and year_key in OPTIONS_YEAR[k]:
                        total_option_bonus += OPTIONS_YEAR[k][year_key]
                    else:
                        total_option_bonus += v[0]

        # plafonnement
        total_option_bonus = min(total_option_bonus, 0.40)

        price *= (1 + total_option_bonus)

    # 🔥 AWD / 4x4 PRO (manuel)
    if transmission in ["4x4","AWD","4WD"]:
        type_cat = "citadine"
        if any(x in key for x in ["3008","qashqai","tucson","sportage","x1","x3","q5"]):
            type_cat = "suv"
        if any(x in key for x in ["bmw","audi","mercedes","volvo"]):
            type_cat = "premium"
        if carburant == "Électrique":
            type_cat = "electrique"

        min_awd, max_awd = AWD_ADJUST.get(type_cat,(0.07,0.12))
        price *= (1 + (min_awd + max_awd)/2)

    # 🔥 GEO AJUSTEMENT
    type_cat = "citadine"
    if any(x in key for x in ["3008","qashqai","tucson","sportage","x1","x3","q5"]):
        type_cat = "suv"
    if any(x in key for x in ["bmw","audi","mercedes","volvo"]):
        type_cat = "premium"
    if carburant == "Électrique":
        type_cat = "electrique"

    if departement in GEO_ADJUST:
        geo_bonus = GEO_ADJUST[departement].get(type_cat,0)
        price *= (1 + geo_bonus)

    # VERROUILLAGE
    price = max(base * 0.60, min(price, base * 1.60))

    if price > base * 1.8:
        price = base * 1.8

    return int(max(4000, min(price, 80000)))








def prix_psy(prix):
    return int(prix / 100) * 100 - 10





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

    st.markdown("### 👤 Accès professionnel uniquement")
    type_client = "Professionnel auto"
    st.success("Compte professionnel requis")

    email = st.text_input("Adresse email")
    new_user = email
    new_pass = st.text_input("Créer un mot de passe", type="password")

    societe = st.text_input("Nom de la société")
    siret = st.text_input("Numéro SIRET")

    if st.button("Créer compte"):
        if not societe or not siret:
            st.error("SIRET obligatoire pour créer un compte")
        elif new_user and new_pass:
            send_to_webhook(new_user, new_pass, societe, siret)
            st.session_state["temp_user"] = new_user.strip()
            st.session_state["temp_pass"] = new_pass.strip()
            st.success("Compte professionnel créé (connexion immédiate possible)")
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

        # priorité utilisateur fraîchement créé
        if "temp_user" in st.session_state and user.strip() == st.session_state["temp_user"] and pwd.strip() == st.session_state["temp_pass"]:
            st.session_state.logged = True
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

transmission = st.selectbox("Transmission", ["4x2","Traction","Propulsion","4x4","AWD","4WD"], key=f"trans_{rid}")

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

    prix_ai = ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement, options, transmission)

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

    # 🔥 LOGIQUE PRIX COHÉRENTE FIXÉE (stable)

    def arrondi_10(x):
        return int(round(x / 10) * 10)

    base = prix_marche
    base = int(round(base / 100) * 100)

    # BAS
    prix_bas_min = arrondi_10(base * 0.88)
    prix_bas_max = arrondi_10(base * 0.94)

    # MARCHÉ (plage cohérente fixe)
    prix_marche_min = arrondi_10(base * 0.95)
    prix_marche_max = arrondi_10(base * 1.05)

    # HAUT
    prix_haut_min = prix_marche_max + 1
    prix_haut_max = arrondi_10(base * 1.12)

    # 🔥 CORRECTION % + NET VENDEUR JUSTE

    if commission_pct > 0:
        commission_calc = round(prix_vente * (commission_pct / 100))
    else:
        commission_calc = commission

    net_marche = prix_vente - commission_calc

    # arrondi cohérent (comme prix affiché)
    net_marche = int(round(net_marche / 10) * 10)

    # sécurité si 0 commission
    if commission == 0 and commission_pct == 0:
        net_marche = prix_vente

    st.markdown("━━━━━━━━━━━━━━━━━━")
    st.markdown("### 💰 PRIX MARCHÉ MOYEN GARAGE")
    st.markdown(f"### {prix_vente} €  |  Net vendeur : {net_marche} €")
    st.caption(f"Prix marché estimé : {prix_marche} €")
    st.markdown("━━━━━━━━━━━━━━━━━━")
    st.markdown("---")
    st.markdown(f"📉 BAS : {prix_bas_min} € → {prix_bas_max} €")
    st.markdown(f"🎯 MARCHÉ : {prix_marche_min} € → {prix_marche_max} €")
    st.markdown(f"📈 HAUT : {prix_haut_min} € → {prix_haut_max} €")

    # 🔥 STOCKAGE RESULTAT (pour éviter reset)
    st.session_state.resultat = {
        "prix_vente": prix_vente,
        "net_marche": net_marche,
        "prix_bas_min": prix_bas_min,
        "prix_bas_max": prix_bas_max,
        "prix_marche_min": prix_marche_min,
        "prix_marche_max": prix_marche_max,
        "prix_haut_min": prix_haut_min,
        "prix_haut_max": prix_haut_max
    }


    

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



# ===== AFFICHAGE STABLE (hors bouton) =====
if "resultat" in st.session_state:
    r = st.session_state.resultat

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 💰 PRIX MARCHÉ MOYEN GARAGE")
        st.markdown(f"### {r['prix_vente']} €  |  Net vendeur : {r['net_marche']} €")
        st.markdown(f"📉 BAS : {r['prix_bas_min']} € → {r['prix_bas_max']} €")
        st.markdown(f"🎯 MARCHÉ : {r['prix_marche_min']} € → {r['prix_marche_max']} €")
        st.markdown(f"📈 HAUT : {r['prix_haut_min']} € → {r['prix_haut_max']} €")

    with col_right:
        st.markdown("### 🧮 Calculateur")
        prix_choisi = st.number_input("Prix choisi", value=r["prix_vente"])
        commission_user = st.number_input("Commission (€)", value=0)
        commission_pct_user = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

        if commission_pct_user > 0:
            commission_calc_user = round(prix_choisi * (commission_pct_user / 100))
        else:
            commission_calc_user = commission_user

        net_calc = prix_choisi - commission_calc_user
        net_calc = int(round(net_calc / 10) * 10)

        st.success(f"💶 Net vendeur : {net_calc} €")


