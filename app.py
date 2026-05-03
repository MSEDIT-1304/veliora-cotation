import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os
import unicodedata

SCRAPER_API_KEY = None


import json

LEARNING_FILE = "learning_data.json"

def load_learning_data():
    if os.path.exists(LEARNING_FILE):
        try:
            with open(LEARNING_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_learning_data(data):
    try:
        with open(LEARNING_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

LEARNING_DATA = {}


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












# 🔥 BASE MULTI-ANNÉES PRO
BASE_PRICES_V2 = {
    "hyundai i20": {2020:10959,2021:11800,2022:12700,2023:13600,2024:14500},
    "peugeot 208": {2020:10959,2021:11800,2022:12800,2023:13800,2024:14800},
    "renault clio": {2020:10959,2021:11700,2022:12600,2023:13500,2024:14500},
    "peugeot 3008": {2020:17500,2021:18900,2022:20500,2023:22500,2024:23500},
    "nissan qashqai": {2020:18500,2021:19800,2022:21500,2023:23000,2024:24000},
    "volkswagen golf": {2020:17592,2021:19000,2022:20500,2023:22000,2024:23000},

    "peugeot 2008": {
        2020:13266,
        2021:14500,
        2022:15800,
        2023:17000,
        2024:18000
    },
    "renault captur": {
        2020:13554,
        2021:14800,
        2022:16000,
        2023:17500,
        2024:18500
    },
    "citroen c1": {2020:8650,2021:9200,2022:9800,2023:10500,2024:11200},
    "volkswagen polo": {2020:12689,2021:13500,2022:14500,2023:15500,2024:16500},
    "ford kuga": {2020:17880,2021:19500,2022:21500,2023:22800,2024:24000},

    }

# DATASET 100+ MODELES SANS DOUBLONS
EXTRA_BASE_PRICES_V2 = {
    "peugeot 508": {2020: 18000, 2021: 19440, 2022: 20880, 2023: 22320, 2024: 23760},
    "renault espace": {2020: 20000, 2021: 21600, 2022: 23200, 2023: 24800, 2024: 26400},
    "citroen c5": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "ds7 crossback": {2020: 23000, 2021: 24840, 2022: 26679, 2023: 28520, 2024: 30360},
    "ds3 crossback": {2020: 17000, 2021: 18360, 2022: 19720, 2023: 21080, 2024: 22440},
    "toyota rav4": {2020: 24000, 2021: 25920, 2022: 27839, 2023: 29760, 2024: 31680},
    "toyota chr": {2020: 18000, 2021: 19440, 2022: 20880, 2023: 22320, 2024: 23760},
    "toyota aygo": {2020: 9000, 2021: 9720, 2022: 10440, 2023: 11160, 2024: 11880},
    "dacia sandero": {2020: 9000, 2021: 9720, 2022: 10440, 2023: 11160, 2024: 11880},
    "dacia duster": {2020: 14000, 2021: 15120, 2022: 16239, 2023: 17360, 2024: 18480},
    "dacia jogger": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "fiat 500": {2020: 10000, 2021: 10800, 2022: 11600, 2023: 12400, 2024: 13200},
    "fiat tipo": {2020: 12000, 2021: 12960, 2022: 13919, 2023: 14880, 2024: 15840},
    "fiat 500x": {2020: 14000, 2021: 15120, 2022: 16239, 2023: 17360, 2024: 18480},
    "jeep renegade": {2020: 16000, 2021: 17280, 2022: 18560, 2023: 19840, 2024: 21120},
    "jeep compass": {2020: 20000, 2021: 21600, 2022: 23200, 2023: 24800, 2024: 26400},
    "suzuki swift": {2020: 11000, 2021: 11880, 2022: 12760, 2023: 13640, 2024: 14520},
    "suzuki vitara": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "mitsubishi asx": {2020: 14000, 2021: 15120, 2022: 16239, 2023: 17360, 2024: 18480},
    "mitsubishi outlander": {2020: 20000, 2021: 21600, 2022: 23200, 2023: 24800, 2024: 26400},
    "alfa romeo giulietta": {2020: 13000, 2021: 14040, 2022: 15079, 2023: 16120, 2024: 17160},
    "alfa romeo stelvio": {2020: 25000, 2021: 27000, 2022: 28999, 2023: 31000, 2024: 33000},
    "land rover evoque": {2020: 28000, 2021: 30240, 2022: 32479, 2023: 34720, 2024: 36960},
    "land rover discovery sport": {2020: 30000, 2021: 32400, 2022: 34800, 2023: 37200, 2024: 39600},
    "porsche macan": {2020: 45000, 2021: 48600, 2022: 52200, 2023: 55800, 2024: 59400},
    "porsche cayenne": {2020: 60000, 2021: 64800, 2022: 69600, 2023: 74400, 2024: 79200},
    "tesla model s": {2020: 50000, 2021: 54000, 2022: 57999, 2023: 62000, 2024: 66000},
    "tesla model x": {2020: 60000, 2021: 64800, 2022: 69600, 2023: 74400, 2024: 79200},
    "cupra formentor": {2020: 28000, 2021: 30240, 2022: 32479, 2023: 34720, 2024: 36960},
    "cupra leon": {2020: 26000, 2021: 28080, 2022: 30159, 2023: 32240, 2024: 34320},
    "skoda enyaq": {2020: 30000, 2021: 32400, 2022: 34800, 2023: 37200, 2024: 39600},
    "volkswagen t-roc": {2020: 20000, 2021: 21600, 2022: 23200, 2023: 24800, 2024: 26400},
    "volkswagen t-cross": {2020: 16000, 2021: 17280, 2022: 18560, 2023: 19840, 2024: 21120},
    "volkswagen passat": {2020: 18000, 2021: 19440, 2022: 20880, 2023: 22320, 2024: 23760},
    "bmw serie 2": {2020: 22000, 2021: 23760, 2022: 25520, 2023: 27280, 2024: 29040},
    "bmw serie 4": {2020: 30000, 2021: 32400, 2022: 34800, 2023: 37200, 2024: 39600},
    "audi a4": {2020: 22000, 2021: 23760, 2022: 25520, 2023: 27280, 2024: 29040},
    "audi a5": {2020: 28000, 2021: 30240, 2022: 32479, 2023: 34720, 2024: 36960},
    "mercedes classe c": {2020: 23000, 2021: 24840, 2022: 26679, 2023: 28520, 2024: 30360},
    "mercedes gla": {2020: 22000, 2021: 23760, 2022: 25520, 2023: 27280, 2024: 29040},
    "mercedes glc": {2020: 30000, 2021: 32400, 2022: 34800, 2023: 37200, 2024: 39600},
    "volvo xc90": {2020: 40000, 2021: 43200, 2022: 46400, 2023: 49600, 2024: 52800},
    "volvo v40": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "volvo v90": {2020: 28000, 2021: 30240, 2022: 32479, 2023: 34720, 2024: 36960},
    "kia picanto": {2020: 9000, 2021: 9720, 2022: 10440, 2023: 11160, 2024: 11880},
    "kia rio": {2020: 11000, 2021: 11880, 2022: 12760, 2023: 13640, 2024: 14520},
    "hyundai i40": {2020: 14000, 2021: 15120, 2022: 16239, 2023: 17360, 2024: 18480},
    "hyundai veloster": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "nissan leaf": {2020: 15000, 2021: 16200, 2022: 17400, 2023: 18600, 2024: 19800},
    "nissan x-trail": {2020: 20000, 2021: 21600, 2022: 23200, 2023: 24800, 2024: 26400},
}


# 🔥 MERGE DATASET SANS DOUBLONS
for model, data in EXTRA_BASE_PRICES_V2.items():
    if model not in BASE_PRICES_V2:
        BASE_PRICES_V2[model] = data


# 🔥 KM ADJUST PRO (90k référence)
KM_ADJUST = {
    "i20":1500,
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
    2023: 0.22,
    2024: 0.10,
    2025: 0.12
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
    "x5": (0.20,0.28),"q7": (0.20,0.28)
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
    2019: -0.07, 2018: -0.14, 2017: -0.30,
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

    import unicodedata

    def norm(s):
        if not s:
            return ""
        return unicodedata.normalize('NFD', s.lower()).encode('ascii','ignore').decode('utf-8')

    marque = norm(marque)
    modele = norm(modele)
    finition = norm(finition)
    motorisation = norm(motorisation)

    key = f"{marque} {modele}".strip()

    # ======================
    # BASE (robuste)
    # ======================
    base = None

    # recherche flexible
    for m, years in BASE_PRICES_V2.items():
        if m == key or m in key:
            if annee in years:
                base = years[annee]
            else:
                closest = min(years.keys(), key=lambda x: abs(x - annee))
                base = years[closest]
            break

    if base is None:
        # fallback intelligent basé sur segment
        if any(x in key for x in ["bmw","audi","mercedes","porsche","tesla"]):
            base = 28000
        elif any(x in key for x in ["kuga","3008","qashqai","tucson","sportage"]):
            base = 22000
        elif any(x in key for x in ["clio","208","corsa","i20","polo"]):
            base = 12000
        else:
            base = 16000

    price = float(base)

    # ======================
    # KM (adouci)
    # ======================
    km_ref = 90000
    km_diff = km - km_ref
    km_adjust = - (km_diff / 10000) * 180
    km_adjust = max(min(km_adjust, 2500), -2500)
    price += km_adjust

    # ======================
    # MOTORISATION
    # ======================
    if any(x in motorisation for x in ["150","160","180"]):
        price *= 1.04
    elif any(x in motorisation for x in ["130","140"]):
        price *= 1.02
    elif any(x in motorisation for x in ["90","100"]):
        price *= 0.98

    # ======================
    # CARBURANT
    # ======================
    if carburant == "Diesel":
        price *= 1.02
    elif carburant == "Hybride":
        price *= 1.03
    elif carburant == "Électrique":
        price *= 1.06

    # ======================
    # BOITE
    # ======================
    if boite == "Automatique":
        price *= 1.025

    # ======================
    # FINITION
    # ======================
    if any(x in finition for x in ["base","life","access"]):
        price *= 0.96
    elif any(x in finition for x in ["gt","line","allure","intens","shine"]):
        price *= 1.06
    elif any(x in finition for x in ["amg","rs","m sport","s line","vignale"]):
        price *= 1.06

    # ======================
    # OPTIONS
    # ======================
    bonus = min(len(options) * 0.012, 0.10)
    price *= (1 + bonus)

    # ======================
    # TRANSMISSION
    # ======================
    if transmission in ["4x4","AWD","4WD"]:
        price *= 1.05

    # ======================
    # GEO
    # ======================
    if departement in ["75","92"]:
        price *= 1.04
    elif departement in ["13","69"]:
        price *= 1.02
    elif departement in ["08","23"]:
        price *= 0.97

    
    # ======================
    # PREMIUM BOOST
    # ======================
    if "porsche" in key or "land rover" in key:
        price *= 1.05
    elif any(x in key for x in ["bmw","audi","mercedes"]):
        price *= 1.03
    elif "tesla" in key:
        price *= 1.015

    
    # ======================
    # SPECIFIC FIX Q5 (cap marché)
    # ======================
    if "q5" in key:
        max_price = base * 1.03
        min_price = base * 0.95
        price = max(min_price, min(price, max_price))

    # ======================
    # CLAMP FINAL (stable)
    # ======================
    if any(x in key for x in ["kuga","3008","qashqai","tucson","sportage"]):
        min_price = base * 0.97
        max_price = base * 1.05
    else:
        min_price = base * 0.95
        max_price = base * 1.07

    price = max(min_price, min(price, max_price))

    return int(max(4000, min(price, 90000)))


    










def get_ai_estimation(marque, modele, annee, km, carburant, boite):
    base = ai_price_engine(marque, modele, "", "", annee, km, carburant, boite)
    low = int(base * 0.98)
    high = int(base * 1.02)
    return low, high

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
    st.session_state.show_ia = False
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
    if st.button("🔎 Voir estimation IA (beta)"):
        st.session_state.show_ia = True

    if st.session_state.get("show_ia", False):
        last = st.session_state.historique[0]
        low, high = get_ai_estimation(
            last["marque"],
            last["modele"],
            last["annee"],
            last["km"],
            carburant,
            boite
        )
        st.info(f"Estimation IA marché pro : {low} € – {high} €")

# ===== AFFICHAGE STABLE (hors bouton) =====
if "resultat" in st.session_state:
    r = st.session_state.resultat

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 💰 PRIX MARCHÉ")
        st.markdown(f"Prix marché estimé : {r['prix_marche_estime']} €")
        st.markdown(f"📉 BAS : {r['prix_bas_min']} € → {r['prix_bas_max']} €")
        st.markdown(f"📈 HAUT : {r['prix_haut_min']} € → {r['prix_haut_max']} €")

    with col_right:
        st.markdown("### 🧮 Calculateur")
        prix_choisi = st.number_input("Prix choisi", value=0)
        commission_user = st.number_input("Commission (€)", value=0)
        commission_pct_user = st.number_input("Commission (%)", 0.0, 100.0, 0.0)

        if commission_pct_user > 0:
            commission_calc_user = round(prix_choisi * (commission_pct_user / 100))
        else:
            commission_calc_user = commission_user

        net_calc = prix_choisi - commission_calc_user
        net_calc = int(round(net_calc / 10) * 10)

        st.success(f"💶 Net vendeur : {net_calc} €")


