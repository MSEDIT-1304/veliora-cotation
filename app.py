# =========================
# 📅 DATE PREMIÈRE MISE EN CIRCULATION
# =========================

st.markdown("### 📅 Date de première mise en circulation")
st.caption("Indiquez le mois et l'année exacts du véhicule")

col_date1, col_date2 = st.columns(2)

with col_date1:
    mois = st.selectbox(
        "Mois",
        list(range(1, 13)),
        index=0
    )

with col_date2:
    annee = st.selectbox(
        "Année",
        list(range(1990, datetime.now().year + 1)),
        index=len(list(range(1990, datetime.now().year + 1))) - 1
    )

# =========================
# 📊 INFOS
# =========================

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    km = st.number_input("Kilométrage", 0, 300000, 50000)

with col4:
    departement = st.text_input("Département")
    vendeur = st.text_input("Nom vendeur")

# =========================
# 💰 CALCUL
# =========================

st.markdown("---")

if st.button("Calculer la cotation"):

    try:
        # âge précis
        age = datetime.now().year - annee + (datetime.now().month - mois)/12

        base = 20000

        # décote âge
        decote_age = base * 0.08 * age

        # décote km
        km_moyen = age * 15000
        decote_km = (km - km_moyen) * 0.05

        # bonus carburant (sécurisé)
        bonus_carburant = 0
        if carburant:
            if "electrique" in carburant.lower():
                bonus_carburant = 2000
            elif "hybride" in carburant.lower():
                bonus_carburant = 1000
            elif "diesel" in carburant.lower():
                bonus_carburant = -500

        # bonus boîte
        bonus_boite = 0
        if boite:
            if "auto" in boite.lower():
                bonus_boite = 800

        resultat = base - decote_age - decote_km + bonus_carburant + bonus_boite

        st.success(f"💰 Valeur estimée : {int(resultat)} €")

    except:
        st.error("Erreur dans les données")
