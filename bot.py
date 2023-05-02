import os
import logging
import configparser
from drive_api import GoogleDrive
from discord_bot import ImageUploaderBot

from common import CONFIG_FILE

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Read configuration
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    discord_token = config.get('Discord', 'Token')
    specific_person_id = int(config.get('Discord', 'SpecificPersonID'))
    g_drive_credentials = config.get('GoogleDrive', 'CredentialsFile')
    g_drive_folder_id = config.get('GoogleDrive', 'FolderID')

    # Initialize Google Drive API
    drive_api = GoogleDrive(g_drive_credentials, g_drive_folder_id)

    # Initialize and run the bot
    bot = ImageUploaderBot(drive_api, discord_token, specific_person_id)
    bot.run()
