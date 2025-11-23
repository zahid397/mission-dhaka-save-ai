import streamlit as st
import requests
import pandas as pd
import datetime

def quake_monitor():
    st.header("🌐 Live Earthquake Monitor (Last 24h)")
    
    # USGS API (2.5+ Magnitude, Past Day)
    URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    try:
        response = requests.get(URL)
        data = response.json()
        quakes = []

        for q in data["features"]:
            props = q["properties"]
            coords = q["geometry"]["coordinates"]
            # Time conversion
            ts = props["time"] / 1000
            time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

            quakes.append([props["mag"], props["place"], time_str, coords[1], coords[0]])

        df = pd.DataFrame(quakes, columns=["Mag", "Location", "Time", "lat", "lon"])

        if not df.empty:
            # Metrics
            c1, c2 = st.columns(2)
            c1.metric("Total Quakes", len(df))
            c2.metric("Max Magnitude", df["Mag"].max())

            # Map
            st.map(df, size=20, color='#FF4B4B')
            
            # Bangladesh Filter
            st.subheader("🇧🇩 Region Activity")
            bd = df[df["Location"].str.contains("Bangladesh|India|Myanmar", case=False, na=False)]
            if not bd.empty:
                st.dataframe(bd)
            else:
                st.success("No major quakes near Bangladesh in last 24h.")
        else:
            st.warning("No data available.")

    except Exception as e:
        st.error(f"Data Fetch Error: {e}")
      
