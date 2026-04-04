import streamlit as st
from datetime import datetime
import webbrowser

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Veliora Pro", layout="centered")

# =========================
# DESIGN PRO
# =========================

st.markdown("""
<style>
.main {background-color: #f5f7fb;}
h1 {color: #1f2c56; font-weight: 700;}
.section {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.stButton button {
    background-color: #1f77ff;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

PASSWORD = "veliora2026"

# =========================
# LOGIN
# =========================

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 VELIORA COTATION PRO")
    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True
        st.rerun()

    st.stop()

# =========================
# TITRE
# =========================

st.title("🚗 Veliora Cotation Pro")

# =========================
# INFOS VEHICULE
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("🚗 Informations véhicule")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CARACTERISTIQUES
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("⚙️ Caractéristiques")

col1, col2 = st.columns(2)

with col1:
    carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"])
    boite = st.selectbox("Boîte", ["Manuelle", "Automatique"])

with col2:
    traction = st.text_input("Traction")
    motorisation = st.text_input("Motorisation")

permis = st.selectbox("Permis", ["Avec permis", "Sans permis"])

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DATE
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📅 Date de première mise en circulation")

col1, col2 = st.columns(2)

with col1:
    mois = st.selectbox("Mois", list(range(1, 13)))

with col2:
    annee = st.selectbox("Année", list(range(1990, datetime.now().year + 1)))

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# KM
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📊 Kilométrage")

km = st.number_input("Kilométrage du véhicule", 0, 300000, 50000)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INFOS VENDEUR
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("👤 Informations vendeur")

departement = st.text_input("Département")
vendeur = st.text_input("Nom vendeur")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# COTATION CALCULÉE
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("💰 Cotation estimée (théorique)")

if st.button("Calculer estimation"):

    age = datetime.now().year - annee + (datetime.now().month - mois)/12

    base = 18000
    valeur = base * (0.78 ** age)

    km_moyen = age * 15000
    valeur -= (km - km_moyen) * 0.07

    if carburant == "Diesel":
        valeur *= 0.9
    elif carburant == "Hybride":
        valeur *= 1.05
    elif carburant == "Électrique":
        valeur *= 1.08

    if boite == "Automatique":
        valeur *= 1.03

    st.info(f"💰 Estimation : {int(valeur)} €")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# COTE MARCHE REEL
# =========================

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📊 Cote marché réel (particulier)")

if st.button("🔎 Voir annonces marché"):

    recherche = f"{marque} {modele} {annee}"
    url = f"https://www.leboncoin.fr/recherche?text={recherche}"
    webbrowser.open_new_tab(url)

st.write("➡️ Renseigne 3 à 5 prix observés")

prix1 = st.number_input("Prix 1", 0, 100000, 0)
prix2 = st.number_input("Prix 2", 0, 100000, 0)
prix3 = st.number_input("Prix 3", 0, 100000, 0)
prix4 = st.number_input("Prix 4", 0, 100000, 0)
prix5 = st.number_input("Prix 5", 0, 100000, 0)

if st.button("Calculer cote marché réelle"):

    prix_list = [p for p in [prix1, prix2, prix3, prix4, prix5] if p > 0]

    if len(prix_list) >= 3:
        prix_list.sort()

        if len(prix_list) > 3:
            prix_list = prix_list[1:-1]

        moyenne = int(sum(prix_list) / len(prix_list))

        bas = int(moyenne * 0.9)
        haut = int(moyenne * 1.1)

        st.success(f"💰 Prix marché réel : {moyenne} €")
        st.info(f"📉 Bas : {bas} €")
        st.info(f"📈 Haut : {haut} €")

    else:
        st.error("Ajoute au moins 3 prix")

st.markdown('</div>', unsafe_allow_html=True)
