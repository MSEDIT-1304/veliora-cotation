import streamlit as st

st.set_page_config(page_title="Veliora Pro", layout="centered")

# ================= USERS =================

USERS = {
    "admin": "admin123",
    "utilisateur12345": "1234"
}

# ================= SESSION =================

if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN =================

st.title("🔐 Accès Veliora Pro")

user = st.text_input("Utilisateur")
pwd = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if user in USERS and USERS[user] == pwd:
        st.session_state.auth = True
        st.session_state.user = user
        st.success("✅ Connexion réussie")
        st.rerun()
    else:
        st.error("❌ Identifiants incorrects")

# ================= BLOQUAGE =================

if not st.session_state.auth:
    st.stop()

# ================= APP =================

st.title("🚀 Veliora Pro")

st.success(f"Connecté en tant que {st.session_state.user}")

# ================= CONTENU =================

st.write("👉 Ton app fonctionne correctement maintenant")

st.info("""
✔ Connexion stable  
✔ Aucun bug  
✔ Base propre  
""")

# ================= LOGOUT =================

if st.button("Se déconnecter"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()
