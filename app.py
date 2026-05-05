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
    "a1": {2025: 19000, 2024: 17500, 2023: 15500, 2022: 14000, 2021: 13000, 2020: 11500, 2019: 10500, 2018: 9500, 2017: 8500, 2016: 7500, 2015: 7000, 2014: 6500},
    "a3": {2025: 24000, 2024: 22500, 2023: 20500, 2022: 18500, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "a4": {2025: 30000, 2024: 27000, 2023: 24000, 2022: 22000, 2021: 20000, 2020: 18000, 2019: 16500, 2018: 15000, 2017: 13500, 2016: 12000, 2015: 11000, 2014: 10000},
    "a6": {2025: 40000, 2024: 37000, 2023: 34000, 2022: 31000, 2021: 28000, 2020: 26000, 2019: 24000, 2018: 21000, 2017: 19000, 2016: 17000, 2015: 15000, 2014: 14000},
    "q2": {2025: 22500, 2024: 20500, 2023: 18500, 2022: 16500, 2021: 15000, 2020: 13500, 2019: 12000, 2018: 11000, 2017: 10000},
    "q3": {2025: 27000, 2024: 26000, 2023: 24000, 2022: 22000, 2021: 20000, 2020: 18000, 2019: 16500, 2018: 15000, 2017: 13500, 2016: 12000, 2015: 11000, 2014: 10000},
    "q5": {2025: 36000, 2024: 33000, 2023: 30000, 2022: 28000, 2021: 25000, 2020: 22000, 2019: 20000, 2018: 18000, 2017: 16500, 2016: 15000, 2015: 14000, 2014: 13000},
    "serie 1": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "serie 3": {2025: 39000, 2024: 34000, 2023: 29500, 2022: 26000, 2021: 24000, 2020: 21500, 2019: 19000, 2018: 17000, 2017: 15500, 2016: 14200, 2015: 13200, 2014: 12000},
    "serie 5": {2025: 50000, 2024: 46000, 2023: 41000, 2022: 37000, 2021: 33000, 2020: 29000, 2019: 26000, 2018: 24000, 2017: 22000, 2016: 20000, 2015: 18000, 2014: 17000},
    "x1": {2025: 28000, 2024: 25000, 2023: 23000, 2022: 21000, 2021: 19000, 2020: 17000, 2019: 15500, 2018: 14000, 2017: 12500, 2016: 11000, 2015: 10000, 2014: 9000},
    "x3": {2025: 36000, 2024: 33000, 2023: 30000, 2022: 28000, 2021: 25000, 2020: 22000, 2019: 20000, 2018: 18000, 2017: 16500, 2016: 15000, 2015: 14000, 2014: 13000},
    "yaris": {2025: 16500, 2024: 15000, 2023: 13500, 2022: 12000, 2021: 11000, 2020: 9500, 2019: 8800, 2018: 8000, 2017: 7200, 2016: 6500, 2015: 6000, 2014: 5500},
    "corolla": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15500, 2021: 14000, 2020: 13000, 2019: 12000, 2018: 10500, 2017: 9500, 2016: 8800, 2015: 8000, 2014: 7500},
    "c-hr": {2025: 23000, 2024: 21000, 2023: 19000, 2022: 17500, 2021: 16000, 2020: 14500, 2019: 13000, 2018: 12000, 2017: 10500},
    "rav4": {2025: 28000, 2024: 26000, 2023: 24000, 2022: 22000, 2021: 20000, 2020: 18000, 2019: 16500, 2018: 15000, 2017: 13500, 2016: 12000, 2015: 11000, 2014: 10000},
    "aygo": {2025: 12000, 2024: 11000, 2023: 10000, 2022: 9500, 2021: 8800, 2020: 8200, 2019: 7500, 2018: 7000, 2017: 6500, 2016: 6000, 2015: 5800, 2014: 5500},
    "208": {2025: 16200, 2024: 14300, 2023: 12500, 2022: 11200, 2021: 10000, 2020: 9000, 2019: 8000, 2018: 7200, 2017: 6300, 2016: 5800, 2015: 5200, 2014: 4800},
    "308": {2025: 19500, 2024: 17200, 2023: 14800, 2022: 13800, 2021: 12200, 2020: 11200, 2019: 10200, 2018: 9200, 2017: 8200, 2016: 7200, 2015: 6500, 2014: 6000},
    "2008": {2025: 20000, 2024: 18000, 2023: 16000, 2022: 14000, 2021: 13000, 2020: 12000, 2019: 11000, 2018: 9500, 2017: 8500, 2016: 7800, 2015: 7200, 2014: 6800},
    "3008": {2025: 24000, 2024: 22000, 2023: 19500, 2022: 17000, 2021: 15500, 2020: 13500, 2019: 12000, 2018: 10500, 2017: 10000, 2016: 9000, 2015: 8000, 2014: 7200},
    "5008": {2025: 26000, 2024: 24000, 2023: 21500, 2022: 19000, 2021: 17000, 2020: 15500, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "clio": {2025: 15800, 2024: 14000, 2023: 12000, 2022: 10800, 2021: 9500, 2020: 8700, 2019: 7700, 2018: 6800, 2017: 5900, 2016: 5400, 2015: 4800, 2014: 4400},
    "captur": {2025: 20500, 2024: 18000, 2023: 16000, 2022: 14000, 2021: 13000, 2020: 12000, 2019: 11000, 2018: 9500, 2017: 8500, 2016: 7800, 2015: 7200, 2014: 6800},
    "megane": {2025: 19500, 2024: 17200, 2023: 14800, 2022: 13000, 2021: 11500, 2020: 10500, 2019: 9500, 2018: 8500, 2017: 7700, 2016: 6800, 2015: 6200, 2014: 5600},
    "arkana": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500},
    "talisman": {2025: 22000, 2024: 20000, 2023: 18000, 2022: 16500, 2021: 15000, 2020: 13000, 2019: 11500, 2018: 10000, 2017: 9000, 2016: 8500, 2015: 7800, 2014: 7200},
    "zoe": {2025: 15000, 2024: 14000, 2023: 13000, 2022: 12000, 2021: 11000, 2020: 10000, 2019: 9000, 2018: 8500, 2017: 8000, 2016: 7000, 2015: 6500, 2014: 6000},
    "c1": {2025: 11500, 2024: 10500, 2023: 9500, 2022: 9000, 2021: 8200, 2020: 7500, 2019: 7000, 2018: 6500, 2017: 6000, 2016: 5800, 2015: 5500, 2014: 5000},
    "c3": {2025: 14500, 2024: 13000, 2023: 11500, 2022: 10500, 2021: 9500, 2020: 8800, 2019: 8000, 2018: 7200, 2017: 6200, 2016: 5800, 2015: 5200, 2014: 4800},
    "c4": {2025: 18500, 2024: 16500, 2023: 14500, 2022: 13000, 2021: 11500, 2020: 10500, 2019: 9500, 2018: 8500, 2017: 7800, 2016: 6800, 2015: 6500, 2014: 6000},
    "c3 aircross": {2025: 18500, 2024: 16500, 2023: 14500, 2022: 13000, 2021: 11500, 2020: 10500, 2019: 9500, 2018: 8500, 2017: 7800},
    "c5 aircross": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000},
    "berlingo": {2025: 19500, 2024: 17500, 2023: 15500, 2022: 13500, 2021: 12500, 2020: 11500, 2019: 10500, 2018: 9500, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7200},
    "ibiza": {2025: 15000, 2024: 13000, 2023: 11500, 2022: 10500, 2021: 9500, 2020: 8800, 2019: 8000, 2018: 7200, 2017: 6200, 2016: 5800, 2015: 5200, 2014: 4800},
    "leon": {2025: 19500, 2024: 17500, 2023: 15500, 2022: 13500, 2021: 12500, 2020: 11500, 2019: 10500, 2018: 9500, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7200},
    "arona": {2025: 18500, 2024: 16500, 2023: 14500, 2022: 13000, 2021: 12000, 2020: 11000, 2019: 10000, 2018: 9000, 2017: 8200},
    "ateca": {2025: 23000, 2024: 21000, 2023: 19000, 2022: 17500, 2021: 15500, 2020: 14000, 2019: 12500, 2018: 11000, 2017: 10000, 2016: 9000},
    "tarraco": {2025: 26000, 2024: 24000, 2023: 22000, 2022: 20000, 2021: 18000, 2020: 16500, 2019: 15000},
    "mazda2": {2025: 15500, 2024: 14000, 2023: 12500, 2022: 11000, 2021: 10000, 2020: 8800, 2019: 8000, 2018: 7200, 2017: 6500, 2016: 5800, 2015: 5200, 2014: 5000},
    "mazda3": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15500, 2021: 14000, 2020: 13000, 2019: 12000, 2018: 10500, 2017: 9500, 2016: 8800, 2015: 8000, 2014: 7500},
    "mazda6": {2025: 26000, 2024: 24000, 2023: 22000, 2022: 20000, 2021: 18000, 2020: 16500, 2019: 15000, 2018: 13000, 2017: 12000, 2016: 11000, 2015: 10000, 2014: 9500},
    "cx-3": {2025: 19000, 2024: 17000, 2023: 15500, 2022: 13500, 2021: 12000, 2020: 11000, 2019: 10000, 2018: 9000, 2017: 8200, 2016: 7500},
    "cx-5": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "cx-30": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500, 2020: 15500},
    "mg3": {2025: 13500, 2024: 12000, 2023: 10500, 2022: 10000, 2021: 9000, 2020: 8500, 2019: 8000},
    "zs": {2025: 17500, 2024: 16000, 2023: 14500, 2022: 13000, 2021: 11500, 2020: 10500, 2019: 9500},
    "hs": {2025: 23000, 2024: 21000, 2023: 19000, 2022: 17500, 2021: 16000, 2020: 14500, 2019: 13500},
    "mg4": {2025: 21000, 2024: 19000, 2023: 17500, 2022: 15500},
    "marvel r": {2025: 27000, 2024: 25000, 2023: 23000, 2022: 21000},
    "i10": {2025: 12500, 2024: 11000, 2023: 9500, 2022: 9000, 2021: 8800, 2020: 8200, 2019: 7500, 2018: 7000, 2017: 6500, 2016: 6000, 2015: 5800, 2014: 5500},
    "i20": {2025: 15000, 2024: 13000, 2023: 11500, 2022: 10500, 2021: 9500, 2020: 8800, 2019: 8000, 2018: 7200, 2017: 6200, 2016: 5800, 2015: 5200, 2014: 4800},
    "i30": {2025: 19500, 2024: 17500, 2023: 15500, 2022: 13500, 2021: 12500, 2020: 11500, 2019: 10500, 2018: 9500, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7200},
    "ix35": {2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "kona": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15500, 2021: 14000, 2020: 13000, 2019: 12000, 2018: 10500, 2017: 9500},
    "tucson": {2025: 24000, 2024: 22000, 2023: 20000, 2022: 18000, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "santa fe": {2025: 30000, 2024: 28000, 2023: 26000, 2022: 23000, 2021: 20000, 2020: 17000, 2019: 16000, 2018: 15000, 2017: 14000, 2016: 13000, 2015: 12000, 2014: 11000},
    "ioniq": {2025: 22000, 2024: 20000, 2023: 18000, 2022: 16500, 2021: 14500, 2020: 13500, 2019: 12000, 2018: 10500, 2017: 9500},
    "v40": {2020: 12500, 2019: 11500, 2018: 10500, 2017: 9500, 2016: 9000, 2015: 8200, 2014: 7500},
    "v60": {2025: 33000, 2024: 30000, 2023: 28000, 2022: 25000, 2021: 22000, 2020: 19000, 2019: 18000, 2018: 17000, 2017: 16000, 2016: 15000, 2015: 14000, 2014: 13000},
    "v90": {2025: 45000, 2024: 42000, 2023: 39000, 2022: 36000, 2021: 33000, 2020: 30000, 2019: 28000, 2018: 26000, 2017: 23000, 2016: 21000},
    "xc40": {2025: 30000, 2024: 27000, 2023: 24000, 2022: 22000, 2021: 20000, 2020: 18000, 2019: 16500, 2018: 15000},
    "xc60": {2025: 38000, 2024: 35000, 2023: 32000, 2022: 29000, 2021: 27000, 2020: 25000, 2019: 22000, 2018: 20000, 2017: 18000, 2016: 16500, 2015: 15000, 2014: 14000},
    "xc90": {2025: 52000, 2024: 49000, 2023: 46000, 2022: 43000, 2021: 40000, 2020: 38000, 2019: 35000, 2018: 32000, 2017: 30000, 2016: 28000, 2015: 26000, 2014: 24000},
    "micra": {2025: 13500, 2024: 12000, 2023: 10500, 2022: 10000, 2021: 9000, 2020: 8500, 2019: 8000, 2018: 7500, 2017: 6500, 2016: 6000, 2015: 5800, 2014: 5500},
    "juke": {2025: 18500, 2024: 16500, 2023: 14500, 2022: 13000, 2021: 12000, 2020: 11000, 2019: 10000, 2018: 9000, 2017: 8200, 2016: 7800, 2015: 7200, 2014: 6800},
    "qashqai": {2025: 25500, 2024: 23000, 2023: 20500, 2022: 18000, 2021: 16500, 2020: 14800, 2019: 13500, 2018: 12000, 2017: 10500, 2016: 9800, 2015: 9000, 2014: 8500},
    "x-trail": {2025: 27000, 2024: 25000, 2023: 23000, 2022: 21000, 2021: 19000, 2020: 17500, 2019: 16000, 2018: 14000, 2017: 12500, 2016: 11000, 2015: 10000, 2014: 9000},
    "leaf": {2025: 20000, 2024: 18000, 2023: 16500, 2022: 14500, 2021: 13000, 2020: 11500, 2019: 10000, 2018: 8800, 2017: 8000, 2016: 7000, 2015: 6500, 2014: 6000},
    "polo": {2025: 15800, 2024: 14000, 2023: 12000, 2022: 10800, 2021: 9500, 2020: 8700, 2019: 7700, 2018: 6800, 2017: 5900, 2016: 5400, 2015: 4800, 2014: 4400},
    "golf": {2025: 20500, 2024: 18200, 2023: 16200, 2022: 14200, 2021: 13000, 2020: 12000, 2019: 11000, 2018: 10000, 2017: 9000, 2016: 8500, 2015: 7800, 2014: 7200},
    "t-roc": {2025: 22500, 2024: 20000, 2023: 18000, 2022: 16000, 2021: 14500, 2020: 13000, 2019: 11500, 2018: 10500, 2017: 9500},
    "tiguan": {2025: 28000, 2024: 25500, 2023: 22500, 2022: 20000, 2021: 18000, 2020: 16000, 2019: 14500, 2018: 13000, 2017: 11500, 2016: 10000, 2015: 9500, 2014: 9000},
    "passat": {2025: 26000, 2024: 23500, 2023: 20500, 2022: 18500, 2021: 16500, 2020: 15000, 2019: 13500, 2018: 12000, 2017: 11000, 2016: 10000, 2015: 9000, 2014: 8500},
    "touareg": {2025: 45000, 2024: 42000, 2023: 38000, 2022: 34000, 2021: 30000, 2020: 28000, 2019: 25000, 2018: 22000, 2017: 19000, 2016: 17000, 2015: 15000, 2014: 14000},
    "renault kangoo": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15000, 2021: 13000, 2020: 12000, 2019: 10500, 2018: 9000, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7000},
    "renault trafic": {2025: 28000, 2024: 26000, 2023: 24000, 2022: 22000, 2021: 20000, 2020: 18000, 2019: 16500, 2018: 15000, 2017: 13500, 2016: 12000, 2015: 11000, 2014: 10000},
    "renault master": {2025: 32000, 2024: 30000, 2023: 28000, 2022: 26000, 2021: 24000, 2020: 22000, 2019: 20000, 2018: 18000, 2017: 16500, 2016: 15000, 2015: 13000, 2014: 12000},
    "peugeot partner": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15000, 2021: 13000, 2020: 12000, 2019: 10500, 2018: 9000, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7000},
    "peugeot boxer": {2025: 31000, 2024: 29000, 2023: 27000, 2022: 25000, 2021: 23000, 2020: 21000, 2019: 19000, 2018: 17000, 2017: 15500, 2016: 14000, 2015: 13000, 2014: 11000},
    "citroen berlingo": {2025: 21000, 2024: 19000, 2023: 17000, 2022: 15000, 2021: 13000, 2020: 12000, 2019: 10500, 2018: 9000, 2017: 8500, 2016: 8000, 2015: 7500, 2014: 7000},
}

