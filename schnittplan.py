import streamlit as st

st.set_page_config(page_title="Schnittplan-Profi", page_icon="✂️")

st.title("🪚 Schnittplan-Optimierer")
st.write("Berechne, wie du deine Führungsschienen am effizientesten sägst.")

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
        # Die Eingabe wird jetzt schlauer verarbeitet
        stuecke = []
        # Wir teilen die Eingabe bei Komma oder Leerzeichen
        roh_daten = eingabe.replace(",", " ").split()
        
        for daten in roh_daten:
        if "x" in daten.lower():
                # Wenn ein 'x' drin ist, z.B. "6x120"
                anzahl, mass = daten.lower().split("x")
                stuecke.extend([float(mass)] * int(anzahl))
        else:
                # Normales Maß, z.B. "120"
                stuecke.append(float(daten))
        
        stuecke.sort(reverse=True) # Die großen zuerst einplanen
        
        # ... ab hier geht der Rest vom Code (stangen = []) ganz normal weiter

        
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

