import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import json
import io

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

# Google Drive API setup (replace with your actual credentials path)
SERVICE_ACCOUNT_FILE = 'keys/score-board-google-drive-key.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Function to save session state to Google Drive
def save_session_state_to_drive():
    # File metadata (you can customize the file name and parent folder if needed)
    file_metadata = {
        'name': 'streamlit_session_state.json',
        'mimeType': 'application/json'
    }
    session_state_dict = st.session_state.to_dict()
    # Serialize session state to JSON
    session_state_json = json.dumps(session_state_dict)


    # Create a MediaFileUpload object
    media = MediaFileUpload(
        'streamlit_session_state.json', 
        mimetype='application/json', 
        resumable=True
    )

    # Search for an existing file
    query = "name='streamlit_session_state.json' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])

    if items:
        # If the file exists, update it
        file_id = items[0]['id']
        file = service.files().update(fileId=file_id, media_body=media, fields='id').execute()
        st.success(f'Session state updated on Google Drive (File ID: {file.get("id")})')
    else:
        # If the file doesn't exist, create it
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        st.success(f'Session state saved to Google Drive (File ID: {file.get("id")})')

# Add a button to trigger saving
if st.button("Save Session State to Drive"):
    save_session_state_to_drive()


def load_session_state_from_drive():
    # Search for the file
    query = "name='streamlit_session_state.json' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])

    if not items:
        st.warning('No saved session state found on Google Drive.')
        return

    # Get the file ID
    file_id = items[0]['id']

    # Download the file content
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    # Deserialize the JSON content
    fh.seek(0)
    loaded_data = json.loads(fh.read().decode())

    # Update the session state
    st.session_state.update(loaded_data)
    st.success('Session state loaded from Google Drive!')

# Add a button to trigger loading
if st.button("Load Session State from Drive"):
    load_session_state_from_drive()

# Display the session state data (you can customize how you want to display it)
st.write("Current Session State:")
st.write(st.session_state)

def save_session_state_to_local_file():
    # Convert SessionStateProxy to a dictionary
    session_state_dict = st.session_state.to_dict()

    # Write the current session state dictionary to the file, overwriting any existing content
    with open('streamlit_session_state.json', 'w') as f:
        json.dump(session_state_dict, f, indent=4)  # indent for better readability

    st.success('Session state saved to local file! (Overwritten)')

# Add a button to trigger saving
if st.button("Save Session State to Local File (Overwrite)"):
    save_session_state_to_local_file()