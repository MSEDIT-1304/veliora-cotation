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

# Infos véhicule
marque = st.selectbox("Marque", ["Peugeot", "Renault", "BMW", "Audi", "Mercedes"])
modele = st.text_input("Modèle", "308")
finition = st.text_input("Finition", "Allure")

date_mec = st.date_input("Date mise en circulation")

km = st.number_input("Kilométrage", 0, 300000, 50000)

# =========================
# 🧠 CALCUL
# =========================
if st.button("Calculer la cotation"):
    try:
        annee_actuelle = datetime.now().year
        age = annee_actuelle - date_mec.year

        # 💰 Valeur de base selon marque
        base_prix = {
            "Peugeot": 22000,
            "Renault": 21000,
            "BMW": 35000,
            "Audi": 36000,
            "Mercedes": 40000
        }

        valeur_neuve = base_prix.get(marque, 25000)

        # 📉 Décote annuelle
        valeur = valeur_neuve * (0.85 ** age)

        # 🚗 Ajustement kilométrique
        km_moyen = age * 15000
        ecart_km = km - km_moyen
        valeur -= ecart_km * 0.05

        # ⭐ Bonus finition
        finition_lower = finition.lower()

        if "gt" in finition_lower or "sport" in finition_lower:
            valeur *= 1.1
        elif "base" in finition_lower:
            valeur *= 0.9

        # 🔎 Affichage
        st.subheader("📊 Résultat")

        st.write(f"**Véhicule :** {marque} {modele} {finition}")
        st.write(f"**Âge :** {age} ans")
        st.write(f"**Kilométrage moyen :** {km_moyen} km")

        st.success(f"💰 Valeur estimée : {int(valeur)} €")

    except:
        st.error("❌ Erreur dans les données")
