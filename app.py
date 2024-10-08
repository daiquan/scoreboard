import streamlit as st
from datetime import datetime
import json 
from helper.st_helper import *
from helper.localFile import *
from helper.helper_fn import *


# Initialize session state for kid's info, score, log, tasks
if 'cindy_dai' not in st.session_state:
    if 'fdb' not in st.session_state:
        st.session_state.fdb = init_firedb()

    st.session_state.cindy_dai = get_profile_from_firebase(st.session_state.fdb,'cindy_dai')


def save_to_firedb():
    save_profile_to_firebase(st.session_state.fdb,'cindy_dai',st.session_state['cindy_dai'])
# loaded_data = get_profile_from_firebase(st.session_state.fdb,'cindy_dai')
# if loaded_data:
#     st.session_state.update(loaded_data)
# else:
#     save_profile_to_firebase(st.session_state.fdb,to_snake_case(st.session_state.kid_name),st.session_state.to_dict())
#     loaded_data = get_profile_from_firebase(st.session_state.fdb,to_snake_case(st.session_state.kid_name))

#load logs
# Keep only the last 20 log entries
st.session_state['cindy_dai']['log_display'] = st.session_state['cindy_dai']['log'][-20:][::-1] 
st.session_state['cindy_dai']['log'] = st.session_state['cindy_dai']['log'][-20:]
# Function to add an entry to the log
def add_to_log(action, points):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state['cindy_dai']['log'].append({"timestamp": timestamp, "action": action, "points": points})
    save_to_firedb()
    st.rerun()
def undo_last():
    last = st.session_state['cindy_dai']['log'].pop()
    st.session_state['cindy_dai']['score'] = st.session_state['cindy_dai']['score']-last['points']
    st.rerun()


# Kid's Information Section
st.title("🌟 Little Star's Scoreboard! 🌟")
st.caption(f"_{st.session_state['cindy_dai']['kid_name']}'s_ Scoreboard")

#layout
stars = "🌟" * (int)(st.session_state['cindy_dai']['score']/5)
st.write(stars) 

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
            st.session_state['cindy_dai']['score'] += adjustment
            add_to_log("Score changed", adjustment)

        if option == '💰':
            st.session_state['cindy_dai']['score'] += adjustment * 5
            add_to_log("Money changed", adjustment)

        save_to_firedb()
        st.rerun()

def delTask(task_name):
    del st.session_state['cindy_dai']['tasks'][task_name]
    st.success(f"Task '{task_name}' deleted!")
    add_to_log(f"Deleted task '{task_name}'", task_score)
    save_to_firedb()
    st.rerun()

def createTask(task_name, task_score):
    st.session_state['cindy_dai']['score'] += task_score
    add_to_log(f"Completed task '{task_name}'", task_score)
    save_to_firedb()
    st.rerun()


with top_col1:
    with st.container(border=1):
        st.markdown(f"# Score: {st.session_state['cindy_dai']['score']}")
        st.markdown(f"### = ${st.session_state['cindy_dai']['score'] / 5.0}")
        with st.expander("Change Score or Money"):
            changeScorePanel()  
        if st.button("Undo last", type="primary"):
            undo_last()

        
with top_col2:
    with st.container(border=1):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create a Task",type="primary"):
                create_task()
        with col2:
            on = st.toggle("Manage Tasks")

        col3, col4 = st.columns(2)
        with col3:
            if st.session_state['cindy_dai']['tasks']:
                for task_name, task_score in st.session_state['cindy_dai']['tasks'].items():
                    if st.button(f"{task_name} ({task_score})",type="secondary"):
                        createTask(task_name, task_score)
        with col4:
            if on and st.session_state['cindy_dai']['tasks']:
                for task_name, task_score in st.session_state['cindy_dai']['tasks'].items():
                    if st.button(f"❌ {task_name}"):
                        delTask(task_name)
    

    

if st.session_state['cindy_dai']['kid_name'] == "":
    introduceYou()


# Display and manage existing tasks



# Log Section
with st.expander("Logs", expanded=True):
    if st.session_state['cindy_dai']['log_display']:
        st.table(st.session_state['cindy_dai']['log_display'])
    else:
        st.write("No log entries yet.")
