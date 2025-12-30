import streamlit as st
import time
from datetime import datetime

# --- 1. THEME & COOKBOOK STYLING ---
st.set_page_config(page_title="The Project Kitchen", page_icon="👩‍🍳", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #FFFDF5;
    }
    
    /* Headers & Fonts */
    h1, h2, h3 {
        color: #5D4037;
        font-family: 'Georgia', serif;
    }

    /* Instagram-style Bubble Chat */
    .chat-bubble {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 8px;
        display: inline-block;
        max-width: 85%;
        border: 1px solid #E0E0E0;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05);
        font-family: 'Helvetica Neue', sans-serif;
        color: #333;
    }
    .user-label {
        font-weight: bold;
        font-size: 0.85em;
        margin-bottom: 2px;
        color: #8D6E63;
        margin-left: 10px;
    }

    /* Custom Button Style */
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE INITIALIZATION ---
if 'total_seconds' not in st.session_state: st.session_state.total_seconds = 0
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"user": "System", "text": "Welcome to the Kitchen! Start cooking to track progress."}
    ]

# --- 3. SIDEBAR: CHEF STATUS (Mood Indicator) ---
with st.sidebar:
    st.header("🖼️ The Fridge")
    st.write("Post your current academic workload:")
    
    c_mood = st.select_slider("Cathy's Vibe", options=["😊", "😐", "😫"], key="c_vibe")
    h_mood = st.select_slider("Helen's Vibe", options=["😊", "😐", "😫"], key="h_vibe")
    
    st.divider()
    st.markdown("### 🏷️ Status Meanings")
    st.caption("😊 Chill: Send me tasks!")
    st.caption("😐 Simmering: Uni is busy.")
    st.caption("😫 Boiling: Do not disturb!")

# --- 4. TOP SECTION: STOVETOP (The Timer) ---
st.title("🍳 The Project Kitchen")
st.write("*Collaborative research at a low, steady heat.*")

col_timer, col_actions = st.columns([2, 1])

# Timer Logic
if st.session_state.is_running:
    current_elapsed = time.time() - st.session_state.start_time
    display_time = st.session_state.total_seconds + current_elapsed
else:
    display_time = st.session_state.total_seconds

# Format to HH:MM:SS
h, rem = divmod(display_time, 3600)
m, s = divmod(rem, 60)
time_str = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

with col_timer:
    st.markdown(f"<h1 style='font-size: 70px; margin-top: 0;'>⏱️ {time_str}</h1>", unsafe_allow_html=True)

with col_actions:
    if not st.session_state.is_running:
        if st.button("▶️ Start Cooking", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("🛑 Stop & Save", use_container_width=True):
            st.session_state.total_seconds += (time.time() - st.session_state.start_time)
            st.session_state.is_running = False
            st.rerun()
    
    if st.button("🧹 Reset Pot", use_container_width=True):
        st.session_state.total_seconds = 0
        st.session_state.is_running = False
        st.rerun()

# --- 5. MIDDLE SECTION: PROGRESS & BUBBLES ---
st.divider()
left_kitchen, right_kitchen = st.columns([1, 1])

with left_kitchen:
    st.subheader("📖 The Recipe (Stages)")
    # Goals in hours based on your screenshot
    recipe_book = {
        "Research": 480,
        "Action Plan": 168,
        "Creation": 3600,
        "Report": 600
    }
    
    curr_hrs = st.session_state.total_seconds / 3600
    for stage, goal in recipe_book.items():
        prog = min(curr_hrs / goal, 1.0)
        st.write(f"**{stage}**")
        st.progress(prog)
        st.caption(f"{curr_hrs:.1f} / {goal} hours simmered")

with right_kitchen:
    st.subheader("💬 Kitchen Pings")
    
    # Display Chat Bubbles
    chat_container = st.container(height=300)
    with chat_container:
        for msg in st.session_state.messages:
            st.markdown(f'<div class="user-label">{msg["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble">{msg["text"]}</div>', unsafe_allow_html=True)

    # Note Input
    chat_col1, chat_col2 = st.columns([3, 1])
    with chat_col1:
        user_choice = st.selectbox("Who's talking?", ["Cathy", "Helen"], label_visibility="collapsed")
        new_note = st.text_input("Leave a bubble note...", label_visibility="collapsed")
    with chat_col2:
        if st.button("Send ✨"):
            if new_note:
                st.session_state.messages.append({"user": user_choice, "text": new_note})
                st.rerun()

# --- 6. BOTTOM SECTION: THE DAILY SPECIAL (Summarizer) ---
st.divider()
st.subheader("📝 The Daily Special (Proposal Summary)")
if st.button("✨ Generate Summary for Research Report"):
    total_h = st.session_state.total_seconds / 3600
    last_note = st.session_state.messages[-1]['text'] if st.session_state.messages else "No recent notes."
    
    summary = f"""
    **Project Progress Update:**
    - **Total Cumulative Effort:** {total_h:.2f} hours recorded.
    - **Current Kitchen Heat:** Cathy is {c_mood}, Helen is {h_mood}.
    - **Latest Collaboration Note:** "{last_note}"
    - **Methodology Note:** The team is utilizing a non-linear, cumulative work-tracking system to balance high-workload academic requirements with project development phases.
    """
    st.info(summary)
    st.caption("Copy and paste this into your Research Proposal or documentation!")
