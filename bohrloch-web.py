import streamlit as st

st.set_page_config(page_title="Bohr-Assistent Pro", page_icon="⚙️")

st.title("⚙️ Bohr-Assistent mit Visu")

# Eingabe
L = st.number_input("Gesamtlänge der Schiene (cm):", min_value=1.0, value=120.0, step=0.1)

if st.button("BERECHNEN & ZEICHNEN"):
    # Logik für Lochanzahl
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
    
    # Ergebnisse berechnen
    ergebnisse = []
    if n == 1:
        ergebnisse.append(start)
    else:
        schritt = (ende - start) / (n - 1)
        for i in range(n):
            ergebnisse.append(start + i * schritt)

    # --- VISUELLE DARSTELLUNG ---
    st.write("### 📏 Visuelle Vorschau:")
    
    # Wir nutzen HTML/CSS für eine schicke Schiene
    löcher_html = ""
    for pos in ergebnisse:
        prozent = (pos / L) * 100
        # Erstellt einen roten Punkt an der richtigen Stelle
        löcher_html += f'<div style="left:{prozent}%; position:absolute; top:-5px; width:12px; height:12px; background-color:red; border-radius:50%; border:2px solid white; z-index:2;" title="{pos:.1f}cm"></div>'

    st.markdown(f"""
        <div style="position:relative; width:100%; height:40px; margin-top:20px; margin-bottom:40px;">
            <div style="position:absolute; width:100%; height:4px; background-color:#555; top:0; z-index:1;"></div>
            <div style="position:absolute; width:100%; height:20px; background-color:#ddd; border:1px solid #999; top:-8px; border-radius:3px;"></div>
            {löcher_html}
        </div>
    """, unsafe_allow_html=True)
    
    # --- TEXT AUSGABE ---
    c1, c2 = st.columns(2)
    c1.metric("Anzahl Löcher", f"{n} Stk")
    c2.metric("Nutzbare Länge", f"{ende-start:.1f} cm")

    st.write("### 📍 Genaue Positionen:")
    for i, pos in enumerate(ergebnisse):
        st.success(f"Loch {i+1}: **{pos:.2f} cm**")
