import streamlit as st

# 1. Page Config (Must be the first line)
st.set_page_config(
    page_title="Mission Dhaka Save",
    page_icon="🇧🇩",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS (Styling)
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #FF4B4B; text-align: center; font-weight: bold;}
    .sub-text {text-align: center; color: #555; margin-bottom: 20px;}
    .stButton>button {width: 100%; border-radius: 5px;}
    .footer {position: fixed; bottom: 0; width: 100%; text-align: center; color: #888; font-size: 12px; background-color: white; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

# 3. Import Modules (With Error Handling)
try:
    from modules.crack_detector import crack_check
    from modules.earthquake_monitor import quake_monitor
    from modules.alert_system import japan_style_alert
    from modules.safe_zone import safe_zone_finder
    from modules.risk_predictor import fault_line_risk
except ImportError as e:
    st.error(f"❌ Module Missing: {e}. Please check the 'modules' folder.")

# 4. Sidebar Navigation
with st.sidebar:
    st.markdown("## 🛡️ Mission Dhaka Save")
    st.markdown("---")
    
    menu = st.radio(
        "Select Feature:",
        [
            "🏠 Home Dashboard",
            "⏱ Early Alert System",   
            "🏚 Building Crack Check", 
            "🌐 Live Global Monitor",
            "⚠️ Fault Line Risk",      
            "🧭 Safe Zone Map"
        ]
    )
    
    st.markdown("---")
    st.info("🚑 Emergency: 999")
    st.caption("Developed by Team Mission Dhaka Save")

# 5. Main Page Logic
if menu == "🏠 Home Dashboard":
    st.markdown('<p class="main-header">🌍 Mission Dhaka Save</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">AI-Powered Earthquake Safety & Awareness System</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🚨 **Status:** Monitoring Active")
    with col2:
        st.success("✅ **System:** Online")

    st.image("https://source.unsplash.com/800x400/?rescue,dhaka", caption="Preparedness is our only defense.")
    
    st.write("### 🎯 সিস্টেম ফিচারসমূহ:")
    c1, c2 = st.columns(2)
    c1.markdown("👉 **Early Alert:** S-Wave পৌঁছানোর আগেই সতর্কতা।")
    c1.markdown("👉 **Crack Check:** AI দিয়ে বিল্ডিং সেফটি চেক।")
    c2.markdown("👉 **Risk Predictor:** ফল্ট লাইন রিস্ক অ্যানালিসিস।")
    c2.markdown("👉 **Safe Zone:** ম্যাপে নিরাপদ জায়গা খুঁজুন।")

elif menu == "⏱ Early Alert System":
    japan_style_alert()

elif menu == "🏚 Building Crack Check":
    crack_check()

elif menu == "🌐 Live Global Monitor":
    quake_monitor()

elif menu == "⚠️ Fault Line Risk":
    fault_line_risk()

elif menu == "🧭 Safe Zone Map":
    safe_zone_finder()

# Footer
st.markdown("---")
st.markdown('<p class="footer">© 2025 Mission Dhaka Save | Saving Lives with AI</p>', unsafe_allow_html=True)
