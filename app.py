import streamlit as st

st.set_page_config(page_title="Veliora", layout="centered")

PASSWORD = "veliora2026"

if "auth" not in st.session_state:
    st.session_state.auth = False

# 🔐 Écran de connexion
if not st.session_state.auth:
    st.title("🔐 VELIORA COTATION")
    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True
        st.experimental_rerun()

    st.stop()

# 🚗 Application principale
st.title("🚗 VELIORA Cotation Pro")

prix = st.number_input("Prix marché (€)", 0, 100000, 15000)
date = st.text_input("Date (MM/YYYY)", "01/2020")
km = st.number_input("Kilométrage", 0, 300000, 50000)

if st.button("Calculer"):
    try:
        mois, annee = map(int, date.split("/"))
        age = 2026 - annee

        km_moyen = age * 15000
        ajustement = (km - km_moyen) * 0.04

        resultat = prix - (prix * 0.07 * age) - ajustement

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except:
        st.error("❌ Format de date invalide")
