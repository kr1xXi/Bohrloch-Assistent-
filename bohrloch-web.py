import streamlit as st

# Design-Konfiguration
st.set_page_config(page_title="Bohr-Master 3000", page_icon="⚙️")

st.title("⚙️ Werkstatt: Bohr-Rechner")

# Eingabe
L = st.number_input("Gesamtlänge des Werkstücks (cm):", min_value=1.0, value=120.0, step=0.1)

if st.button("BERECHNEN"):
    # Die korrigierte Logik mit 5 Löchern
    if L < 70:
        n = 1
    elif L < 130:
        n = 2
    elif L < 170:
        n = 3
    elif L < 210:
        n = 4
    else:
        n = 5
    
    start = 3.3
    ende = L - 15.0
    
    st.divider()
    st.subheader(f"Ergebnis für {L} cm")
    st.metric(label="Anzahl Löcher", value=f"{n} Stk")

    # Positionen berechnen und anzeigen
    st.write("### Loch-Positionen (ab Nullpunkt):")
    if n == 1:
        st.success(f"📍 Loch 1: {start:.2f} cm")
    else:
        schritt = (ende - start) / (n - 1)
        for i in range(n):
            pos = start + i * schritt
            st.success(f"📍 Loch {i+1}: {pos:.2f} cm")

    # Visuelle Hilfe
    st.progress(min(1.0, (max(0.1, ende/L))))