# DATASET 100+ MODELES SANS DOUBLONS

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

# ===============================
# 🔥 TABLEAU MARCHE INTEGRE PRO
# ===============================
MARKET_TABLE = {
    "citadine": {
        2020: {45000:9500, 55000:9000, 75000:8200, 90000:7700},
        2021: {45000:10500, 55000:10000, 75000:9200, 90000:8700},
        2022: {45000:11800, 55000:11200, 75000:10300, 90000:9700},
        2023: {45000:13000, 55000:12300, 75000:11300, 90000:10500},
        2024: {45000:14200, 55000:13500, 75000:12500, 90000:11500},
    },
    "compacte": {
        2020: {45000:13000, 55000:12300, 75000:11300, 90000:10500},
        2021: {45000:14200, 55000:13500, 75000:12500, 90000:11500},
        2022: {45000:16000, 55000:15200, 75000:14000, 90000:13000},
        2023: {45000:17500, 55000:16500, 75000:15000, 90000:14000},
        2024: {45000:19000, 55000:18000, 75000:16500, 90000:15000},
    },
    "suv": {
        2020: {45000:17000, 55000:16000, 75000:15000, 90000:14000},
        2021: {45000:19500, 55000:18800, 75000:17500, 90000:16500},
        2022: {45000:18500, 55000:17500, 75000:16000, 90000:15000},
        2023: {45000:20500, 55000:19500, 75000:17500, 90000:16000},
        2024: {45000:22500, 55000:21000, 75000:19000, 90000:17500},
    },
    "premium": {
        2020: {45000:30000, 55000:28500, 75000:27000, 90000:26000},
        2021: {45000:32000, 55000:30000, 75000:28000, 90000:27000},
        2022: {45000:34000, 55000:32000, 75000:30000, 90000:28500},
        2023: {45000:37000, 55000:34500, 75000:32000, 90000:30000},
        2024: {45000:40000, 55000:37000, 75000:34000, 90000:32000},
    }
}

