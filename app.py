import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ================= CONFIG =================

PAYMENT_LINK = "https://buy.stripe.com/test_7sYcN67QC1lbcmneek9fW00"

# 👉 IMPORTANT : remplace par ton vrai Google Sheet (CSV public)
SHEET_URL = "https://docs.google.com/spreadsheets/d/TON_ID/export?format=csv"

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ================= LOAD GOOGLE SHEET =================

@st.cache_data(ttl=30)
def load_sheet():
    try:
        df = pd.read_csv(SHEET_URL)
        df["email"] = df["email"].astype(str)
        return df
    except:
        return pd.DataFrame(columns=["email", "montant", "paiement_id"])

# ================= SESSION =================

if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

if "trial_start" not in st.session_state:
    st.session_state.trial_start = None

# ================= UI =================

st.title("🔐 Accès Veliora Pro")

tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

# ================= CONNEXION =================

with tab1:
    user = st.text_input("Email", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter", key="login_btn"):

        if not user:
            st.error("❌ Entre un email")
            st.stop()

        if pwd != "1234":
            st.error("❌ Mot de passe incorrect")
            st.stop()

        df = load_sheet()

        # 🔥 Vérification paiement (case insensitive)
        emails = df["email"].str.lower().values

        if user.lower() in emails:
            st.session_state.auth = True
            st.session_state.user = user
            st.success("✅ Accès activé (paiement détecté)")
            st.rerun()

        # 👉 SINON = ESSAI
        else:
            if st.session_state.trial_start:

                expire = st.session_state.trial_start + timedelta(days=7)

                if datetime.now() > expire:
                    st.error("⛔ Essai expiré")
                    st.markdown(f"[💳 S’abonner 99€/an]({PAYMENT_LINK})")
                    st.stop()
                else:
                    st.session_state.auth = True
                    st.session_state.user = user
                    st.success("✅ Accès essai actif")
                    st.rerun()

            else:
                st.error("❌ Aucun accès actif (active l'essai ou abonne-toi)")

# ================= ESSAI GRATUIT =================

with tab2:

    if st.session_state.trial_start:
        expire = st.session_state.trial_start + timedelta(days=7)

        if datetime.now() < expire:
            st.info(f"Essai actif jusqu'au : {expire.strftime('%d/%m/%Y')}")
        else:
            st.warning("Essai expiré")

    if st.button("Activer essai 7 jours", key="trial_btn"):
        st.session_state.trial_start = datetime.now()
        st.session_state.auth = True
        st.session_state.user = "essai"
        st.success("✅ Essai activé pour 7 jours")
        st.rerun()

# ================= BLOQUAGE =================

if not st.session_state.auth:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

st.success(f"Connecté en tant que {st.session_state.user}")

df = load_sheet()
emails = df["email"].str.lower().values

# ================= STATUT ABONNEMENT =================

if st.session_state.user.lower() in emails:
    st.success("💎 Abonnement actif")
else:
    st.warning("🔒 Compte non abonné")
    st.markdown(f"[💳 S’abonner 99€/an]({PAYMENT_LINK})")

# ================= CONTENU =================

st.write("👉 Ton SaaS est maintenant connecté au paiement automatiquement")

st.info("✔️ Essai 7 jours\n✔️ Paiement Stripe\n✔️ Activation automatique")

# ================= LOGOUT =================

if st.button("Se déconnecter"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()
