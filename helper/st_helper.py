import streamlit as st
from helper.localFile import *
@st.dialog("introduce you")
def introduceYou():
    st.write("Introduce yourself")
    kid_name = st.text_input("Enter your star's name:", st.session_state['cindy_dai']['kid_name'])
    kid_age = st.number_input("Enter your star's age:", min_value=0, max_value=100, value=st.session_state['cindy_dai']['kid_age'])

    if st.button("OK"):
        if kid_name:
            st.session_state['cindy_dai']['kid_name'] = kid_name
        if kid_age:
            st.session_state['cindy_dai']['kid_age'] = kid_age

        st.rerun()

@st.dialog("Create New Task")
def create_task():
    new_task_name = st.text_input("New Task Name:")
    new_task_score = st.number_input("Task Score:", min_value=-100, max_value=100, value=1)
    taskBtn = st.button("Create")
    if taskBtn:
        st.session_state['cindy_dai']['tasks'][new_task_name] = new_task_score
        st.success(f"Task '{new_task_name}' created!")
        save_profile_to_firebase(st.session_state.fdb,'cindy_dai',st.session_state['cindy_dai'])
        st.rerun()