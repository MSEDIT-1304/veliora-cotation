import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Veliora", layout="centered")

PASSWORD = "veliora2026"

# =========================
# 🔐 AUTHENTIFICATION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 VELIORA COTATION")

    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True

    st.stop()

# =========================
# 🚗 APP PRINCIPALE
# =========================
st.title("🚗 VELIORA Cotation Pro")

# ===== MARQUE =====
marques = ["Peugeot", "Renault", "BMW", "Audi", "Mercedes", "Volkswagen", "Toyota", "Autre"]
marque_select = st.selectbox("Marque", marques)

if marque_select == "Autre":
    marque = st.text_input("Saisir la marque")
else:
    marque = marque_select

# ===== MODELE =====
modele = st.text_input("Modèle (ou saisie libre)", "308")

# ===== FINITION =====
finition = st.text_input("Finition (ou saisie libre)", "Allure")

# ===== DATE =====
date_mec = st.date_input("Date mise en circulation")

# ===== KM =====
km = st.number_input("Kilométrage", 0, 300000, 50000)

# =========================
# 🧠 CALCUL
# =========================
if st.button("Calculer la cotation"):
    try:
        annee_actuelle = datetime.now().year
        age = annee_actuelle - date_mec.year

        # 💰 Base par marque
        base_prix = {
            "Peugeot": 22000,
            "Renault": 21000,
            "BMW": 35000,
            "Audi": 36000,
            "Mercedes": 40000,
            "Volkswagen": 28000,
            "Toyota": 27000
        }

        valeur_neuve = base_prix.get(marque, 25000)

        # 📉 Décote
        valeur = valeur_neuve * (0.85 ** age)

        # 🚗 Ajustement km
        km_moyen = age * 15000
        ecart_km = km - km_moyen
        valeur -= ecart_km * 0.05

        # ⭐ Finition
        finition_lower = finition.lower()

        if "gt" in finition_lower or "sport" in finition_lower:
            valeur *= 1.1
        elif "base" in finition_lower:
            valeur *= 0.9

        # 📊 Résultat
        st.subheader("📊 Résultat")

        st.write(f"**Véhicule :** {marque} {modele} {finition}")
        st.write(f"**Âge :** {age} ans")
        st.write(f"**Kilométrage moyen :** {km_moyen} km")

        st.success(f"💰 Valeur estimée : {int(valeur)} €")

    except:
        st.error("❌ Erreur dans les données")
