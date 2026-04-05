if st.button("Calculer l'estimation"):

    age = datetime.now().year - int(annee)

    # 🔥 1. PRIX NEUF ESTIMÉ (base réaliste)
    prix_neuf = 25000

    if marque.lower() in ["bmw", "mercedes", "audi"]:
        prix_neuf = 45000

    if "clio" in modele.lower() or "208" in modele.lower():
        prix_neuf = 18000

    if "3008" in modele.lower() or "tiguan" in modele.lower():
        prix_neuf = 32000

    if carburant == "Électrique":
        prix_neuf += 8000

    if carburant == "Hybride":
        prix_neuf += 4000

    # 🔥 2. DÉCOTE RÉELLE PRO
    # -20% la première année puis -10%/an
    valeur = prix_neuf * 0.8
    for i in range(age - 1):
        valeur *= 0.90

    # 🔥 3. KILOMÉTRAGE
    km_moyen = age * 15000
    ecart_km = km - km_moyen

    if ecart_km > 0:
        valeur -= (ecart_km / 10000) * 500
    else:
        valeur += abs(ecart_km / 10000) * 300

    # 🔥 4. BONUS OPTIONS (réalistes)
    bonus = 0
    for opt in options:
        if opt in ["Toit panoramique", "Caméra 360"]:
            bonus += 300
        elif opt in ["GPS / Navigation", "Caméra de recul"]:
            bonus += 150
        else:
            bonus += 80

    valeur += bonus

    # 🔥 5. AJUSTEMENTS MARCHÉ
    if boite == "Automatique":
        valeur *= 1.05

    if carburant == "Diesel":
        valeur *= 0.95

    # 🔥 6. PLANCHER
    if valeur < 3000:
        valeur = 3000

    prix_bas = int(valeur * 0.9)
    prix_haut = int(valeur * 1.1)

    st.markdown(f"""
## 📊 COTATION MARCHÉ RÉALISTE

👉 Véhicule : {marque} {modele} ({annee})  
📍 {km} km

💰 Prix marché particulier :

➡️ {prix_bas} € → {prix_haut} €
""")
