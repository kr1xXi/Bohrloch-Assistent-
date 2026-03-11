import streamlit as st

st.set_page_config(page_title="Schnittplan-Profi", page_icon="✂️")

st.title("🪚 Schienen-Optimierer (6m)")

# Einstellungen in der Seitenleiste
with st.sidebar:
    st.header("⚙️ Werkstatt-Einst.")
    roh_laenge = st.number_input("Schienen-Länge (cm):", value=600.0)
    anschnitt = st.number_input("Anschnitt vorne (cm):", value=3.0)
    saege = st.number_input("Sägeblatt (mm):", value=3.0) / 10
    min_rest = st.number_input("Rest nutzbar ab (cm):", value=15.0)
    
    # Nutzbare Länge pro Schiene
    lager = roh_laenge - anschnitt
    st.write(f"---")
    st.write(f"📏 Pro Schiene nutzbar: **{lager} cm**")

st.subheader("Benötigte Maße")
st.caption("Beispiel: 5x120, 2x85, 40")
eingabe = st.text_area("Eingabe:", "10x120, 5x45")

if st.button("BERECHNEN"):
    try:
        # 1. Daten einlesen
        stuecke = []
        roh_daten = eingabe.replace(",", " ").split()
        for d in roh_daten:
            if "x" in d.lower():
                anz, mass = d.lower().split("x")
                stuecke.extend([float(mass)] * int(anz))
            else:
                stuecke.append(float(d))
        
        stuecke.sort(reverse=True)
        
        # 2. Auf Schienen verteilen
        schienen = []
        for s in stuecke:
            if s > lager:
                st.error(f"⚠️ Teil {s}cm ist länger als nutzbar ({lager}cm)!")
                st.stop()
            
            gepackt = False
            for leiste in schienen:
                belegt = sum(leiste) + (len(leiste) * saege)
                if belegt + s <= lager:
                    leiste.append(s)
                    gepackt = True
                    break
            if not gepackt:
                schienen.append([s])
        
        # 3. Ergebnis-Zusammenfassung
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Schienen GESAMT", f"{len(schienen)} Stk")
        
        gesamt_meter = len(schienen) * (roh_laenge / 100)
        c2.metric("Meter Einkauf", f"{gesamt_meter:.2f} m")
        
        # Verschnitt berechnen
        verschnitt_cm = (len(schienen) * lager) - sum(stuecke)
        prozent = (verschnitt_cm / (len(schienen) * lager)) * 100
        c3.metric("Verschnitt", f"{prozent:.1f} %")

        # 4. Detail-Schnittplan
        st.write("### 📋 Dein Schnittplan")
        for i, leiste in enumerate(schienen):
            belegt_durch_teile = sum(leiste)
            belegt_durch_saege = (len(leiste) - 1) * saege
            rest = lager - belegt_durch_teile - belegt_durch_saege
            
            with st.expander(f"Schiene {i+1} (Rest: {rest:.1f} cm)", expanded=True):
                st.write(f"**Schnitte:** {' | '.join(map(str, leiste))} cm")
                st.progress(min(1.0, (lager-rest)/lager))
                
                if rest >= min_rest:
                    st.success(f"✅ Nutzbares Reststück: {rest:.1f} cm")
                else:
                    st.warning(f"🗑️ Abfall: {rest:.1f} cm")

    except Exception:
        st.error("Fehler! Bitte Format prüfen (z.B. 5x120).")
