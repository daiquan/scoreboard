import json

def save_session_state_to_local_file(session_state_dict):

    # Write the current session state dictionary to the file, overwriting any existing content
    with open('streamlit_session_state.json', 'w') as f:
        try:
            json.dump(session_state_dict, f, indent=4)  # indent for better readability
            return True
        except:
            return False

        
def load_session_state_from_local_file():
    # Try to load data from the file 
    with open('streamlit_session_state.json', 'r') as f:
        loaded_data = json.load(f)

    # Update the session state
    return loaded_data
