"""
Google Drive helper for Lesson Plan Notes.

Folder hierarchy on Drive:
  <GOOGLE_DRIVE_ROOT_FOLDER_ID>   (one shared folder for the whole ERP)
    └── <SchoolName>/
          └── <ClassName>/
                └── <SubjectName>/
                      └── <uploaded files>

Multiple schools are automatically isolated by their name subfolder.
Each file is made viewable by anyone with the link (read-only).
"""
import io
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
_service_cache = None


def _get_service():
    global _service_cache
    if _service_cache is None:
        creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )
        _service_cache = build('drive', 'v3', credentials=creds, cache_discovery=False)
    return _service_cache


def _get_or_create_folder(service, name, parent_id):
    """Return existing folder ID or create a new one under parent_id."""
    safe_name = name.replace("'", "\\'")
    query = (
        f"name='{safe_name}' "
        f"and mimeType='application/vnd.google-apps.folder' "
        f"and '{parent_id}' in parents "
        f"and trashed=false"
    )
    res = service.files().list(
        q=query,
        fields='files(id)',
        pageSize=1,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    files = res.get('files', [])
    if files:
        return files[0]['id']

    folder = service.files().create(
        body={
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id],
        },
        fields='id',
        supportsAllDrives=True,
    ).execute()
    return folder['id']


def upload_note(file_obj, filename, mime_type, school_name, class_name, subject_name):
    """
    Upload file_obj to Drive under School/Class/Subject.
    Returns (file_id, view_url, download_url).
    Raises on error.
    """
    service = _get_service()
    root_id = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID

    school_folder  = _get_or_create_folder(service, school_name,  root_id)
    class_folder   = _get_or_create_folder(service, class_name,   school_folder)
    subject_folder = _get_or_create_folder(service, subject_name, class_folder)

    file_obj.seek(0)
    media = MediaIoBaseUpload(
        io.BytesIO(file_obj.read()),
        mimetype=mime_type,
        resumable=True,
    )
    uploaded = service.files().create(
        body={'name': filename, 'parents': [subject_folder]},
        media_body=media,
        fields='id',
        supportsAllDrives=True,
    ).execute()
    file_id = uploaded['id']

    # Make readable by anyone with the link
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
        supportsAllDrives=True,
    ).execute()

    info = service.files().get(
        fileId=file_id,
        fields='webViewLink,webContentLink',
        supportsAllDrives=True,
    ).execute()

    return file_id, info.get('webViewLink', ''), info.get('webContentLink', '')


def delete_note(file_id):
    """Move a Drive file to trash (silent on error)."""
    try:
        _get_service().files().update(
            fileId=file_id,
            body={'trashed': True},
            supportsAllDrives=True,
        ).execute()
    except Exception as exc:
        print(f"Drive trash error for {file_id}: {exc}")
