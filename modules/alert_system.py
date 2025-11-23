import streamlit as st
import requests
import math
import pandas as pd
import pydeck as pdk 

# USGS REAL-TIME GLOBAL EARTHQUAKE FEED (Last 1 Hour)
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# 🇧🇩 FULL 64 DISTRICT COORDS (Thanks to Zahid)
districts = {
    "Dhaka": (23.8103, 90.4125), "Gazipur": (23.9999, 90.4203), "Narayanganj": (23.6238, 90.5000),
    "Narsingdi": (23.9185, 90.7181), "Manikganj": (23.8617, 90.0037), "Munshiganj": (23.5422, 90.5350),
    "Faridpur": (23.6070, 89.8420), "Gopalganj": (23.0059, 89.8267), "Madaripur": (23.1641, 90.1890),
    "Rajbari": (23.7573, 89.6447), "Shariatpur": (23.2197, 90.3500),
    "Chattogram": (22.3569, 91.7832), "Cox's Bazar": (21.4272, 92.0058), "Bandarban": (22.1953, 92.2184),
    "Khagrachari": (23.1193, 91.9847), "Rangamati": (22.7324, 92.2985), "Feni": (22.9332, 91.3950),
    "Lakshmipur": (22.9440, 90.8300), "Noakhali": (22.8696, 91.0990), "Brahmanbaria": (23.9570, 91.1110),
    "Cumilla": (23.4682, 91.1789), "Chandpur": (23.2515, 90.8518),
    "Sylhet": (24.8949, 91.8687), "Moulvibazar": (24.4829, 91.7774), "Habiganj": (24.3740, 91.4155), 
    "Sunamganj": (25.0658, 91.3950), "Rajshahi": (24.3636, 88.6241), "Natore": (24.4206, 89.0000), 
    "Pabna": (24.0064, 89.2372), "Sirajganj": (24.4534, 89.7000), "Bogura": (24.8481, 89.3730), 
    "Joypurhat": (25.0968, 89.0227), "Naogaon": (24.7936, 88.9318), "Chapainawabganj": (24.5965, 88.2773),
    "Rangpur": (25.7439, 89.2752), "Nilphamari": (25.9310, 88.8560), "Lalmonirhat": (25.9930, 89.2847),
    "Kurigram": (25.8054, 89.6362), "Gaibandha": (25.3288, 89.5435), "Dinajpur": (25.6217, 88.6354),
    "Thakurgaon": (26.0335, 88.4618), "Panchagarh": (26.3411, 88.5542), "Khulna": (22.8456, 89.5403), 
    "Jessore": (23.1706, 89.2000), "Satkhira": (22.7185, 89.0700), "Jhenaidah": (23.5448, 89.1536), 
    "Narail": (23.1725, 89.5120), "Magura": (23.4873, 89.4196), "Bagerhat": (22.6516, 89.7853), 
    "Kushtia": (23.9013, 89.1205), "Chuadanga": (23.6402, 88.8418), "Meherpur": (23.7622, 88.6319),
    "Barishal": (22.7010, 90.3535), "Patuakhali": (22.3596, 90.3290), "Bhola": (22.6859, 90.6476),
    "Jhalokathi": (22.6326, 90.2000), "Pirojpur": (22.5791, 89.9750), "Barguna": (22.1540, 90.1250),
    "Mymensingh": (24.7471, 90.4203), "Jamalpur": (24.9375, 89.9370), "Netrokona": (24.8835, 90.7270), 
    "Sherpur": (25.0205, 90.0153)
}

