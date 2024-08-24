import streamlit as st
from datetime import datetime
import json 
from helper import *

# Initialize session state for kid's info, score, log, tasks
if 'kid_name' not in st.session_state:
    st.session_state.kid_name = "Cindy"
if 'kid_age' not in st.session_state:
    st.session_state.kid_age = 5
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'log' not in st.session_state:
    st.session_state.log = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}


# Function to add an entry to the log
def add_to_log(action, points):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.log.append({"timestamp": timestamp, "action": action, "points": points})
    # Keep only the last 20 log entries
    st.session_state.log = st.session_state.log[-20:]

# Kid's Information Section
st.title("🌟 Little Star's Scoreboard! 🌟")
st.caption("_Cindy's_ Scoreboard")


top_col1, top_col2 = st.columns(2)
with top_col2:
    left_col, right_col = st.columns([3,1])

with top_col1:
    st.markdown(f"# Total Score: {st.session_state.score}")
    st.markdown(f"### = ${st.session_state.score / 5.0}")
with right_col:
    if st.button("Create a Task"):
        create_task()
with left_col:
    # Score Adjustment
    adjustment = st.number_input("Adjust score:", min_value=-100, max_value=100, value=0)
    if st.button("Apply"):
        st.session_state.score += adjustment
        add_to_log("Score adjusted", adjustment)
        st.rerun()



    

if st.session_state.kid_name == "":
    introduceYou()


# Display and manage existing tasks
if st.session_state.tasks:
    st.subheader("Tasks:")
    for task_name, task_score in st.session_state.tasks.items():
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{task_name} ({task_score})"):
                st.session_state.score += task_score
                add_to_log(f"Completed task '{task_name}'", task_score)
                st.rerun()
        with col2:
            if st.button(f"delete {task_name}"):
                del st.session_state.tasks[task_name]
                st.success(f"Task '{task_name}' deleted!")
                st.rerun()


# Log Section
with st.expander("Logs"):
    if st.session_state.log:
        st.table(st.session_state.log)
    else:
        st.write("No log entries yet.")
