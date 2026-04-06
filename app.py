import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ================= CONFIG =================

PAYMENT_LINK = "https://buy.stripe.com/test_7sYcN67QC1lbcmneek9fW00"

# 👉 REMPLACE PAR TON GOOGLE SHEET (CSV PUBLIC)
SHEET_URL = "https://docs.google.com/spreadsheets/d/TON_ID/export?format=csv"

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ================= LOAD SHEET =================

@st.cache_data(ttl=60)
def load_sheet():
    try:
        df = pd.read_csv(SHEET_URL)
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

# ================= LOGIN UI =================

st.title("🔐 Accès Veliora Pro")

tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

# ================= CONNEXION =================

with tab1:
    user = st.text_input("Utilisateur", key="login_user")
    pwd = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter", key="login_btn"):

        if user == "utilisateur12345" and pwd == "1234":

            df = load_sheet()

            # 👉 Paiement détecté
            if user in df["email"].astype(str).values:
                st.session_state.auth = True
                st.session_state.user = user
                st.success("✅ Accès activé (paiement détecté)")
                st.rerun()

            # 👉 Sinon essai
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
                    st.error("❌ Aucun accès actif")
        else:
            st.error("❌ Identifiants incorrects")

# ================= ESSAI GRATUIT =================

with tab2:

    if st.session_state.trial_start:
        st.info(
            f"Essai actif depuis : {st.session_state.trial_start.strftime('%d/%m/%Y')}"
        )

    if st.button("Activer essai 7 jours", key="trial_btn"):
        st.session_state.trial_start = datetime.now()
        st.session_state.auth = True
        st.session_state.user = "utilisateur12345"
        st.success("✅ Essai activé pour 7 jours")
        st.rerun()

# ================= BLOQUAGE =================

if not st.session_state.auth:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

st.success(f"Connecté en tant que {st.session_state.user}")

st.write("👉 Paiement + essai + accès automatique actifs")

# Bouton paiement toujours visible si pas encore payé
df = load_sheet()

if st.session_state.user not in df["email"].astype(str).values:
    st.warning("🔒 Compte non abonné")
    st.markdown(f"[💳 S’abonner 99€/an]({PAYMENT_LINK})")

# Déconnexion
if st.button("Se déconnecter"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()
