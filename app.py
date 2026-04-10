import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import statistics

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔥 IA AJOUT SÉCURISÉ
try:
    import joblib
    import os
    model = None
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
except:
    model = None

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ===== THEME VELOIRA =====
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: white;
}
h1, h2, h3 {
    color: white;
}
.stButton>button {
    background: linear-gradient(90deg,#0f766e,#14b8a6);
    color:white;
    border-radius:10px;
    padding:10px 20px;
    border:none;
}
.stTextInput>div>div>input,
.stSelectbox>div>div {
    background-color:#1e293b;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CONFIG ----------------
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# ---------------- USERS ----------------
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")
    return df

def check_login(username, password):
    df = load_users()
    user = df[(df["username"] == username.strip()) & (df["password"] == password.strip())]
    if not user.empty:
        expire = user.iloc[0]["expire"]
        if datetime.now() > expire:
            return "expired"
        return "ok"
    return "error"

def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    requests.post(WEBHOOK_URL, json={
        "username": username,
        "password": password,
        "expire": expire,
        "trial": True
    })

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:

    st.title("🚗 Veliora Pro")
    st.subheader("🎁 Essai gratuit 3 jours")
    st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logged = True
            st.rerun()

        result = check_login(user, pwd)
        if result == "ok":
            st.session_state.logged = True
            st.rerun()
        elif result == "expired":
            st.error("Abonnement expiré")
        else:
            st.error("Erreur login")

    st.stop()

# ================= APP =================

st.title("🚗 VELIORA COTATION PRO")

marque = st.text_input("Marque")
modele = st.text_input("Modèle")
finition = st.text_input("Finition")
motorisation = st.text_input("Motorisation")

annee = st.number_input("Année", 1990, 2025, 2019)
km = st.number_input("Kilométrage", 0, 400000, 90000)

commission = st.number_input("Commission (€)", 0, 10000, 1000)

# ================= CALCUL =================

if st.button("Calculer l'estimation"):

    prix_marche = int(9000 + (2025 - annee)*-300 - km*0.01)
    prix_bas = int(prix_marche * 0.92)
    prix_haut = int(prix_marche * 1.08)

    net_marche = prix_marche - commission
    net_bas = prix_bas - commission
    net_haut = prix_haut - commission

    # ===== DESIGN =====
    st.markdown("## 📊 Résultat")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🔻 Vente rapide", f"{prix_bas} €", f"net {net_bas} €")

    with col2:
        st.metric("⭐ Prix marché", f"{prix_marche} €", f"net {net_marche} €")

    with col3:
        st.metric("🔺 Prix haut", f"{prix_haut} €", f"net {net_haut} €")

    # ===== COPIER ANNONCE =====
    annonce = f"""
🚗 {marque} {modele}
📅 {annee} | {km} km
⚙️ {motorisation} | {finition}

💰 Prix conseillé : {prix_marche} €
"""

    st.text_area("📋 Annonce prête à copier", annonce)

    # ===== PDF =====
    def create_pdf():
        doc = SimpleDocTemplate("estimation.pdf")
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Estimation véhicule - Veliora", styles['Title']))
        content.append(Spacer(1, 10))
        content.append(Paragraph(annonce, styles['Normal']))

        doc.build(content)

    if st.button("📄 Générer PDF"):
        create_pdf()
        with open("estimation.pdf", "rb") as f:
            st.download_button("📥 Télécharger PDF", f, file_name="estimation.pdf")
