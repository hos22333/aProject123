import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
import httplib2
from google_auth_httplib2 import AuthorizedHttp

# 📁 Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'static/aDrive/service_account.json'

# 🔐 Scopes required
SCOPES = ['https://www.googleapis.com/auth/drive']

# 📁 Optional: Static folder ID in your shared drive
REPORTS_FOLDER_ID = 'your-folder-id-here'  # Replace with your actual folder ID


def get_drive_service():
    """Create and return a Google Drive service using a service account."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

service = get_drive_service()

def create_folder(service, folder_name, parent_folder_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"Folder '{folder_name}' created successfully. ID: {folder.get('id')}")


def check_folder_exists(service, folder_name, parent_folder_id=None):
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return (True, files[0]) if files else (False, None)

def get_folder_id_by_name(service, folder_name, parent_folder_id=None):
    # If parent_folder_id is provided, the query is restricted to that folder
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])
    if not items:
        print(f'No folder found with name: {folder_name}')
        return None
    return items[0]['id']

def get_file_ids_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return [(f['id'], f['name']) for f in results.get('files', [])]


def get_file_id_by_name(service, file_name):
    query = f"name = '{file_name}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    if files:
        return files[0]['id']
    print(f"No file found with name: {file_name}")
    return None


def download_file(service, file_id, file_name, download_folder):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    os.makedirs(download_folder, exist_ok=True)
    with open(os.path.join(download_folder, file_name), 'wb') as f:
        f.write(fh.read())
    print(f"Downloaded: {file_name}")


def download_file_as_bytes(service, file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh.getvalue()
    except Exception as e:
        print(f"Download error for file {file_id}: {e}")
        return None

def make_file_public(service, file_id):
    """Make a Google Drive file publicly accessible via a direct link."""
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    print(f"File {file_id} is now public.")

def upload_files(service, file_path, file_name, mime_type, folder_id=None):
    folder_id = folder_id or REPORTS_FOLDER_ID

    # Search for existing file with the same name in the folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    existing_files = service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

    if existing_files:
        print(f"File exists: {existing_files[0]['name']} (ID: {existing_files[0]['id']})")
    else:
        print("File does not exist.")

    # Delete existing file(s) with the same name
    for file in existing_files:
        print(f"Deleting existing file: {file['name']} (ID: {file['id']})")
        service.files().delete(fileId=file['id']).execute()


    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    make_file_public(service, response.get('id'))
    print(f"Upload complete. File ID: {response.get('id')}, File Name: {file_name}")
    return response.get('id')


def upload_files_directly(service, file_obj, file_name, mime_type, folder_id=None):
    folder_id = folder_id or REPORTS_FOLDER_ID

    # Search for existing file with the same name in the folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    existing_files = service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

    if existing_files:
        print(f"File exists: {existing_files[0]['name']} (ID: {existing_files[0]['id']})")
    else:
        print("File does not exist.")
        
    # Delete existing file(s) with the same name
    for file in existing_files:
        print(f"Deleting existing file: {file['name']} (ID: {file['id']})")
        service.files().delete(fileId=file['id']).execute()


    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)

    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    return response.get('id')