import streamlit as st
import google.generativeai as genai
import requests
import os

# --- 1. CONFIGURATION ---
# Replace this with the API Key you got earlier
MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("✈ AI-Powered Travel Itinerary Planner")
st.caption("Cloud Computing & Distributed Systems Project")

# --- 2. SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Plan Your Trip")
    destination = st.text_input("Destination City", "Istanbul")
    duration = st.slider("Duration (Days)", 1, 7, 3)
    budget = st.selectbox("Budget Level", ["Budget-Friendly", "Moderate", "Luxury"])
    interests = st.multiselect(
        "Interests", 
        ["History", "Food", "Nature", "Art", "Shopping", "Adventure"],
        default=["History", "Food"]
    )
    submit_btn = st.button("Generate Itinerary")

# --- 3. GOOGLE MAPS FUNCTION ---
def get_places_data(city, api_key):
    """
    Connects to Google Maps Places API to find top attractions.
    Returns a list of place names and their ratings.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"top attractions in {city}"
    params = {
        "query": query,
        "key": api_key,
        "language": "en"
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Check if Google gave a valid response
        if data.get("status") == "OK":
            places = []
            # Get top 5 places
            for result in data["results"][:5]:
                name = result["name"]
                rating = result.get("rating", "N/A")
                places.append(f"{name} (Rating: {rating})")
            return places, data # Return both the list and raw data
        else:
            return [], data
    except Exception as e:
        st.error(f"Error connecting to Maps API: {e}")
        return [], {}

# --- 4. MAIN APPLICATION LOGIC ---
if submit_btn:
    if not MAPS_API_KEY or MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
        st.error("⚠ Please enter your Google Maps API Key in the code!")
    else:
        st.info(f"🔄 Fetching real data for {destination}...")
        
        # Call the Google Maps Function
        poi_list, raw_data = get_places_data(destination, MAPS_API_KEY)
        
        if poi_list:
            st.success(f"✅ Found {len(poi_list)} top places in {destination}!")
            
            # Show the "Context" we will send to the AI
            st.subheader("📍 Context Data (from Google Maps)")
            st.write("We found these places to base the itinerary on:")
            for place in poi_list:
                st.write(f"- {place}")
                
            # Developer View: Show raw JSON (Great for your report!)
            with st.expander("View Raw JSON Response (For Debugging)"):
                st.json(raw_data)
        else:
            st.warning("Could not find places. Check your API Key or City name.")
            st.json(raw_data) # Show error detail