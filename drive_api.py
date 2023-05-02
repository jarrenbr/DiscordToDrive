import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class GoogleDrive:
    def __init__(self, credentials_file, folder_id):
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        self.service = build('drive', 'v3', credentials=credentials)
        self.folder_id = folder_id

    async def upload_to_drive(self, file_path, file_name, mime_type, retries=3):
        for attempt in range(retries):
            try:
                file_metadata = {
                    'name': file_name,
                    'parents': [self.folder_id],
                }
                media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
                self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                return True
            except HttpError as error:
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f'An error occurred: {error}')
                    return False
