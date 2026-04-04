import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Veliora Pro", layout="centered")

PASSWORD = "veliora2026"

# =========================
# 🔐 LOGIN
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 VELIORA COTATION PRO")
    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True

    st.stop()

# =========================
# 🚗 BASE MARQUES / MODELES
# =========================
data = {
    "Peugeot": ["208", "308", "3008", "5008"],
    "Renault": ["Clio", "Megane", "Captur", "Kadjar"],
    "BMW": ["Serie 1", "Serie 3", "X1", "X3"],
    "Audi": ["A1", "A3", "A4", "Q3", "Q5"],
    "Mercedes": ["Classe A", "Classe C", "GLA", "GLC"],
    "Volkswagen": ["Golf", "Polo", "Tiguan", "Passat"],
    "Toyota": ["Yaris", "Corolla", "RAV4"]
}

# =========================
# 🧾 INTERFACE VENDEUR
# =========================
st.title("🚗 VELIORA Cotation Vendeur")

col1, col2 = st.columns(2)

with col1:
    marque_select = st.selectbox("Marque", list(data.keys()) + ["Autre"])

    if marque_select == "Autre":
        marque = st.text_input("Marque libre")
        modele = st.text_input("Modèle")
    else:
        marque = marque_select
        modele_select = st.selectbox("Modèle", data[marque] + ["Autre"])

        if modele_select == "Autre":
            modele = st.text_input("Modèle libre")
        else:
            modele = modele_select

    finition = st.text_input("Finition", "Allure")

with col2:
    carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Electrique"])
    date_mec = st.date_input("Mise en circulation")
    km = st.number_input("Kilométrage", 0, 300000, 50000)

# =========================
# 💰 CALCUL VENDEUR
# =========================
if st.button("🔍 Calculer la valeur"):

    annee_actuelle = datetime.now().year
    age = annee_actuelle - date_mec.year

    # Base prix par gamme marque
    base_prix = {
        "Peugeot": 22000,
        "Renault": 21000,
        "Volkswagen": 28000,
        "Toyota": 27000,
        "BMW": 35000,
        "Audi": 36000,
        "Mercedes": 40000
    }

    valeur_neuve = base_prix.get(marque, 25000)

    # Décote pro (plus réaliste)
    valeur = valeur_neuve * (0.82 ** age)

    # Ajustement kilométrique
    km_moyen = age * 15000
    valeur -= (km - km_moyen) * 0.06

    # Ajustement carburant
    if carburant == "Diesel":
        valeur *= 0.95
    elif carburant == "Hybride":
        valeur *= 1.05
    elif carburant == "Electrique":
        valeur *= 1.1

    # Ajustement finition
    f = finition.lower()
    if "sport" in f or "gt" in f:
        valeur *= 1.1
    elif "base" in f:
        valeur *= 0.9

    # Encadrement vendeur (prix mini / max)
    prix_bas = int(valeur * 0.9)
    prix_haut = int(valeur * 1.1)

    # =========================
    # 📊 AFFICHAGE PRO
    # =========================
    st.markdown("---")
    st.subheader("📊 Résultat de cotation")

    st.write(f"**Véhicule :** {marque} {modele} {finition}")
    st.write(f"**Carburant :** {carburant}")
    st.write(f"**Âge :** {age} ans")
    st.write(f"**Kilométrage :** {km} km")

    st.success(f"💰 Prix conseillé : {int(valeur)} €")

    st.info(f"💸 Fourchette de vente : {prix_bas} € → {prix_haut} €")

    # Conseil vendeur
    if km > km_moyen:
        st.warning("⚠️ Kilométrage supérieur à la moyenne")
    else:
        st.success("✔️ Kilométrage cohérent")
