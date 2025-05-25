import os
import io
from .Google import Create_Service
import httplib2
from google_auth_httplib2 import AuthorizedHttp
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload

CLIENT_SECRET_FILE = 'static/aDrive/client_secret.json'
API_NAME = 'drive'
API_VERSION = "v3"
SCOPES = [ 'https://www.googleapis.com/auth/drive'  ]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_folder(service, project_name, folder_id = None):
    file_metadata = {
        'name' : project_name,
        'mimeType' : 'application/vnd.google-apps.folder',
        'parents' : [folder_id]
    }

    service.files().create(body=file_metadata).execute()
    print(f"Folder '{project_name}' created successfully.")


def check_folder_exists(service, folder_name, parent_folder_id=None):
    """
    Checks if a folder exists in Google Drive by its name.
    
    If a parent folder ID is provided, it will search within that folder.
    """
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'"
    
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    
    # Execute the search query to find the folder
    results = service.files().list(q=query, fields="files(id, name)").execute()
    
    files = results.get('files', [])
    
    if files:
        # If folder(s) are found, return True (indicating folder exists)
        return True, files[0]  # Returning the first folder found (if multiple)
    else:
        # If no folder is found
        return False, None


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


def get_file_id_by_name(service, file_name):
    query = f"name = '{file_name}'"
    
    # Execute the search query
    results = service.files().list(q=query, fields="files(id, name)").execute()
    
    files = results.get('files', [])
    
    # If no files are found
    if not files:
        print(f"No file found with the name: {file_name}")
        return None
    
    # If multiple files are found, print them out (can be handled as needed)
    if len(files) > 1:
        print(f"Warning: Multiple files found with the name '{file_name}'")
        for file in files:
            print(f"File ID: {file['id']}, Name: {file['name']}")
    
    # Return the file ID of the first matching file (or the one you want)
    return files[0]['id']


def get_file_ids_in_folder(service, folder_id):
    """Get all file IDs and names in a folder."""
    query = f"'{folder_id}' in parents"
    
    # Execute the search query to find the files within the folder
    results = service.files().list(q=query, fields="files(id, name)").execute()
    
    files = results.get('files', [])
    
    if not files:
        print(f"No files found in the folder with ID: {folder_id}")
        return []
    
    # Return a list of file IDs and file names
    return [(file['id'], file['name']) for file in files]


def download_file(service, file_id, file_name, download_folder):
    """Download a file using its file ID."""
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress {file_name}: {status.progress() * 100}%")

    fh.seek(0)
    with open(os.path.join(download_folder, file_name), 'wb') as f:
        f.write(fh.read())
    print(f"Downloaded {file_name}")


def download_file_as_bytes(service, file_id):
    request = service.files().get_media(fileId=file_id)
    from io import BytesIO
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return fh.getvalue()


def upload_files(service,file_path, file_name, mime_type, folder_id = None):
    file_metadata = {
        'name' : file_name,
        'parents' : [folder_id]
    }

    # Use MediaFileUpload with resumable=True
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    # Set timeout (300 seconds = 5 minutes)
    http = httplib2.Http(timeout=300)
    authorized_http = AuthorizedHttp(service._http.credentials, http=http)
    
    # Rebuild the Drive service with the increased timeout
    drive_service = build('drive', 'v3', http=authorized_http)

    request = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        except Exception as e:
            print(f"An error occurred during upload: {e}")
            raise

    print(f"Upload complete. File ID: {response.get('id')}, File Name: {file_name}")
    return response.get('id')


def upload_files_directly(service,file_obj, file_name, mime_type, folder_id = None):
    file_metadata = {
        'name' : file_name,
        'parents' : [folder_id] if folder_id else []
    }

    # Use MediaFileUpload with resumable=True
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
