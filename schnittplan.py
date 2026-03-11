import streamlit as st

st.set_page_config(page_title="Schnittplan-Profi", page_icon="✂️")

st.title("🪚 Schnittplan-Optimierer")
st.write("Berechne, wie du deine Leisten am effizientesten sägst.")

# Eingabe-Bereich
with st.sidebar:
    st.header("Einstellungen")
    lager_laenge = st.number_input("Lager-Länge (cm):", min_value=10.0, value=200.0, step=1.0)
    schnittbreite = st.number_input("Sägeblatt-Stärke (mm):", value=3) / 10
    st.info("Die Sägeblatt-Stärke wird bei jedem Schnitt abgezogen.")

st.subheader("Welche Maße benötigst du?")
eingabe = st.text_area("Maße in cm eingeben (z.B. 45, 30, 110...):", "50, 80, 40, 110, 30")

if st.button("Schnittplan berechnen"):
    # Daten verarbeiten
    try:
        stuecke = [float(x.strip()) for x in eingabe.replace(",", " ").split() if x.strip()]
        stuecke.sort(reverse=True) # Die großen zuerst einplanen
        
        stangen = []
        
        for stueck in stuecke:
            if stueck > lager_laenge:
                st.error(f"Fehler: Das Stück {stueck} cm ist länger als dein Lager-Material!")
                st.stop()
                
            passt_in_vorhandene = False
            for s in stangen:
                # Prüfen: Summe der Stücke + notwendige Schnitte
                anzahl_schnitte = len(s) 
                if sum(s) + stueck + (anzahl_schnitte * schnittbreite) <= lager_laenge:
                    s.append(stueck)
                    passt_in_vorhandene = True
                    break
            
            if not passt_in_vorhandene:
                stangen.append([stueck])
        
        # Ergebnis-Anzeige
        st.divider()
        st.header(f"Ergebnis: {len(stangen)} Leisten")
        
        for i, stange in enumerate(stangen):
            verbraucht = sum(stange)
            schnitte_verlust = (len(stange) - 1) * schnittbreite
            gesamt_belegt = verbraucht + schnitte_verlust
            rest = lager_laenge - gesamt_belegt
            
            with st.expander(f"Leiste {i+1}: {verbraucht} cm genutzt", expanded=True):
                st.write(f"**Einzelstücke:** {' cm | '.join(map(str, stange))} cm")
                st.write(f"Reststück: **{rest:.1f} cm** (inkl. Verschnitt)")
                st.progress(min(1.0, gesamt_belegt / lager_laenge))

    except ValueError:
        st.error("Bitte nur Zahlen eingeben, getrennt durch Komma oder Leerzeichen.")

