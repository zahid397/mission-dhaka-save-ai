import streamlit as st
import google.generativeai as genai
from PIL import Image

def crack_check():
    st.header("🧱 Building Crack Detector (AI)")
    st.info("Upload an image of a crack to analyze risk.")

    img_file = st.file_uploader("Upload Crack Image", type=["jpg", "png", "jpeg"])

    # API Key Handling
    API_KEY = st.secrets.get("GEMINI_API_KEY", None)
    
    if not API_KEY:
        st.warning("⚠️ API Key not found! Running in DEMO MODE.")
        USE_REAL_AI = False
    else:
        USE_REAL_AI = True

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", width=300)

        if st.button("🔍 Analyze Risk"):
            if USE_REAL_AI:
                try:
                    with st.spinner("🤖 AI is analyzing structural integrity..."):
                        genai.configure(api_key=API_KEY)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        prompt = """
                        Act as a Structural Engineer. Analyze this crack image.
                        Output format:
                        1. **Type:** (e.g., Hairline, Structural)
                        2. **Severity:** (1-10)
                        3. **Risk:** (Low/High)
                        4. **Action:** What to do?
                        """
                        response = model.generate_content([prompt, image])
                        st.success("Analysis Complete!")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                # Demo Mode
                st.success("Analysis Complete (Demo)")
                st.markdown("""
                ### 📋 Expert Report (Demo)
                - **Severity:** ⚠️ 7/10  
                - **Risk:** **High**
                - **Action:** Consult an engineer immediately.
                """)
              
