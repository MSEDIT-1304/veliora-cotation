# ===============================
# VERSION STABLE VENDABLE
# ===============================

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import io
import os
import unicodedata
import json

SCRAPER_API_KEY = None

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

# ===============================
# DATASET CONSERVÉ (inchangé)
# ===============================
BASE_PRICES_V2 = {
    "peugeot 208": {2020:11800,2021:12800,2022:13800,2023:14800,2024:15800},
    "renault clio": {2020:11700,2021:12600,2022:13500,2023:14500,2024:15500},
    "peugeot 3008": {2020:18900,2021:20500,2022:22500,2023:23500,2024:24500},
    "nissan qashqai": {2020:19800,2021:21500,2022:23000,2023:24000,2024:25000},
    "volkswagen golf": {2020:19000,2021:20500,2022:22000,2023:23000,2024:24000},
    "audi q5": {2020:27000,2021:29000,2022:31000,2023:33000,2024:35000}
}

# ===============================
# 🔥 NOUVEAU MOTEUR STABLE
# ===============================
def ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement="", options=None, transmission=None):

    if options is None:
        options = []

    def norm(s):
        return unicodedata.normalize('NFD', str(s).lower()).encode('ascii','ignore').decode('utf-8')

    marque = norm(marque)
    modele = norm(modele)
    finition = norm(finition)
    motorisation = norm(motorisation)

    key = f"{marque} {modele}"

    # ======================
    # BASE FIABLE
    # ======================
    base = None
    for m, years in BASE_PRICES_V2.items():
        if m in key:
            if annee in years:
                base = years[annee]
            else:
                closest = min(years.keys(), key=lambda x: abs(x - annee))
                base = years[closest]
            break

    if base is None:
        base = 16000

    # ======================
    # COEF GLOBAL (STABLE)
    # ======================
    coef = 1.0

    # KM
    km_delta = (km - 90000) / 100000
    km_delta = max(min(km_delta, 0.03), -0.03)
    coef -= km_delta

    # MOTORISATION
    if "150" in motorisation or "180" in motorisation:
        coef += 0.02
    elif "130" in motorisation:
        coef += 0.01
    elif "90" in motorisation:
        coef -= 0.015

    # CARBURANT
    if carburant == "Diesel":
        coef += 0.01
    elif carburant == "Hybride":
        coef += 0.015
    elif carburant == "Électrique":
        coef += 0.02

    # BOITE
    if boite == "Automatique":
        coef += 0.015

    # FINITION
    if "gt" in finition or "line" in finition:
        coef += 0.025
    elif "amg" in finition or "s line" in finition:
        coef += 0.03
    elif "base" in finition:
        coef -= 0.02

    # OPTIONS
    coef += min(len(options) * 0.008, 0.05)

    # GEO
    if departement in ["75","92"]:
        coef += 0.02
    elif departement in ["08","23"]:
        coef -= 0.015

    # PREMIUM
    if any(x in key for x in ["audi","bmw","mercedes"]):
        coef += 0.015

    # ======================
    # PRIX FINAL
    # ======================
    price = base * coef

    # ======================
    # CLAMP ULTRA STABLE
    # ======================
    min_price = base * 0.97
    max_price = base * 1.03

    price = max(min_price, min(price, max_price))

    return int(max(4000, min(price, 90000)))

# ===============================
# UI STREAMLIT (INCHANGÉ)
# ===============================
st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
annee = st.number_input("Année", 1990, 2025, 2020)
km = st.number_input("KM", 0, 400000, 90000)
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")
carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
boite = st.selectbox("Boîte", ["Manuelle","Automatique"])
options = st.multiselect("Options", ["GPS","Cuir","Camera"])

if st.button("Calculer"):
    prix = ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, "", options)

    st.success(f"💰 Prix marché estimé : {prix} €")
