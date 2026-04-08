if st.button("Calculer l'estimation"):

    base = 12000  # 🔥 base réaliste marché FR

    age = datetime.now().year - annee

    # ---------------- AJUSTEMENTS MARQUE ----------------
    if marque.lower() in ["bmw","audi","mercedes"]:
        base += 4000
    elif marque.lower() in ["renault","peugeot","citroen"]:
        base += 1500

    # ---------------- BOITE ----------------
    if boite == "Automatique":
        base += 1500

    # ---------------- CARBURANT ----------------
    if carburant == "Hybride":
        base += 2000
    elif carburant == "Électrique":
        base += 4000

    # ---------------- AGE (moins violent) ----------------
    base -= age * 500

    # ---------------- KILOMETRAGE ----------------
    if km > 80000:
        base -= 800
    if km > 120000:
        base -= 1200
    if km > 160000:
        base -= 1500

    # ---------------- OPTIONS ----------------
    base += len(options) * 150

    # ---------------- BONUS SUV (type Captur) ----------------
    if "captur" in modele.lower():
        base += 1000

    # ---------------- AJUSTEMENT FINAL ----------------
    prix_marche = int(base)

    # 🔥 COHERENCE MARCHE (plancher minimum réaliste)
    if prix_marche < 7000:
        prix_marche = 7000

    # ---------------- PRIX ----------------
    prix_bas = int(prix_marche * 0.93)
    prix_haut = int(prix_marche * 1.08)

    # 🔥 PRIX GARAGE (marge pro)
    prix_garage = int(prix_bas - 1000)

    # ---------------- AFFICHAGE ----------------
    st.markdown(f"### 💰 Prix bas : {prix_bas} €")
    st.markdown(f"### 📊 Prix marché : {prix_marche} €")
    st.markdown(f"### 🚀 Prix haut : {prix_haut} €")
    st.markdown(f"### 🏪 Prix garage : {prix_garage} €")
