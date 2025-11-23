import streamlit as st
import pandas as pd
import pydeck as pdk

def fault_line_risk():
    st.header("⚠️ Bangladesh Fault Line Map")
    st.info("Major tectonic fault lines threatening Dhaka.")

    # 1. Fault Line Coordinates (Approximate Centers for Visualization)
    fault_data = [
        {"name": "Dauki Fault", "lat": 25.133, "lon": 91.87, "risk": "Extreme", "color": [255, 0, 0, 200]},
        {"name": "Madhupur Fault", "lat": 24.600, "lon": 90.40, "risk": "High (Close to Dhaka)", "color": [255, 69, 0, 200]},
        {"name": "Tripura Fold Belt", "lat": 23.500, "lon": 91.50, "risk": "Moderate", "color": [255, 165, 0, 200]},
        {"name": "Assam Seismic Zone", "lat": 26.100, "lon": 92.00, "risk": "High", "color": [200, 0, 0, 200]},
    ]
    
    df = pd.DataFrame(fault_data)

    # 2. Display Map using PyDeck
    st.subheader("🗺️ Active Fault Lines")
    
    # Layer for Fault Points
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=20000,  # 20km radius circles
        pickable=True,
    )

    # View State focused on Bangladesh
    view_state = pdk.ViewState(
        latitude=24.0,
        longitude=90.5,
        zoom=6.5,
        pitch=0,
    )

    # Tooltip
    tooltip = {
        "html": "<b>{name}</b><br/>Risk Level: {risk}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    st.pydeck_chart(r)

    # 3. Risk Details Table
    st.divider()
    st.subheader("📋 Risk Analysis by Zone")
    st.table(df[["name", "risk"]])
    
    st.markdown("""
    > **Note:** **Madhupur Fault** is the most critical for Dhaka due to its proximity (Tangail/Mymensingh area). 
    > **Dauki Fault** (Sylhet Border) is capable of generating 8.0+ magnitude earthquakes.
    """)
  
