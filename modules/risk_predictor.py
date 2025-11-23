import streamlit as st
import pandas as pd
import pydeck as pdk

def fault_line_risk():
    st.header("⚠️ Bangladesh Fault Line Map (National View)")
    st.info("Major tectonic fault zones surrounding Bangladesh.")

    # Fault Line Data
    fault_data = [
        {"name": "Dauki Fault (Sylhet)", "lat": 25.133, "lon": 91.87, "risk": "Extreme", "color": [255, 0, 0, 200]},
        {"name": "Madhupur Fault (Tangail)", "lat": 24.600, "lon": 90.40, "risk": "High", "color": [255, 69, 0, 200]},
        {"name": "Tripura Fold Belt (CTG)", "lat": 23.500, "lon": 91.50, "risk": "Moderate", "color": [255, 165, 0, 200]},
        {"name": "Assam Seismic Zone (North)", "lat": 26.100, "lon": 92.00, "risk": "High", "color": [200, 0, 0, 200]}
    ]
    
    df = pd.DataFrame(fault_data)

    # Layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=25000, # Large radius to show danger zones
        pickable=True,
    )

    # BANGLADESH-FOCUSED VIEW (Country Level)
    view_state = pdk.ViewState(
        latitude=23.6850, # Center of BD
        longitude=90.3563,
        zoom=6.4,         # Shows whole country
        pitch=0,
    )

    tooltip = {
        "html": "<b>{name}</b><br/>Risk Level: {risk}",
        "style": {"color": "white", "background-color": "#333", "padding": "8px", "borderRadius": "4px"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    st.pydeck_chart(deck)

    st.subheader("📌 Fault Line Risk Overview")
    st.table(df[["name", "risk"]])
    
