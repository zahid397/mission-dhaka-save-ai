import streamlit as st
import requests
import pandas as pd
import datetime
import pydeck as pdk

def quake_monitor():
    st.header("🌐 Bangladesh-Focused Live Earthquake Monitor")
    st.info("Live data from USGS, filtered specifically for Bangladesh & surrounding border regions.")

    # USGS API (Past 2.5+ Magnitude, Last 24 Hours)
    URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    try:
        # Fetch Data
        with st.spinner("Fetching live satellite data..."):
            response = requests.get(URL)
            if response.status_code != 200:
                st.error("❌ Connection Error: Unable to fetch data.")
                return
            
            data = response.json()
            quakes = []

            for q in data["features"]:
                props = q["properties"]
                coords = q["geometry"]["coordinates"]

                # Time Parsing
                ts = props["time"] / 1000
                time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

                quakes.append([
                    props["mag"],
                    props["place"],
                    time_str,
                    coords[1],   # Latitude
                    coords[0]    # Longitude
                ])

        # Create DataFrame
        df = pd.DataFrame(quakes, columns=["Mag", "Location", "Time", "lat", "lon"])

        # 🇧🇩 REGION FILTER (Bangladesh + Border Areas)
        # Lat: 20.0 to 27.5 | Lon: 88.0 to 93.0 covers BD + Tripura/Assam/West Bengal borders
        bd_df = df[
            (df["lat"] >= 20.0) &
            (df["lat"] <= 27.5) &
            (df["lon"] >= 88.0) &
            (df["lon"] <= 93.0)
        ]

        # 1. Display Data Table
        st.subheader("🇧🇩 Regional Activity (Last 24 Hours)")
        
        if bd_df.empty:
            st.success("✅ No significant earthquakes detected in Bangladesh region recently.")
        else:
            # Highlight high magnitude
            st.warning(f"⚠ Detected {len(bd_df)} tremors in the region!")
            st.dataframe(
                bd_df.style.highlight_max(axis=0, subset=["Mag"], color='red'),
                use_container_width=True
            )

        # 2. Bangladesh-Focused Map
        st.subheader("🗺️ Live Geographic View")

        # Map Layer (Red circles for quakes)
        layer = pdk.Layer(
            "ScatterplotLayer",
            bd_df if not bd_df.empty else df, # Show global if BD is empty (optional fallback) or just empty map
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 200]',
            get_radius=25000,
            pickable=True
        )

        # Perfect Zoom for Bangladesh
        view = pdk.ViewState(
            latitude=23.7,
            longitude=90.4,
            zoom=6.7,
            pitch=0
        )

        # Tooltip
        tooltip = {
            "html": "<b>Location:</b> {Location}<br/><b>Magnitude:</b> {Mag} R<br/><b>Time:</b> {Time}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            map_style="mapbox://styles/mapbox/outdoors-v11", # Changed to 'outdoors' for better visibility
            tooltip=tooltip
        )

        st.pydeck_chart(deck)

        # Note
        st.caption("Data Source: USGS Real-time Feed. Monitoring zone: Lat 20-27.5, Lon 88-93.")

    except Exception as e:
        st.error(f"⚠ System Error: {e}")
