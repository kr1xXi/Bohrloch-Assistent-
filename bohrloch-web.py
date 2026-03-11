import streamlit as st

st.set_page_config(page_title="Bohr-Assistent Pro", page_icon="⚙️")

st.title("⚙️ Bohr-Assistent")

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
    
    # Absolute Positionen berechnen
    pos_absolut = []
    if n == 1:
        pos_absolut.append(start)
    else:
        schritt = (ende - start) / (n - 1)
        for i in range(n):
            pos_absolut.append(start + i * schritt)

    # --- VISUELLE DARSTELLUNG ---
    st.write("### 📏 Visuelle Vorschau:")
    löcher_html = ""
    for pos in pos_absolut:
        prozent = (pos / L) * 100
        löcher_html += f'<div style="left:{prozent}%; position:absolute; top:-5px; width:12px; height:12px; background-color:red; border-radius:50%; border:2px solid white; z-index:2;"></div>'

    st.markdown(f"""
        <div style="position:relative; width:100%; height:40px; margin-top:20px; margin-bottom:40px;">
            <div style="position:absolute; width:100%; height:4px; background-color:#555; top:0; z-index:1;"></div>
            <div style="position:absolute; width:100%; height:20px; background-color:#ddd; border:1px solid #999; top:-8px; border-radius:3px;"></div>
            {löcher_html}
        </div>
    """, unsafe_allow_html=True)
    
    # --- AUSGABE ---
    col1, col2 = st.columns(2)
    col1.metric("Anzahl Löcher", f"{n} Stk")
    if n > 1:
        abstand_zwischen = (ende - start) / (n - 1)
        col2.metric("Lochabstand (Mitte)", f"{abstand_zwischen:.2f} cm")

    st.write("### 📍 Bohr-Maße:")
    
    # Tabelle für die Maße
    tab_abs, tab_kette = st.tabs(["Absolut (ab 0 cm)", "Kettenmaß (Loch zu Loch)"])
    
    with tab_abs:
        for i, pos in enumerate(pos_absolut):
            st.write(f"Loch {i+1}: **{pos:.2f} cm**")
            
    with tab_kette:
        st.write(f"1. Loch bei: **{start} cm**")
        if n > 1:
            abstand = (ende - start) / (n - 1)
            for i in range(1, n):
                st.info(f"➡️ Dann jeweils **{abstand:.2f} cm** weitermessen")
        else:
            st.write("Nur ein Loch vorhanden.")

    st.caption(f"Info: Das letzte Loch sitzt bei {pos_absolut[-1]:.2f} cm (entspricht {L - pos_absolut[-1]:.1f} cm vom Ende).")
