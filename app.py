import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ================= CONFIG =================

PAYMENT_LINK = "https://buy.stripe.com/test_7sYcN67QC1lbcmneek9fW00"

# 👉 TON GOOGLE SHEET (remplace avec ton lien CSV)
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

# ================= LOGIN =================

st.title("🔐 Accès Veliora Pro")

tab1, tab2 = st.tabs(["Connexion", "Essai gratuit 7 jours"])

# ---------- CONNEXION ----------
with tab1:
    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if user == "utilisateur12345" and pwd == "1234":

            df = load_sheet()

            # 👉 Vérifie si l'utilisateur a payé
            if user in df["email"].values:
                st.session_state.auth = True
                st.session_state.user = user
                st.success("✅ Accès activé (paiement détecté)")
                st.rerun()

            # 👉 sinon vérifie essai
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
                    st.error("Aucun accès actif")
        else:
            st.error("Identifiants incorrects")

# ---------- ESSAI GRATUIT ----------
with tab2:
    if st.button("Activer essai 7 jours"):
        st.session_state.trial_start = datetime.now()
        st.success("✅ Essai activé")
        st.rerun()

# ================= BLOQUAGE =================

if not st.session_state.auth:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

st.success(f"Connecté en tant que {st.session_state.user}")

st.write("👉 Ton outil fonctionne maintenant avec paiement automatique")

if st.button("Se déconnecter"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()
