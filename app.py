import streamlit as st
import pandas as pd
import time
import prompts

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Travel Planner", layout="wide")

# --- CSS HACKS (For Title & Button Styling) ---
st.markdown("""
    <style>
    /* making the font bigger */
    html {
        font-size: 19px; /* 
    }

    /* 1. Adjust the top padding to make the title higher */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    /* 2. Style the "Generate Itinerary" Button */
    div.stButton > button {
        background-color: #262730; /* Dark background */
        color: #aa71d9;            /* Purple Text */
        border: 2px solid #9D4EDD; /* Purple Border */
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    /* Hover Effect: Glow! */
    div.stButton > button:hover {
        background-color: #9D4EDD; /* Turn background purple */
        color: white;              /* Turn text white */
        box-shadow: 0 0 20px #9D4EDD; /* The GLOW effect */
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER SECTION ---
# using HTML to center text and control size
st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>✈ AI-Powered Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA; margin-bottom: 30px;'>Cloud Computing & Distributed Systems Project</p>", unsafe_allow_html=True)
# --- TEMPORARY DEBUGGING TOOL ---
if st.button("🐞 Debug: Show Me The Prompt"):
    # 1. Fake the data (simulate what the map would find)
    fake_pois = ["Galata Tower", "Spice Bazaar", "Hagia Sophia"]
    
    # 2. Call your function
    # Note: We use 'prompts.create_travel_prompt' to access the file you made
    test_prompt = prompts.create_travel_prompt(
        destination="Istanbul",
        duration=3,
        budget="Moderate",
        interests=["History", "Food"],
        poi_list=fake_pois
    )
    
    # 3. Display it raw so you can check for typos/formatting
    st.text_area("Generated Prompt", test_prompt, height=300)
    
    # 4. The "Manual" Test
    st.info("👉 Copy the text above and paste it into ChatGPT or Gemini etc. to see if it produces a good itinerary.")

# --- 3. INPUTS (Top Bar) ---
with st.container():
    # Split into 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        destination = st.text_input("📍 Destination", "Istanbul")
    
    with col2:
        duration = st.slider("📅 Days", 1, 7, 3)
        
    with col3:
        budget = st.selectbox("💰 Budget", ["Budget-Friendly", "Moderate", "Luxury"])
        
    with col4:
        st.write("") # Spacer
        st.write("") 
        submit_btn = st.button("✨ Generate Itinerary", use_container_width=True)

    interests = st.multiselect(
        "❤ Interests", 
        ["History", "Food", "Nature", "Art", "Shopping", "Adventure"],
        default=["History", "Food"]
    )

# --- 4. MOCK DATA  ---
def get_mock_data(city):
    """
    Returns data with a 'color' column for the map.
    Streamlit map wants colors in [R, G, B, A] format (0-255).
    Purple (#9D4EDD) is approximately [157, 78, 221].
    """
    data = {
        'name': [
            f"Top Attraction in {city}", f"Famous Museum of {city}",
            f"Local Park in {city}", f"Historic Bridge", f"Best Restaurant"
        ],
        'lat': [41.0082, 41.0122, 41.0422, 41.0250, 41.0360],
        'lon': [28.9784, 28.9760, 29.0060, 28.9740, 28.9850],
        # THIS IS THE MAGIC LINE FOR COLOR:
        'color': [[157, 78, 221, 200] for _ in range(5)] # Purple with some transparency
    }
    return pd.DataFrame(data)

# --- 5. MAIN OUTPUT ---
if submit_btn:
    with st.spinner(f"Flying to {destination}..."):
        time.sleep(1) 
        df_places = get_mock_data(destination)
        
        st.success(f"✅ Found top places in {destination}!")
        
        map_col, details_col = st.columns([2, 1])
        
        with map_col:
            # We tell st.map to look at the 'color' column we created
            st.map(df_places, color="color", zoom=12)

        with details_col:
            st.subheader("📍 Top Spots")
            for index, row in df_places.iterrows():
                with st.container(border=True):
                    st.write(f"**{row['name']}**")
                    st.caption("Rating: ⭐ 4.8")

        st.markdown("---")
        st.header("🗓️ Your Daily Plan")
        with st.expander("Day 1: Arrival & Exploration", expanded=True):
            st.write("Morning: Breakfast at...")