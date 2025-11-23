import streamlit as st
import requests
import math
from datetime import datetime

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

def dist(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

def estimate_intensity(mag, distance_km):
    """
    Estimate Shindo Scale Intensity based on Magnitude & Distance.
    This is a heuristic approximation for the demo.
    """
    if distance_km > 600: return "0 (Not Felt)", "grey"
    
    # Simplified logic
    impact_score = mag - (distance_km / 100)
    
    if impact_score >= 5.5:
        return "Shindo 5+ (Strong)", "red"
    elif impact_score >= 4.5:
        return "Shindo 4 (Moderate)", "orange"
    elif impact_score >= 3.5:
        return "Shindo 3 (Light)", "yellow"
    else:
        return "Shindo 1-2 (Weak)", "green"

def japan_style_alert():
    st.header("⏱ Intensity Estimator (Silent Alert)")
    st.info("Visual Alert Only - No Sound to prevent panic.")
    
    DHAKA_LAT, DHAKA_LON = 23.8103, 90.4125
    
    # Toggle for Demo
    simulation = st.toggle("🛠 Simulation Mode", value=False)

    try:
        if simulation:
            # Demo Scenario: 6.8 Mag at Sylhet (240km away)
            mag, place, q_lat, q_lon = 6.8, "Simulation: Dauki Fault", 25.1, 91.8
        else:
            data = requests.get(USGS_URL).json()
            if not data["features"]:
                st.success("✅ No earthquakes currently detected.")
                return
            q = data["features"][0]
            mag = q["properties"]["mag"]
            place = q["properties"]["place"]
            q_lon, q_lat, _ = q["geometry"]["coordinates"]

        # Calculate Distance & Intensity
        distance = dist(DHAKA_LAT, DHAKA_LON, q_lat, q_lon)
        intensity_label, color = estimate_intensity(mag, distance)
        
        # Display Core Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("📍 Location", place)
        c2.metric("📏 Dist. to Dhaka", f"{int(distance)} km")
        c3.metric("⚛ Magnitude", mag)

        st.divider()

        # Visual Intensity Card (The New Feature)
        st.subheader("📉 Dhaka Shaking Forecast")
        
        html_code = f"""
        <div style="
            background-color: {color}; 
            color: black; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center; 
            font-weight: bold;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
            <h2 style='margin:0;'>{intensity_label}</h2>
            <p style='margin:0; font-size:18px;'>Estimated Impact in Dhaka</p>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)

        # Guidance text based on intensity
        if "Red" in color or "Orange" in color:
            st.warning("⚠️ **Action:** Stay away from glass windows. Take cover if shaking starts.")
        else:
            st.success("✅ **Status:** Safe. Minor or no shaking expected.")
            
    except Exception as e:
        st.warning(f"System Offline: {e}")
      
