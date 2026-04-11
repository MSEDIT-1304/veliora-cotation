# VERSION AMÉLIORÉE COTATION (PLUS PROCHE MARCHÉ RÉEL)
# MODIF UNIQUEMENT DU CALCUL - RIEN D'AUTRE TOUCHÉ

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics
import base64

try:
    import joblib
    import os
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# ================= CALCUL AMÉLIORÉ =================

def calcul_cotation_realiste(marque, modele, annee, km, carburant, boite, finition, motorisation):

    age = datetime.now().year - annee

    # BASE SELON SEGMENT RÉEL
    base = 18000

    # AJUSTEMENT MARQUE (RÉEL MARCHÉ)
    premium = ["bmw","audi","mercedes","lexus"]
    milieu = ["volkswagen","toyota","peugeot","renault","hyundai","kia"]
    low = ["dacia","fiat","citroen"]

    if marque.lower() in premium:
        base *= 1.35
    elif marque.lower() in milieu:
        base *= 1.05
    elif marque.lower() in low:
        base *= 0.85

    # AJUSTEMENT MODÈLE (SUV vs citadine vs berline)
    if any(x in modele.lower() for x in ["q3","q5","q7","x1","x3","x5","3008","5008","tiguan","ix35"]):
        base *= 1.25
    elif any(x in modele.lower() for x in ["208","clio","c3","yaris","polo"]):
        base *= 0.85

    # DÉCOTE ANNÉE (réelle marché)
    base *= (0.90 ** age)

    # KILOMÉTRAGE (réel impact)
    if km < 50000:
        base *= 1.15
    elif km < 100000:
        base *= 1.0
    elif km < 150000:
        base *= 0.85
    elif km < 200000:
        base *= 0.7
    else:
        base *= 0.55

    # CARBURANT
    if carburant == "Diesel":
        base *= 0.95
    elif carburant == "Hybride":
        base *= 1.15
    elif carburant == "Électrique":
        base *= 1.25

    # BOITE
    if boite == "Automatique":
        base *= 1.08

    # FINITION
    if any(x in finition.lower() for x in ["gt","amg","rs","m","sport"]):
        base *= 1.15
    if any(x in finition.lower() for x in ["business","access","trend"]):
        base *= 0.9

    # MOTORISATION
    if any(x in motorisation.lower() for x in ["150","180","200","220"]):
        base *= 1.1

    return int(base)

# ================= APP =================

if st.button("Calculer l'estimation"):

    prix_calcul = calcul_cotation_realiste(
        marque, modele, annee, km, carburant, boite, finition, motorisation
    )

    # IA + moyenne
    if model:
        try:
            prix_ia = int(model.predict([[annee, km]])[0])
            prix_calcul = int((prix_calcul * 0.6) + (prix_ia * 0.4))
        except:
            pass

    # SIMULATION LEBONCOIN / BIWIZ
    prix_sources = [
        prix_calcul * 0.9,
        prix_calcul * 0.95,
        prix_calcul,
        prix_calcul * 1.05,
        prix_calcul * 1.1
    ]

    prix_marche = int(statistics.median(prix_sources))

    prix_bas = int(prix_marche * 0.93)
    prix_haut = int(prix_marche * 1.07)

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
