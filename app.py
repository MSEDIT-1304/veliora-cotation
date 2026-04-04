import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Veliora", layout="centered")

PASSWORD = "veliora2026"

# Auth
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 VELIORA COTATION")

    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True

    st.stop()

# =========================
# 🚗 APP PRO
# =========================

st.title("🚗 VELIORA Cotation Pro")

# Infos véhicule
marque = st.text_input("Marque", "Peugeot")
modele = st.text_input("Modèle", "308")
finition = st.text_input("Finition", "Allure")

date_mec = st.date_input("Date mise en circulation")

km = st.number_input("Kilométrage", 0, 300000, 50000)
prix_marche = st.number_input("Prix marché (€)", 0, 100000, 15000)

# Calcul
if st.button("Calculer la cotation"):
    try:
        annee_actuelle = datetime.now().year
        age = annee_actuelle - date_mec.year

        km_moyen = age * 15000
        ecart_km = km - km_moyen

        # Ajustements
        coeff_age = 0.08
        coeff_km = 0.05

        decote_age = prix_marche * coeff_age * age
        ajustement_km = ecart_km * coeff_km

        valeur = prix_marche - decote_age - ajustement_km

        st.subheader("📊 Résultat")

        st.write(f"**Véhicule :** {marque} {modele} {finition}")
        st.write(f"**Âge :** {age} ans")
        st.write(f"**Kilométrage moyen attendu :** {km_moyen} km")

        st.success(f"💰 Valeur estimée : {int(valeur)} €")

    except:
        st.error("Erreur dans les données")
