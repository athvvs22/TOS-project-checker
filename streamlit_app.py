import streamlit as st
import time
import json
import os
from datetime import datetime

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Project Kitchen", page_icon="🥘", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #fdfcfb 0%, #e2d1c3 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Glassmorphism Panels */
    .glass-panel {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
    }
    
    /* Glowing Pot Timer */
    .timer-circle {
        width: 160px; height: 160px;
        background: white;
        border-radius: 50%;
        margin: 20px auto;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 10px 40px rgba(141, 110, 99, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.8);
    }
    .pulse { animation: pulse-ring 2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite; }
    @keyframes pulse-ring { 0% { transform: scale(.95); box-shadow: 0 0 0 0 rgba(255, 126, 95, 0.4); } 70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(255, 126, 95, 0); } 100% { transform: scale(.95); } }

    /* Chat Bubbles */
    .bubble {
        background: rgba(255, 255, 255, 0.8);
        padding: 10px 15px; border-radius: 18px 18px 18px 4px;
        margin-bottom: 8px; border: 1px solid #eee; font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA STORAGE ENGINE ---
DB_FILE = "kitchen_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "hours": {"Research": 0.0, "Briefings": 0.0, "Action Plan": 0.0, "Creation": 0.0, "Report": 0.0},
        "chats": [],
        "workloads": {"Cathy": "😊", "Helen": "😊"}
    }

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Initialize Session State
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'is_running' not in st.session_state: st.session_state.is_running = False

# --- 3. THE INTERFACE ---
st.title("🥘 The Project Kitchen")

col_left, col_mid, col_right = st.columns([1, 1.2, 1])

# LEFT: ACADEMIC WORKLOAD & TASKS
with col_left:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("👨‍🍳 Chef Status")
    c_w = st.select_slider("Cathy's Workload", options=["😫", "😐", "😊"], value=st.session_state.data['workloads']['Cathy'])
    h_w = st.select_slider("Helen's Workload", options=["😫", "😐", "😊"], value=st.session_state.data['workloads']['Helen'])
    
    if (c_w != st.session_state.data['workloads']['Cathy']) or (h_w != st.session_state.data['workloads']['Helen']):
        st.session_state.data['workloads'] = {"Cathy": c_w, "Helen": h_w}
        save_data(st.session_state.data)
    st.markdown('</div>', unsafe_allow_html=True)

# MID: POT STOPWATCH (TASK ACCUMULATION)
with col_mid:
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    target_stage = st.selectbox("Current Burner:", list(st.session_state.data['hours'].keys()))
    
    # Timer Display
    display_sec = 0
    if st.session_state.is_running:
        display_sec = time.time() - st.session_state.start_time
    
    h_disp, rem = divmod(display_sec, 3600)
    m_disp, s_disp = divmod(rem, 60)
    
    pulse_class = "pulse" if st.session_state.is_running else ""
    st.markdown(f"""
        <div class="timer-circle {pulse_class}">
            <h1 style="color:#5D4037; margin:0;">{int(h_disp):02d}:{int(m_disp):02d}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"Active Ingredient: **{target_stage}**")

    if not st.session_state.is_running:
        if st.button("▶ Start Cooking", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏹ Save to Recipe", use_container_width=True):
            elapsed_hrs = (time.time() - st.session_state.start_time) / 3600
            st.session_state.data['hours'][target_stage] += elapsed_hrs
            st.session_state.is_running = False
            save_data(st.session_state.data)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT: CHAT BUBBLES & PROGRESS
with col_right:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("💬 Kitchen Pings")
    chat_box = st.container(height=180)
    with chat_box:
        for m in st.session_state.data['chats']:
            st.markdown(f'<div class="bubble"><b>{m["user"]}:</b> {m["text"]}</div>', unsafe_allow_html=True)
    
    chat_user = st.selectbox("I am...", ["Cathy", "Helen"])
    chat_text = st.text_input("Send a note...")
    if st.button("Ping! ✨"):
        if chat_text:
            st.session_state.data['chats'].append({"user": chat_user, "text": chat_text})
            save_data(st.session_state.data)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("📖 Recipe Progress")
    # Goal mapping from your screenshot
    goals = {"Research": 480, "Briefings": 24, "Action Plan": 168, "Creation": 3600, "Report": 600}
    for s, h in st.session_state.data['hours'].items():
        st.caption(f"{s}: {h:.1f}h / {goals[s]}h")
        st.progress(min(h/goals[s], 1.0))
    st.markdown('</div>', unsafe_allow_html=True)