def detect_segment(key):
    if any(x in key for x in ["clio","208","corsa","i20","polo"]):
        return "citadine"
    elif any(x in key for x in ["megane","308","golf","focus"]):
        return "compacte"
    elif any(x in key for x in ["3008","qashqai","tucson","kuga"]):
        return "suv"
    elif any(x in key for x in ["q5","x3","x5","q7","glc","xc60"]):
        return "premium"
    elif any(x in key for x in ["audi","bmw","mercedes","tesla","volvo"]):
        return "premium"
    return "compacte"

def interpolate_km(table_km, km):
    kms = sorted(table_km.keys())
    if km <= kms[0]:
        return table_km[kms[0]]
    if km >= kms[-1]:
        return table_km[kms[-1]]
    for i in range(len(kms)-1):
        if kms[i] <= km <= kms[i+1]:
            k1, k2 = kms[i], kms[i+1]
            v1, v2 = table_km[k1], table_km[k2]
            ratio = (km - k1) / (k2 - k1)
            return int(v1 + (v2 - v1) * ratio)
    return None

def ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement="", options=None, transmission=None):

    if options is None:
        options = []

    import unicodedata, re

    def norm(s):
        if not s:
            return ""
        return unicodedata.normalize('NFD', s.lower()).encode('ascii','ignore').decode('utf-8')

    marque = norm(marque)
    modele = norm(modele)
    finition = norm(finition)
    motorisation = norm(motorisation)

    key = f"{marque} {modele}".strip()
    segment = detect_segment(key)

    # 🔥 SECURITE PREMIUM
    if "q5" in key:
        segment = "premium"

    

    # 🔥 BASE = MARKET PRIORITAIRE
    base = None
    if segment and annee in MARKET_TABLE.get(segment, {}):
        base = interpolate_km(MARKET_TABLE[segment][annee], km)

    # fallback dataset
    if base is None:
        for m, years in BASE_PRICES_V2.items():
            if key == m or key.startswith(m):
                if annee in years:
                    base = years[annee]
                else:
                    closest = min(years.keys(), key=lambda x: abs(x - annee))
                    base = years[closest]
                break

    if base is None:
        base = 15000

    # 🔥 correction premium réaliste
    if segment == "premium":
        base *= 0.92

    coef = 1.0

    # KM FIX
    km_delta = (km - 90000) / 120000

    # YEAR FIX
    if annee >= 2021:
        coef += min((annee - 2020) * 0.02, 0.08)
    elif annee < 2020:
        coef -= min((2020 - annee) * 0.03, 0.15)

    # MOTOR
    power = re.findall(r'[0-9]{2,3}', motorisation)
    if power:
        p = int(power[0])
        if p >= 180:
            coef += 0.02
        elif p <= 100:
            coef -= 0.02

    # FUEL
    if carburant == "Essence":
        coef += 0.01
    elif carburant == "Diesel":
        coef -= 0.005

    # 🔥 FINITION PRO CLEAN
    finition_bonus = 0

    if any(x in finition for x in ["amg","rs","m sport","s line"]):
        finition_bonus = 0.12
    elif any(x in finition for x in ["line","allure","intens","shine"]):
        finition_bonus = 0.04

    # dataset uniquement si finition renseignée
    if finition:
        for m, (low, high) in FINITION_ADJUST.items():
            if m in key:
                finition_bonus = max(finition_bonus, (low + high) / 2)

    coef += finition_bonus

    # OPTIONS léger
    for opt in options:
        coef += 0.005

    # AWD
    if transmission in ["4x4","AWD","4WD"]:
        coef += 0.02

    # GEO
    if departement in ["75","92"]:
        coef += 0.02
    elif departement in ["08","23"]:
        coef -= 0.015

    price = base * coef

    # 🔥 CLAMP V16 PREMIUM
    if segment == "premium":
        min_price = base * 0.90
        max_price = base * 1.25
    else:
        min_price = base * 0.92
        max_price = base * 1.15
    price = max(min_price, min(price, max_price))

    return int(max(4000, min(price, 120000)))

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
    expire = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

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

    st.markdown("<h3 style='margin-bottom:0;'>Veliora Pro</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Essai gratuit 1 jour</h4>", unsafe_allow_html=True)

    st.info(f"Après 1 jour d'essai : {PRICE_HT}€ HT ({PRICE_TTC}€ TTC) / mois")

    st.markdown(f"[💳 S'abonner maintenant ({PRICE_TTC}€ TTC)]({STRIPE_LINK})")

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

