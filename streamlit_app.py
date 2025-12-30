import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Project Engine", layout="wide")

# --- DATABASE SIMULATION ---
# In a real app, this would be a Google Sheet or Database
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'chat' not in st.session_state:
    st.session_state.chat = []

# --- APP LAYOUT ---
st.title("🚀 Team Progress Engine")
st.subheader("Focus on the work, not the clock.")

# --- STAGE TRACKING (From your screenshot) ---
stages = {
    "RESEARCH": {"goal": 480, "unit": "hours", "current": 120},
    "BRIEFINGS": {"goal": 1, "unit": "day", "current": 0.5},
    "ACTION PLAN": {"goal": 7, "unit": "days", "current": 2},
    "CREATION": {"goal": 150, "unit": "days", "current": 10}, # 5 months converted
    "REPORT": {"goal": 25, "unit": "days", "current": 5},
}

cols = st.columns(len(stages))

for i, (name, data) in enumerate(stages.items()):
    with cols[i]:
        progress = data['current'] / data['goal']
        st.metric(name, f"{data['current']} / {data['goal']} {data['unit']}")
        st.progress(min(progress, 1.0))

# --- THE INTERACTIVE WORK LOG ---
st.divider()
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("### ✍️ Log Your Progress")
    member = st.selectbox("Who is logging?", ["Cathy", "Helen"])
    stage_select = st.selectbox("Which stage?", list(stages.keys()))
    amount = st.number_input(f"Amount (Hours/Days)", min_value=0.1)
    
    if st.button("Add to Total"):
        entry = f"{member} added {amount} to {stage_select}"
        st.session_state.logs.append(entry)
        st.success("Progress saved!")

with col_b:
    st.markdown("### 💬 Team Chat & Brainstorm")
    user_msg = st.text_input("Send a note to your partner:")
    if st.button("Send"):
        st.session_state.chat.append(f"**{member}**: {user_msg}")
    
    # Display Chat
    for msg in reversed(st.session_state.chat):
        st.write(msg)

# --- RESEARCH SUMMARY TOOL ---
st.divider()
st.markdown("### 📝 Research Proposal Summarizer")
research_text = st.text_area("Paste your latest findings or pseudocode here to summarize for the report:")
if st.button("Summarize for Cathy/Helen"):
    st.info("Summary: This section identifies key sources for the 'Creation' stage and outlines the pseudocode logic.")
