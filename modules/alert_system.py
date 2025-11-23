import streamlit as st
import requests
import math
import pandas as pd
from datetime import datetime

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# Bangladesh District Coordinates
districts = {
    "Dhaka": (23.8103, 90.4125),
    "Sylhet": (24.8949, 91.8687),
    "Chittagong": (22.3569, 91.7832),
    "Rajshahi": (24.3636, 88.6241),
    "Khulna": (22.8456, 89.5403),
    "Barishal": (22.7010, 90.3535),
    "Rangpur": (25.7439, 89.2752),
    "Mymensingh": (24.7471, 90.4203)
}

def dist(lat1, lon1, lat2, lon2):
    """Calculate distance using Haversine formula"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

def estimate_intensity(mag, distance_km):
    """Estimate Shindo Scale Intensity based on Magnitude & Distance"""
    if distance_km > 600: 
        return "0 (Not Felt)", "#808080", "white" # Grey
    
    # Heuristic Formula
    impact_score = mag - (distance_km / 100)
    
    if impact_score >= 5.5:
        return "Shindo 5+ (Severe)", "#FF0000", "white" # Red
    elif impact_score >= 4.5:
        return "Shindo 4 (Strong)", "#FF8C00", "white" # Dark Orange
    elif impact_score >= 3.5:
        return "Shindo 3 (Moderate)", "#FFD700", "black" # Yellow
    else:
        return "Shindo 1-2 (Weak)", "#32CD32", "white" # Green

def japan_style_alert():
    st.header("⏱ Nationwide Intensity Forecast (Japan-Style)")
    st.info("Visual Alert System: Select your location to see specific impact.")

    # 1. District Selector
    col_sel, col_tog = st.columns([3, 1])
    with col_sel:
        selected_district = st.selectbox("📍 Select your Location", list(districts.keys()))
    with col_tog:
        simulation = st.toggle("🛠 Test Mode", value=False)
        
    USER_LAT, USER_LON = districts[selected_district]

    try:
        # 2. Data Fetching (Real vs Simulation)
        if simulation:
            # Scenario: 7.2 Magnitude Earthquake at Dauki Fault
            mag, place = 7.2, "Simulation: Dauki Fault Zone"
            q_lat, q_lon = 25.13, 91.85 
        else:
            data = requests.get(USGS_URL).json()
            if not data["features"]:
                st.success("✅ No earthquakes detected globally in the last hour.")
                return
            q = data["features"][0]
            mag = q["properties"]["mag"]
            place = q["properties"]["place"]
            q_lon, q_lat, _ = q["geometry"]["coordinates"]

        # 3. Calculations
        distance = dist(USER_LAT, USER_LON, q_lat, q_lon)
        intensity_label, bg_color, text_color = estimate_intensity(mag, distance)
        
        # S-Wave Arrival Time (Approx speed 4 km/s)
        seconds_to_impact = distance / 4.0

        # 4. Display Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("📍 Epicenter", place)
        c2.metric(f"📏 Dist. to {selected_district}", f"{int(distance)} km")
        c3.metric("⚛ Magnitude", f"{mag}")

        st.divider()

        # 5. Visual Map (User vs Quake)
        map_data = pd.DataFrame({
            'lat': [USER_LAT, q_lat],
            'lon': [USER_LON, q_lon],
            'type': ['You', 'Epicenter'],
            'size': [100, 500], # User small, Quake big
            'color': [[0, 0, 255, 200], [255, 0, 0, 200]] # Blue vs Red
        })
        st.map(map_data, size='size', color='color')

        # 6. The "Japan Style" Alert Card
        st.subheader(f"📉 Impact Forecast for {selected_district}")

        html_code = f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            font-family: sans-serif;">
            
            <p style="margin:0; font-size:16px; opacity:0.9;">PREDICTED INTENSITY</p>
            <h1 style="margin:5px 0; font-size: 40px;">{intensity_label}</h1>
            
            <hr style="border: 1px solid {text_color}; opacity: 0.3; margin: 15px 0;">
            
            <p style="margin:0; font-size:18px;">Destructive S-Waves Arriving In:</p>
            <h2 style="margin:5px 0; font-size: 35px;">{int(seconds_to_impact)} Seconds</h2>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)

        # 7. Action Guidance
        if "Red" in bg_color or "Orange" in bg_color: # Checking hex logic visually
            if "Shindo 5" in intensity_label or "Shindo 4" in intensity_label:
                st.error("⚠️ **CRITICAL WARNING:** Drop, Cover, and Hold On! Do not run outside immediately.")
        else:
            st.success("🟢 **SAFE:** You might feel a light shake, but no damage is expected.")

    except Exception as e:
        st.error(f"⚠ System Error: {e}")

