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
    folder_path = "profiles"
    file_path = f"{folder_path}/{file_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return None 
    # Try to load data from the file 
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)

    # Update the session state
    return loaded_data

import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_firedb():
    try:
        # Attempt to get an existing app instance
        firebase_admin.get_app()  
        print("Firebase app already initialized. Skipping initialization.")
    except ValueError:
        # If no app exists, initialize it
        firebase_config = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        # cred = credentials.Certificate("./firebase/scoreboard-83388-firebase-adminsdk-h2hvp-d9206869d5.json")
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        print("Firebase app initialized.")
    fdb = firestore.client()
    return fdb


def save_profile_to_firebase(fdb,id,data):
    try:

        doc = fdb.collection("profile").document(id)
        doc.set(data)
        st.success("data saved to firebase!")
    except Exception as e:
        st.error(f"Error save to firebase: {e}")

def get_profile_from_firebase(fdb,id):
    try:

        doc = fdb.collection("profile").document(id).get()
        if doc.exists:
            profile_json = json.loads(json.dumps(doc.to_dict()))
            print(profile_json)
            return profile_json
    except Exception as e:
        st.error(f"Error to fetch {id} from firebase: {e}")
