import streamlit as st
import pandas as pd
import requests
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import prompts  # This imports the logic from prompts.py

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Travel Planner", layout="wide")

MAPS_API_KEY = "AIzaSyAUPMPaYezCOvMleHPa--u8tRUJ2rn-Bmc"

# Initialize Vertex AI (Cloud Native)
# This uses your Cloud Shell credentials automatically
PROJECT_ID = "travelplanner-480211"
LOCATION = "us-central1"

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception as e:
    # If running locally without gcloud auth, this might fail, but we catch it.
    print(f"Vertex AI Init warning: {e}")

st.markdown("""
    <style>
    html { font-size: 19px; }
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    
    /* Button Styling */
    div.stButton > button {
        background-color: #262730; 
        color: #aa71d9;
        border: 2px solid #9D4EDD; 
        border-radius: 10px; 
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #9D4EDD; 
        color: white; 
        box-shadow: 0 0 20px #9D4EDD;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. BACKEND FUNCTIONS (The "Real" Distributed System) ---

def get_real_maps_data(city, api_key):
    """
    Connects to Google Maps API.
    Returns:
    1. List of place names (for AI Context)
    2. DataFrame (for UI Map) with Friend's Purple Color
    """
    if not api_key or "YOUR_" in api_key:
        return [], pd.DataFrame()

    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"top tourist attractions in {city}", "key": api_key}
    
    try:
        response = requests.get(endpoint, params=params)
        print(response.text)
        data = response.json()
        
        poi_names = []
        map_data = []
        
        if data.get("status") == "OK":
            for place in data["results"][:7]: # Top 7 results
                name = place.get("name")
                rating = place.get("rating", "N/A")
                lat = place["geometry"]["location"]["lat"]
                lng = place["geometry"]["location"]["lng"]
                
                # For AI
                poi_names.append(f"{name} (Rating: {rating})")
                
                # For Map (Preserving Friend's Purple Color Logic)
                map_data.append({
                    "name": name,
                    "lat": lat,
                    "lon": lng,
                    "color": [157, 78, 221, 200] # Purple format [R,G,B,A]
                })
                
        return poi_names, pd.DataFrame(map_data)

    except Exception as e:
        st.error(f"Maps API Error: {e}")
        return [], pd.DataFrame()

def generate_ai_itinerary(prompt_text):
    """Calls Gemini Pro via Vertex AI"""
    # Using Flash model for speed/cost efficiency in the project
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_text)
    return response.text

# --- 4. UI HEADER ---
st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>✈ AI-Powered Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA; margin-bottom: 30px;'>Cloud Computing & Distributed Systems Project</p>", unsafe_allow_html=True)

# --- 5. INPUTS (Friend's Layout) ---
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1: destination = st.text_input("📍 Destination", "Istanbul")
    with col2: duration = st.slider("📅 Days", 1, 7, 3)
    with col3: budget = st.selectbox("💰 Budget", ["Budget-Friendly", "Moderate", "Luxury"])
    with col4: 
        st.write("") # Spacer
        st.write("")
        submit_btn = st.button("✨ Generate Itinerary", use_container_width=True)

interests = st.multiselect(
    "❤ Interests", 
    ["History", "Food", "Nature", "Art", "Shopping", "Adventure"],
    default=["History", "Food"]
)

# --- 6. MAIN EXECUTION ---
if submit_btn:
    
    # 1. Validation
    if "YOUR_" in MAPS_API_KEY:
        st.error("⚠️ PLEASE UPDATE THE API KEY IN LINE 13 OF APP.PY")
        st.stop()

    with st.status(f"🚀 Flying to {destination}...", expanded=True) as status:
        
        # 2. Context Phase (Maps API)
        st.write("📡 Scanning Google Maps Platform...")
        poi_list, df_places = get_real_maps_data(destination, MAPS_API_KEY)
        
        if poi_list:
            st.write(f"✅ Found {len(poi_list)} verified locations.")
        else:
            st.warning("⚠️ Could not verify locations. AI will use internal knowledge.")

        # 3. Prompt Phase (Using Friend's prompts.py)
        st.write("🧠 Contextualizing User Constraints...")
        full_prompt = prompts.create_travel_prompt(
            destination=destination,
            duration=duration,
            budget=budget,
            interests=interests,
            poi_list=poi_list
        )
        
        # 4. Generation Phase (Vertex AI)
        st.write("🤖 Gemini Pro is designing your plan...")
        try:
            itinerary = generate_ai_itinerary(full_prompt)
            status.update(label="Itinerary Ready!", state="complete", expanded=False)
            
            # --- UI OUTPUT ---
            st.success(f"✅ Trip to {destination} Generated!")

            map_col, details_col = st.columns([2, 1])
            
            with map_col:
                if not df_places.empty:
                    # Using Friend's color column logic
                    st.map(df_places, color="color", zoom=12)
            
            with details_col:
                st.subheader("📍 Verified Spots")
                if not df_places.empty:
                    for index, row in df_places.iterrows():
                         with st.container(border=True):
                            st.write(f"**{row['name']}**")

            st.markdown("---")
            st.header("🗓️ Your Daily Plan")
            st.markdown(itinerary)
            
        except Exception as e:
            st.error(f"AI Generation Error: {e}")
            st.info("Tip: Ensure 'Vertex AI API' is enabled in Google Cloud Console.")