import streamlit as st
import time
from datetime import datetime

# --- 1. SETTINGS & CUTE THEME (Quibble/Dreamy Aesthetic) ---
st.set_page_config(page_title="Magical Project Kitchen", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;500&family=Indie+Flower&display=swap');

    /* Background: Soft, warm kitchen glow */
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)),
                    url("https://www.transparenttextures.com/patterns/cream-paper.png"),
                    #F9F5F0;
        font-family: 'Fredoka', sans-serif;
    }

    /* Instagram-Style Note Bubbles */
    .insta-note {
        background: white;
        border-radius: 25px;
        padding: 10px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        width: fit-content;
        border: 1px solid #F0EAD6;
    }
    .profile-pic {
        width: 40px; height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        background: #E2D1C3;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: bold; color: white;
    }

    /* The Magical Pot Container */
    .pot-container {
        background: #D7CCC8;
        border-radius: 40% 40% 50% 50%;
        width: 220px; height: 180px;
        margin: 20px auto;
        position: relative;
        border-bottom: 8px solid #8D6E63;
        display: flex; align-items: center; justify-content: center;
    }
    .bubbling {
        position: absolute; top: 10%; width: 80%; height: 20%;
        background: rgba(255,255,255,0.3); border-radius: 50%;
        animation: steam 2s infinite;
    }
    @keyframes steam { 0% {transform: translateY(0); opacity:0;} 50% {opacity:0.5;} 100% {transform: translateY(-40px); opacity:0;} }

    /* The Flippable Scroll/Book */
    .recipe-scroll {
        background: #FFF9E1;
        border: 2px solid #D7CCC8;
        border-radius: 10px;
        padding: 20px;
        margin-top: -20px;
        box-shadow: 5px 5px 0px #E2D1C3;
        font-family: 'Indie Flower', cursive;
    }

    /* Custom Slider Styles (Good on Left, Bad on Right) */
    .stSlider [data-baseweb="slider"] {
        background: linear-gradient(to right, #A5D6A7, #EF9A9A);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (Data Persistence) ---
if 'hours' not in st.session_state:
    st.session_state.hours = {"Research": 0.0, "Briefings": 0.0, "Action Plan": 0.0, "Creation": 0.0, "Report": 0.0}
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'book_page' not in st.session_state: st.session_state.book_page = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. THE INTERFACE ---
st.write("<h1 style='text-align: center; color: #8D6E63;'>✨ Magical Project Kitchen ✨</h1>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([1, 1.5, 1])

# LEFT SIDE: CHEF MOODS (Academic Workload)
with col_left:
    st.write("### 👩‍🍳 Chef Moods")
    st.caption("Good (Left) ↔️ Stressed (Right)")
    cathy_vibe = st.select_slider("Cathy", options=["✨", "😊", "😐", "😫", "🔥"])
    helen_vibe = st.select_slider("Helen", options=["✨", "😊", "😐", "😫", "🔥"])
    
    st.divider()
    st.write("### 🛒 Pantry Tasks")
    st.checkbox("Read 3 papers", value=True)
    st.checkbox("Draft pseudocode")
    st.checkbox("Update report")

# MIDDLE: THE POT & SCROLL
with col_mid:
    # 1. The Active Pot
    target_stage = st.selectbox("Which ingredient are we cooking?", list(st.session_state.hours.keys()))
    
    # Live Timer Logic
    elapsed_display = 0
    if st.session_state.is_running:
        elapsed_display = time.time() - st.session_state.start_time
    
    m, s = divmod(int(elapsed_display), 60)
    h_disp, m = divmod(m, 60)
    timer_str = f"{h_disp:02d}:{m:02d}:{s:02d}"

    st.markdown(f"""
        <div class="pot-container">
            <div class="bubbling"></div>
            <h1 style="color: white; font-family: monospace; z-index: 10;">{timer_str}</h1>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if not st.session_state.is_running:
            if st.button("▶ Start Cooking", use_container_width=True):
                st.session_state.start_time = time.time()
                st.session_state.is_running = True
                st.rerun()
        else:
            if st.button("⏹ Save Progress", use_container_width=True):
                st.session_state.hours[target_stage] += (time.time() - st.session_state.start_time) / 3600
                st.session_state.is_running = False
                st.rerun()
    with c2:
        if st.button("🗑 Reset Pot", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

    # 2. The Flippable Recipe Scroll (Directly under Pot)
    st.write("### 📖 The Master Recipe")
    pages = list(st.session_state.hours.keys())
    curr_p = pages[st.session_state.book_page]
    
    st.markdown(f"""
        <div class="recipe-scroll">
            <h2 style="margin:0;">Page {st.session_state.book_page + 1}: {curr_p}</h2>
            <hr style="border: 0.5px dashed #D7CCC8;">
            <p style="font-size: 1.5rem;">Total Cooked: <b>{st.session_state.hours[curr_p]:.2f} hours</b></p>
            <p><i>Keep simmering until this reaches perfection.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    pc1, pc2 = st.columns(2)
    with pc1:
        if st.button("⬅️ Flip Back"):
            st.session_state.book_page = (st.session_state.book_page - 1) % len(pages)
            st.rerun()
    with pc2:
        if st.button("Flip Forward ➡️"):
            st.session_state.book_page = (st.session_state.book_page + 1) % len(pages)
            st.rerun()

# RIGHT SIDE: INSTAGRAM NOTES (Kitchen Pings)
with col_right:
    st.write("### 💭 Kitchen Pings")
    
    # Note Display
    for msg in st.session_state.messages[-3:]: # Show last 3
        color = "#FFD1DC" if msg['user'] == "Cathy" else "#B2EBF2"
        st.markdown(f"""
            <div class="insta-note">
                <div class="profile-pic" style="background:{color};">{msg['user'][0]}</div>
                <div>{msg['text']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Note Input
    st.divider()
    sender = st.radio("I am...", ["Cathy", "Helen"], horizontal=True)
    new_msg = st.text_input("Leave a note...", placeholder="Thinking about pseudocode...")
    if st.button("Post Note ✨"):
        if new_msg:
            st.session_state.messages.append({"user": sender, "text": new_msg})
            st.rerun()
