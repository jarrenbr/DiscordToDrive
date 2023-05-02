import asyncio
import configparser
import unittest
from unittest.mock import Mock, AsyncMock, patch

from discord_bot import ImageUploaderBot
from drive_api import GoogleDrive

from common import CONFIG_FILE

# These tests check if the upload_to_drive method in GoogleDrive and the download_file method in ImageUploaderBot are
# working as expected. Mock objects and patching are used to isolate the methods being tested from external services
# and dependencies.

# Read the configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

discord_token = config.get('Discord', 'Token')
specific_person_id = int(config.get('Discord', 'SpecificPersonID'))
g_drive_credentials = config.get('GoogleDrive', 'CredentialsFile')
g_drive_folder_id = config.get('GoogleDrive', 'FolderID')


class TestGoogleDrive(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.drive_api = GoogleDrive(g_drive_credentials, g_drive_folder_id)

    @patch("googleapiclient.discovery.build")
    def test_upload_to_drive(self, mock_build):
        file_path = "test_image.png"
        file_name = "test_image.png"
        mime_type = "image/png"

        mock_service = Mock()
        mock_service.files.return_value.create.return_value.execute.return_value = {"id": "file_id"}
        mock_build.return_value = mock_service

        success = self.loop.run_until_complete(self.drive_api.upload_to_drive(file_path, file_name, mime_type))
        self.assertTrue(success)


class TestImageUploaderBot(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.drive_api = AsyncMock(spec=GoogleDrive)
        self.bot = ImageUploaderBot(self.drive_api, discord_token, specific_person_id)

    @patch("aiohttp.ClientSession.get")
    def test_download_file(self, mock_get):
        url = "https://example.com/image.png"
        filename = "image.png"

        async def fake_response():
            response = AsyncMock()
            response.status = 200
            response.read.return_value = b"fake_image_data"
            return response

        mock_get.return_value.__aenter__.return_value = fake_response()

        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            success = self.loop.run_until_complete(self.bot.download_file(url, filename))
            self.assertTrue(success)
            mock_file.assert_called_once_with(filename, "wb")
            mock_file.return_value.write.assert_called_once_with(b"fake_image_data")


if __name__ == "__main__":
    unittest.main()
