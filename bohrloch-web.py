import streamlit as st

# Design-Konfiguration
st.set_page_config(page_title="Bohr-Master 3000", page_icon="⚙️", layout="centered")

# Eigenes CSS für noch schöneres Design (Farben, Schrift)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; height: 3em; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚙️ Führungsschienen: Bohr-Rechner")
st.write("Berechne präzise Lochabstände für deine Werkstücke.")

# Eingabe-Bereich
with st.container():
    st.subheader("Eingabe")
    laenge = st.number_input("Gesamtlänge des Werkstücks (cm):", min_value=1.0, value=120.0, step=0.1)

# Berechnung starten
if st.button("BERECHNEN"):
    # Deine bewährte Logik
    if laenge < 70: n = 1
    elif laenge < 130: n = 2
    elif laenge < 170: n = 3
    else: n = 4
    
    start = 3.3
    ende = laenge - 15.0
    
    st.divider()
    
    # Ergebnisse anzeigen
    st.subheader(f"Ergebnis für {laenge} cm")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Anzahl Löcher", value=f"{n} Stk")
    with col2:
        st.metric(label="End-Punkt", value=f"{ende:.2f} cm")

    # Die genauen Positionen in einer schicken Liste
    st.markdown("### Loch-Positionen (ab Nullpunkt):")
    if n == 1:
        st.info(f"📍 Loch 1: **{start:.2f} cm**")
    else:
        schritt = (ende - start) / (n - 1)
        for i in range(n):
            pos = start + i * schritt
            st.success(f"📍 Loch {i+1}: **{pos:.2f} cm**")

    # Visuelle Darstellung als Fortschrittsbalken
    st.write("Visuelle Verteilung:")
    st.progress(min(1.0, (ende/laenge)))
