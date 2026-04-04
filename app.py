if not st.session_state.auth:
    st.title("🔐 VELIORA COTATION")
    pwd = st.text_input("Mot de passe", type="password")

    if pwd == PASSWORD:
        st.session_state.auth = True
        st.rerun()

    st.stop()
