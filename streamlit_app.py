import streamlit as st
import time

# --- 1. CONFIG & ARTISTIC STYLES ---
st.set_page_config(page_title="The Project Kitchen", page_icon="🍳", layout="wide")

st.markdown("""
    <style>
    /* Main Kitchen Background */
    .stApp {
        background-color: #FFF8E7; /* Creamy parchment color */
        background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
    }
    
    /* Hand-drawn Font Styles */
    h1, h2, h3, .hand-drawn {
        color: #5D4037;
        font-family: 'Brush Script MT', cursive;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* THE SIMMERING POT */
    .pot-container {
        position: relative;
        width: 250px;
        height: 220px;
        margin: auto;
        background: #BCAAA4; /* Pot Color */
        border-radius: 10px 10px 40px 40px;
        border-bottom: 8px solid #8D6E63;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    .pot-rim {
        height: 20px;
        background: #A1887F;
        border-radius: 10px 10px 0 0;
    }
    .pot-liquid {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 60%; /* Adjust for fullness */
        background: linear-gradient(to top, #FFAB91, #FFCCBC);
        animation: simmer 3s infinite alternate ease-in-out;
    }
    .timer-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 48px;
        font-weight: bold;
        color: #3E2723;
        z-index: 10;
        font-family: 'Courier New', monospace;
    }
    @keyframes simmer {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-5px); }
    }
    
    /* THE RECIPE BOOK */
    .recipe-book {
        background-color: #fff;
        width: 90%;
        margin: 20px auto;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        border-radius: 5px;
        display: flex;
        border: 1px solid #d0d0d0;
    }
    .book-page {
        flex: 1;
        padding: 30px;
        border-right: 1px solid #eee;
        background-image: linear-gradient(to right, rgba(0,0,0,0.05) 1px, transparent 1px);
        background-size: 20px 100%; /* Lined paper effect */
    }
    .page-content {
        font-family: 'Garamond', serif;
        font-size: 1.1em;
    }
    
    /* Custom Button Style */
    .stButton>button {
        border-radius: 20px;
        font-family: 'Brush Script MT', cursive;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE INITIALIZATION ---
if 'hours_data' not in st.session_state:
    st.session_state.hours_data = {
        "Research": 0.0, "Briefings": 0.0, "Action Plan": 0.0,
        "Creation": 0.0, "Report": 0.0
    }
recipe_goals = {"Research": 480, "Briefings": 24, "Action Plan": 168, "Creation": 3600, "Report": 600}
stage_list = list(recipe_goals.keys())

if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'active_stage' not in st.session_state: st.session_state.active_stage = "Research"
if 'book_page_idx' not in st.session_state: st.session_state.book_page_idx = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. SIDEBAR: PANTRY & MOOD ---
with st.sidebar:
    st.header("🖼️ The Pantry")
    c_mood = st.select_slider("Cathy's Apron", options=["😊", "😐", "😫"], key="c_v")
    h_mood = st.select_slider("Helen's Apron", options=["😊", "😐", "😫"], key="h_v")
    st.divider()
    st.subheader("🛒 Shopping List")
    st.checkbox("Buy coffee beans")
    st.checkbox("Organize bookmarks")

# --- 4. THE STOVETOP (Artistic Pot Timer) ---
st.markdown("<h1 style='text-align: center;'>👩‍🍳 The Project Kitchen</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; font-style: italic;'>Where great ideas simmer slowly.</p>", unsafe_allow_html=True)

col_pot, col_controls = st.columns([3, 2])

with col_controls:
    st.subheader("🔥 Stovetop Controls")
    st.write("Select ingredients to cook:")
    current_choice = st.selectbox("Select Burner:", stage_list, disabled=st.session_state.is_running, label_visibility="collapsed")
    st.session_state.active_stage = current_choice
    
    st.write(f"**Cooking: {st.session_state.active_stage}**")
    
    b1, b2 = st.columns(2)
    with b1:
        if not st.session_state.is_running:
            if st.button("▶️ Ignite Burner", use_container_width=True):
                st.session_state.start_time = time.time()
                st.session_state.is_running = True
                st.rerun()
        else:
            if st.button("🛑 Turn Off Heat", use_container_width=True):
                elapsed_hrs = (time.time() - st.session_state.start_time) / 3600
                st.session_state.hours_data[st.session_state.active_stage] += elapsed_hrs
                st.session_state.is_running = False
                st.rerun()

with col_pot:
    # Calculate time
    display_seconds = 0
    if st.session_state.is_running:
        display_seconds = time.time() - st.session_state.start_time
    
    h, rem = divmod(display_seconds, 3600)
    m, s = divmod(rem, 60)
    timer_str = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
    
    # The HTML Pot with animated liquid
    st.markdown(f"""
        <div class="pot-container">
            <div class="pot-rim"></div>
            <div class="pot-liquid"></div>
            <div class="timer-text">{timer_str}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. THE INTERACTIVE RECIPE BOOK ---
st.divider()
st.subheader("📖 The Master Recipe Book")

# Navigation for the book
nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
with nav_col1:
    if st.button("⬅️ Prev Page"):
        st.session_state.book_page_idx = max(0, st.session_state.book_page_idx - 1)
with nav_col3:
    if st.button("Next Page ➡️"):
        st.session_state.book_page_idx = min(len(stage_list) - 1, st.session_state.book_page_idx + 1)

# Get current page data
curr_stage_name = stage_list[st.session_state.book_page_idx]
curr_goal = recipe_goals[curr_stage_name]
curr_done = st.session_state.hours_data[curr_stage_name]
progress_fraction = min(curr_done / curr_goal, 1.0)

# Display the "Open Book"
st.markdown(f"""
<div class="recipe-book">
    <div class="book-page">
        <h2 class="hand-drawn">Chapter {st.session_state.book_page_idx + 1}: {curr_stage_name}</h2>
        <div class="page-content">
            <p><strong>Ingredients Needed:</strong> {curr_goal} hours of focused effort.</p>
            <p><strong>Instructions:</strong> Combine readings, notes, and creative thought. Simmer gently over low heat until the mixture thickens into clarity.</p>
            <hr>
            <h3 class="hand-drawn">Chef's Notes:</h3>
            <ul>
                <li>Don't rush the process.</li>
                <li>Taste-test (review) often.</li>
            </ul>
        </div>
    </div>
    <div class="book-page" style="border-right: none; background-color: #f9f5f0;">
        <h2 class="hand-drawn">Current Progress</h2>
        <div style="text-align: center; padding: 20px;">
            <h1 style="font-size: 3em;">{curr_done:.1f} <span style="font-size: 0.5em;">hrs</span></h1>
            <p>prepared out of <strong>{curr_goal} hrs</strong></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Use Streamlit's native progress bar outside the HTML block for functionality
st.progress(progress_fraction)


# --- 6. KITCHEN CHAT (Bubbles) ---
st.divider()
st.subheader("💬 Kitchen Pings")
# ... (Chat code from previous version remains here for communication) ...
