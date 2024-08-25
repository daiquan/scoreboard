import json
import os

def save_session_state_to_local_file(file_name,session_state_dict):
    file_path = f"profiles/{file_name}"
    # Write the current session state dictionary to the file, overwriting any existing content
    with open(file_path, 'w') as f:
        try:
            json.dump(session_state_dict, f, indent=4)  # indent for better readability
            return True
        except:
            return False

        
def load_session_state_from_local_file(file_name):
    file_path = f"profiles/{file_name}"
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return None 
    # Try to load data from the file 
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)

    # Update the session state
    return loaded_data