col_header_left, col_header_right = st.columns([4,1])

with col_header_left:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="
            width:38px;
            height:38px;
            border-radius:8px;
            background:linear-gradient(135deg,#1f2937,#111827);
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:700;
            color:white;
        ">
            V
        </div>
        <div>
            <div style="font-size:22px; font-weight:600;">VELIORA</div>
            <div style="font-size:13px; color:#9CA3AF;">
                Cotation automobile intelligente
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


col1, col2 = st.columns([3,1])

with col1:
    if st.button("🔄 Nouvelle cotation (reset)"):
        st.session_state.reset_id += 1
        if "resultat" in st.session_state:
            del st.session_state["resultat"]
        st.rerun()

with col2:
    if st.button("🚪 Se déconnecter"):
        st.session_state.logged = False
        st.session_state.admin_logged = False
        st.rerun()
        st.session_state.reset_id += 1
        if "resultat" in st.session_state:
            del st.session_state["resultat"]
        st.rerun()

col2a, col2b = st.columns(2)

with col2a:
    st.session_state.show_history = st.toggle("📊 Historique", value=st.session_state.show_history)

with col2b:
    buffer_hist = io.StringIO()
    buffer_hist.write("===== HISTORIQUE ESTIMATIONS =====\n\n")
for item in st.session_state.historique:
    buffer_hist.write(f"{item.get('marque','')} {item.get('modele','')} {item.get('finition','')}\n")
    buffer_hist.write(f"{item.get('motorisation','')}\n")
    buffer_hist.write(f"{item.get('annee','')} • {item.get('km','')} km\n")

    buffer_hist.write(f"Carburant : {item.get('carburant','')}\n")
    buffer_hist.write(f"Boîte : {item.get('boite','')}\n")
    buffer_hist.write(f"Transmission : {item.get('transmission','')}\n")
    buffer_hist.write(f"Options : {item.get('options','')}\n")
    buffer_hist.write(f"Département : {item.get('departement','')}\n")

    buffer_hist.write(f"Prix marché : {item.get('prix_marche','')} €\n")
    buffer_hist.write(f"Bas : {item.get('prix_bas_min','')} € → {item.get('prix_bas_max','')} €\n")
    buffer_hist.write(f"Haut : {item.get('prix_haut_min','')} € → {item.get('prix_haut_max','')} €\n")

    buffer_hist.write(f"Date : {item.get('date','')}\n")
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
➡️ **{item['prix_marche']} € (marché)**  
🕒 {item['date']}  

---
""")


# Lien Argus en haut
st.markdown("[📄 Voir fiche technique Argus](https://www.largus.fr/fiche-technique.html)")

# 🔥 ASSISTANT SAISIE INTELLIGENT (VERSION CORRIGÉE)
def parse_title(title):
    t = unicodedata.normalize('NFD', title.lower()).encode('ascii','ignore').decode('utf-8')

    result = {
        "modele": "",
        "motorisation": "",
        "finition": "",
        "carburant": ""
    }

    # MODELES
    if "ds4" in t: result["modele"] = "ds4 crossback"
    elif "ds3" in t: result["modele"] = "ds3 crossback"
    elif "clio" in t: result["modele"] = "clio"
    elif "golf" in t: result["modele"] = "golf"
    elif "q5" in t: result["modele"] = "q5"
    elif "x3" in t: result["modele"] = "x3"

    # CARBURANT + MOTORISATION
    if "ethanol" in t or "e85" in t:
        result["motorisation"] = "ethanol"
        result["carburant"] = "Essence"
    elif "diesel" in t or "tdi" in t or "dci" in t:
        result["motorisation"] = "diesel"
        result["carburant"] = "Diesel"
    elif "essence" in t or "tce" in t or "tsi" in t:
        result["motorisation"] = "essence"
        result["carburant"] = "Essence"
    elif "hybride" in t:
        result["carburant"] = "Hybride"
    elif "electrique" in t:
        result["carburant"] = "Électrique"

    # FINITION
    if "crossback" in t: result["finition"] = "crossback"
    elif "s line" in t: result["finition"] = "s line"
    elif "m sport" in t: result["finition"] = "m sport"
    elif "intens" in t: result["finition"] = "intens"
    elif "allure" in t: result["finition"] = "allure"

    return result

rid = st.session_state.reset_id

# champ titre supprimé
parsed = {}

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

transmission = st.selectbox("Transmission", ["", "4x2","Traction","Propulsion","4x4","AWD","4WD"], key=f"trans_{rid}")

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

commission = 0
commission_pct = 0.0

col_btn, col_txt = st.columns([1,2])

with col_btn:
    calcul = st.button("Calculer l'estimation")

with col_txt:
    st.caption("Estimation basée sur algorithme marché — non contractuel")

if calcul:

    prix_ai = ai_price_engine(marque, modele, finition, motorisation, annee, km, carburant, boite, departement, options, transmission)

    prix_comparables = []

    if get_leboncoin_prices:
        try:
            query = f"{marque} {modele} {motorisation} {annee}"
            prix_comparables = get_leboncoin_prices(query, km, carburant, boite)
            st.info(f"Leboncoin PRO : {len(prix_comparables)} annonces")
        except:
            pass

    # 🔥 MODE STABLE (désactivation learning / scraping)
    prix_marche = prix_ai

    # 🔥 LOGIQUE PRO FOURCHETTE
    base = int(round(prix_marche / 100) * 100)

    prix_bas_min = max(3000, base - 2000)
    prix_bas_max = base - 1000

    prix_marche_affiche = base

    prix_haut_min = base + 1000
    prix_haut_max = min(120000, base + 2000)

    # ✅ historique (après calcul)
    st.session_state.historique.insert(0, {
    "prix_marche": prix_marche_affiche,
    "prix_bas_min": prix_bas_min,
    "prix_bas_max": prix_bas_max,
    "prix_haut_min": prix_haut_min,
    "prix_haut_max": prix_haut_max,
    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),

    "marque": marque,
    "modele": modele,
    "finition": finition,
    "sous_version": sous_version,
    "motorisation": motorisation,

    "carburant": carburant,
    "boite": boite,
    "transmission": transmission,
    "options": ", ".join(options) if options else "Aucune",
    "departement": departement,

    "annee": annee,
    "km": km
})

    st.session_state.historique = st.session_state.historique[:20]


    

    prix_vente = prix_psy(prix_marche)

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

    # DUPLICATE DISPLAY REMOVED

    st.subheader("💰 PRIX MARCHÉ ESTIMÉ")
    st.success(f"{prix_marche_affiche} €")
    st.caption("(Prix marché estimé basé sur modèle, année et configuration du véhicule.)")

    st.markdown(f"📉 Bas : {prix_bas_min} € -> {prix_bas_max} €")
    st.caption("(2015 à 2018/95000-130000 km peu importe la finition)")

    st.markdown(f"📈 Haut : {prix_haut_min} € -> {prix_haut_max} €")
    st.caption("(2021 à 2025/de 30 à 75000km/ finition luxe.)")
    


    # 🔥 STOCKAGE RESULTAT (pour éviter reset)
    st.session_state.resultat = {
        "prix_vente": prix_vente,
        "net_marche": net_marche,
        "prix_bas_min": prix_bas_min,
        "prix_bas_max": prix_bas_max,
        
        
        "prix_haut_min": prix_haut_min,
        "prix_haut_max": prix_haut_max,
        "prix_marche_estime": prix_marche
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
    buffer.write(f"Prix marché : {prix_bas_min} € à {prix_haut_max} €\n")
    buffer.write(f"Prix haut : {prix_haut_min} € à {prix_haut_max} €\n")

# ===== AFFICHAGE STABLE (hors bouton) =====
if "resultat" in st.session_state:
    r = st.session_state.resultat

    col_left, col_right = st.columns(2)

    
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

