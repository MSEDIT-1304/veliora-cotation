import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ================= CONFIG =================
WEBHOOK_URL = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"
SHEET_ID = "1JWwwLP3IKaG-ELsC3li84eouOFVFnv_C5MxBDQSfz3M"
STRIPE_LINK = "https://buy.stripe.com/3cIcN64Eq0h72LNfio9fW04"

ADMIN_USER = "admin"
ADMIN_PASS = "TonMotDePasseFort123!"

# ================= LOAD USERS =================
@st.cache_data(ttl=60)
def load_users():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)

    df.columns = df.columns.str.strip().str.lower()

    if "username" not in df.columns:
        return pd.DataFrame(columns=["username","password","expire","trial","active"])

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["expire"] = pd.to_datetime(df["expire"], errors="coerce")

    if "active" not in df.columns:
        df["active"] = True
    if "trial" not in df.columns:
        df["trial"] = True

    return df

# ================= LOGIN =================
def check_login(username, password):
    df = load_users()

    user = df[
        (df["username"] == username.strip()) &
        (df["password"] == password.strip())
    ]

    if user.empty:
        return "error"

    u = user.iloc[0]

    if str(u["active"]).upper() != "TRUE":
        return "inactive"

    if pd.isna(u["expire"]) or datetime.now() > u["expire"]:
        return "expired"

    return "ok"

# ================= WEBHOOK =================
def send_to_webhook(username, password):
    expire = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    try:
        requests.post(WEBHOOK_URL, json={
            "username": username,
            "password": password,
            "expire": expire,
            "trial": True,
            "active": True
        })
    except:
        pass

# ================= SESSION =================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# ================= LOGIN PAGE =================
def login_page():
    st.title("🚗 Veliora Pro")

    st.subheader("Créer un compte")
    new_user = st.text_input("Identifiant", key="create_user")
    new_pass = st.text_input("Mot de passe", type="password", key="create_pass")

    if st.button("Créer compte", key="btn_create"):
        if new_user and new_pass:
            send_to_webhook(new_user, new_pass)
            st.success("Compte créé")
        else:
            st.error("Champs requis")

    st.markdown("---")

    st.subheader("Connexion")
    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pass")

    if st.button("Se connecter", key="btn_login"):

        # ADMIN DIRECT
        if user.strip() == ADMIN_USER and pwd.strip() == ADMIN_PASS:
            st.session_state.logged = True
            st.session_state.admin = True
            st.rerun()

        result = check_login(user, pwd)

        if result == "ok":
            st.session_state.logged = True
            st.session_state.admin = False
            st.rerun()

        elif result == "expired":
            st.error("⛔ Accès expiré")
            st.markdown(f"[💳 S'abonner]({STRIPE_LINK})")

        elif result == "inactive":
            st.error("⛔ Paiement échoué")
            st.markdown(f"[💳 Réactiver]({STRIPE_LINK})")

        else:
            st.error("Identifiant incorrect")

# ================= ADMIN =================
def admin_page():
    st.title("📊 Dashboard Admin")

    df = load_users()

    st.metric("Utilisateurs", len(df))
    st.metric("Actifs", df[df["active"] == True].shape[0])
    st.metric("Expirés", df[df["expire"] < datetime.now()].shape[0])

    st.dataframe(df)

    if st.button("Se déconnecter admin", key="logout_admin"):
        st.session_state.logged = False
        st.session_state.admin = False
        st.rerun()

# ================= APP =================
def app_page():
    st.title("🚗 Cotation véhicule")

    if st.button("Se déconnecter", key="logout_user"):
        st.session_state.logged = False
        st.rerun()

    marque = st.text_input("Marque", key="marque")
    modele = st.text_input("Modèle", key="modele")
    sous_version = st.text_input("Sous-version", key="sous_version")
    finition = st.text_input("Finition", key="finition")
    motorisation = st.text_input("Motorisation", key="motorisation")

    col1, col2 = st.columns(2)

    with col1:
        mois = st.selectbox("Mois", list(range(1,13)), key="mois")
        annee = st.number_input("Année", 1990, 2025, 2019, key="annee")
        carburant = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"], key="carburant")

    with col2:
        boite = st.selectbox("Boîte", ["Manuelle","Automatique"], key="boite")
        techno = st.selectbox("Technologie", ["-", "DSG", "EDC", "CVT", "BVA"], key="techno")
        transmission = st.selectbox("Transmission", ["-", "Traction", "Propulsion", "4x4"], key="transmission")

    etat = st.selectbox("État", ["Bon état", "Excellent état"], key="etat")
    places = st.selectbox("Places", [2,3,4,5,6,7], key="places")
    portes = st.selectbox("Portes", [1,2,3,4,5], key="portes")
    km = st.number_input("Kilométrage", 0, 400000, 90000, key="km")

    departement = st.selectbox("Département", ["75","13","69","59","33","06","44","31","34","Autre"], key="dep")

    options = st.multiselect("Options", ["GPS","Caméra","Cuir","Toit ouvrant","LED","CarPlay"], key="options")

    commission = st.number_input("Commission (€)", 0, 10000, 1000, key="commission")

    if st.button("Calculer l'estimation", key="calc"):

        base = 9000

        if "captur" in modele.lower():
            base = 9000

        age = datetime.now().year - annee
        base -= age * 400

        if km > 80000:
            base -= 700
        if km > 120000:
            base -= 1200

        base += len(options) * 100

        if boite == "Automatique":
            base += 800

        if departement == "75":
            base *= 1.08

        base = int(base)

        annonces = [base*1.05, base, base*0.97]
        prix_marche = int(sum(annonces)/len(annonces) * 0.95)

        prix_bas = int(prix_marche * 0.93)
        prix_haut = int(prix_marche * 1.05)

        st.markdown(f"### 🔻 Vente rapide : {prix_bas} €")
        st.markdown(f"### 📊 Marché : {prix_marche} €")
        st.markdown(f"### 🔺 Haut : {prix_haut} €")

# ================= ROUTER =================
if not st.session_state.logged:
    login_page()
elif st.session_state.admin:
    admin_page()
else:
    app_page()
