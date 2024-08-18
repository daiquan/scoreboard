import streamlit as st
@st.dialog("introduce you")
def introduceYou():
    st.write("Introduce yourself")
    kid_name = st.text_input("Enter your star's name:", st.session_state.kid_name)
    kid_age = st.number_input("Enter your star's age:", min_value=0, max_value=100, value=st.session_state.kid_age)

    if st.button("OK"):
        if kid_name:
            st.session_state.kid_name = kid_name
        if kid_age:
            st.session_state.kid_age = kid_age

        st.rerun()

@st.dialog("Create New Task")
def create_task():
    new_task_name = st.text_input("New Task Name:")
    new_task_score = st.number_input("Task Score:", min_value=-100, max_value=100, value=1)
    taskBtn = st.button("Create")
    if taskBtn:
        st.session_state.tasks[new_task_name] = new_task_score
        st.success(f"Task '{new_task_name}' created!")
        st.rerun()