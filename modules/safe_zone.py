import streamlit as st
import pandas as pd
import pydeck as pdk

def safe_zone_finder():
    st.header("🧭 Safe Zone & Risk Map")

    # Sample Data
    data = {
        "Building_id": ["B1", "B2", "B3"],
        "Area": ["Dhanmondi", "Mirpur", "Uttara"],
        "Risk": ["High", "Medium", "Low"],
        "lat": [23.7461, 23.8042, 23.8728],
        "lon": [90.3742, 90.3667, 90.4043]
    }
    df = pd.DataFrame(data)

    # Color logic
    def get_color(risk):
        return [255, 0, 0, 160] if risk == "High" else [0, 255, 0, 160]
    
    df["color"] = df["Risk"].apply(get_color)

    # Map
    layer = pdk.Layer(
        "ScatterplotLayer", df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=800, pickable=True
    )
    
    view = pdk.ViewState(latitude=23.8103, longitude=90.4125, zoom=10)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip={"text": "{Area}\nRisk: {Risk}"}))

    st.subheader("✅ Recommended Safe Zones")
    st.table(df[df["Risk"] == "Low"])
  