# DISTANCE FORMULA (Haversine)
def dist(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# JAPAN SHINDO SCALE ESTIMATOR
def estimate_intensity(mag, d):
    # Simplified Physics: Intensity drops with distance
    score = mag - (d / 100)

    if score >= 5.5: return "Shindo 5+ (Severe)", "#FF0000", "white" # Red
    if score >= 4.5: return "Shindo 4 (Strong)", "#FF8C00", "white" # Orange
    if score >= 3.5: return "Shindo 3 (Moderate)", "#FFD700", "black" # Yellow
    if score >= 2.0: return "Shindo 2 (Weak)", "#32CD32", "white" # Green
    return "Not Felt", "#808080", "white" # Grey

# MAIN FUNCTION
def japan_style_alert():
    st.header("⏱ Nationwide Early Warning System (64 Districts)")
    st.info("Real-time impact analysis for all Bangladesh districts.")

    # 1. Inputs: District Selection & Simulation Toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        my_district = st.selectbox("📍 Select Your Location", sorted(districts.keys()))
    with col2:
        simulation = st.toggle("🛠 Test Mode", False)

    # User Coordinates
    user_lat, user_lon = districts[my_district]

    try:
        # 2. Fetch Data
        if simulation:
            # Scenario: Major Quake at Dauki Fault (Sylhet Border)
            mag = 7.2
            place = "Simulation: Dauki Fault Zone"
            eq_lat, eq_lon = 25.133, 91.87
            event_time = "Just Now"
        else:
            data = requests.get(USGS_URL).json()
            if not data["features"]:
                st.success("✅ No earthquakes detected globally in the last hour.")
                return

            quake = data["features"][0]
            mag = quake["properties"]["mag"]
            place = quake["properties"]["place"]
            eq_lon, eq_lat, _ = quake["geometry"]["coordinates"]
            event_time = "Live Feed"

        # 3. Process Data for ALL 64 Districts
        results = []
        for district_name, (d_lat, d_lon) in districts.items():
            d_dist = dist(d_lat, d_lon, eq_lat, eq_lon)
            d_intensity, _, _ = estimate_intensity(mag, d_dist)
            results.append({
                "District": district_name,
                "Distance (km)": int(d_dist),
                "Estimated Intensity": d_intensity,
                "Arrival Time (sec)": int(d_dist / 4.0) # S-wave speed ~4km/s
            })

        # Create sorted dataframe (Most affected on top)
        df = pd.DataFrame(results)
        df = df.sort_values("Distance (km)")

        # 4. Personal Alert Card (For Selected District)
        # Find user's data in the processed list
        my_data = next(item for item in results if item["District"] == my_district)
        
        d_km = my_data["Distance (km)"]
        s_wave_sec = my_data["Arrival Time (sec)"]
        lbl, bg, txt = estimate_intensity(mag, d_km)

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("📍 Epicenter", place)
        c2.metric("⚛ Magnitude", mag)
        c3.metric(f"📏 Dist. to {my_district}", f"{d_km} km")

        # ALERT CARD
        st.subheader(f"📉 Impact Forecast: {my_district}")
        html_code = f"""
        <div style="background-color:{bg}; color:{txt}; padding:20px; border-radius:10px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin:0;">{lbl}</h2>
            <p style="margin:5px 0 15px 0;">Intensity Forecast</p>
            <hr style="border:1px solid {txt}; opacity:0.3;">
            <p style="margin:10px 0 0 0; font-size:18px;">S-Wave Arrival In:</p>
            <h1 style="margin:0; font-size:45px;">{s_wave_sec} sec</h1>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)

        # 5. Map Visualization (User vs Epicenter)
        map_data = pd.DataFrame([
            {"lat": user_lat, "lon": user_lon, "type": "You", "color": [0, 0, 255, 200], "size": 100},
            {"lat": eq_lat, "lon": eq_lon, "type": "Epicenter", "color": [255, 0, 0, 200], "size": 500}
        ])
        
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(latitude=23.68, longitude=90.35, zoom=6),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer", map_data, get_position="[lon, lat]",
                    get_color="color", get_radius="size * 100", pickable=True
                )
            ]
        ))

        # 6. National Leaderboard (Top 10 Affected Districts)
        st.divider()
        st.subheader("🇧🇩 Most Affected Districts (Top 10)")
        st.dataframe(df.head(10), hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"System Error: {e}")
        
