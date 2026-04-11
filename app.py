import streamlit as st
import requests
import statistics

MAKE_PRICE_WEBHOOK = "https://hook.eu1.make.com/21t4wtf82gxg97h4mxwqm987hblds6n3"

st.title("Test estimation véhicule")

# Inputs simples
marque = st.text_input("Marque", "Renault")
modele = st.text_input("Modèle", "Clio")
annee = st.number_input("Année", value=2018)
km = st.number_input("Kilométrage", value=90000)

if st.button("Calculer l'estimation"):

    prix_marche_api = None
    prix_calcul = 10000  # base fake pour test

    try:
        query = f"{marque} {modele} {annee} {km} km"

        response = requests.post(
            MAKE_PRICE_WEBHOOK,
            json={"query": query},
            timeout=15
        )

        st.write("DEBUG STATUS:", response.status_code)
        st.write("DEBUG TEXT:", response.text)

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception:
                st.error("Réponse non JSON")
                st.write(response.text)
                st.stop()

            if "result" in data:
                st.success(f"Réponse API: {data['result']}")
                prix_marche_api = int(data["result"])

    except Exception as e:
        st.error(f"Erreur API : {e}")

    # fallback si API marche pas
    prix_annonces = [
        prix_calcul * 0.85,
        prix_calcul * 0.9,
        prix_calcul * 0.95,
        prix_calcul * 1.05,
        prix_calcul * 1.1,
    ]

    if prix_marche_api:
        prix_final = prix_marche_api
    else:
        prix_final = int(statistics.median(prix_annonces))

    st.subheader(f"Prix estimé : {prix_final} €")
