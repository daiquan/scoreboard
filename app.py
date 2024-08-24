import streamlit as st
from datetime import datetime
import json 
from helper.st_helper import *
from helper.localFile import *


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


loaded_data = load_session_state_from_local_file()
if loaded_data:
    st.session_state.update(loaded_data)
else:
    save_session_state_to_local_file(st.session_state.to_dict())
    loaded_data = load_session_state_from_local_file()

# Function to add an entry to the log
def add_to_log(action, points):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.log.append({"timestamp": timestamp, "action": action, "points": points})
    # Keep only the last 20 log entries
    st.session_state.log = st.session_state.log[-20:]

# Kid's Information Section
st.title("🌟 Little Star's Scoreboard! 🌟")
st.caption("_Cindy's_ Scoreboard")

#layout
top_col1, top_col2 = st.columns(2)
with top_col2:
    left_col, right_col = st.columns([3,1])

#panels
def changeScorePanel():
    option = st.radio("5 pts → $1", ("#️⃣", '💰'),horizontal=True)
    # Score Adjustment

    adjustment = st.number_input("Change:", min_value=-100, max_value=100, value=0)
    if st.button("Apply"):
        if option == '#️⃣':
            st.session_state.score += adjustment
            add_to_log("Score changed", adjustment)

        if option == '💰':
            st.session_state.score += adjustment * 5
            add_to_log("Money changed", adjustment)

        save_session_state_to_local_file(st.session_state.to_dict())
        st.rerun()

def delTask(task_name):
    del st.session_state.tasks[task_name]
    st.success(f"Task '{task_name}' deleted!")
    add_to_log(f"Deleted task '{task_name}'", task_score)
    save_session_state_to_local_file(st.session_state.to_dict())
    st.rerun()

def createTask(task_name, task_score):
    st.session_state.score += task_score
    add_to_log(f"Completed task '{task_name}'", task_score)
    save_session_state_to_local_file(st.session_state.to_dict())
    st.rerun()
with top_col1:
    st.markdown(f"# Total Score: {st.session_state.score}")
    st.markdown(f"### = ${st.session_state.score / 5.0}")
    with st.expander("Change Score or Money"):
        changeScorePanel()  

        
with top_col2:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create a Task"):
            create_task()
    with col2:
        on = st.toggle("Manage Tasks")

    col3, col4 = st.columns(2)
    with col3:
        if st.session_state.tasks:
            for task_name, task_score in st.session_state.tasks.items():
                if st.button(f"{task_name} ({task_score})"):
                    createTask(task_name, task_score)
    with col4:
        if on and st.session_state.tasks:
            for task_name, task_score in st.session_state.tasks.items():
                if st.button(f"❌ {task_name}"):
                    delTask(task_name)
    

    

if st.session_state.kid_name == "":
    introduceYou()


# Display and manage existing tasks



# Log Section
with st.expander("Logs"):
    if st.session_state.log:
        st.table(st.session_state.log)
    else:
        st.write("No log entries yet.")
