# Image Uploader Discord Bot

This Discord bot uploads images reacted to by a specific user to a Google Drive folder. The bot is designed to be resilient, scalable, and production-ready. This project is assisted by AI such as GitHub Copilot and ChatGPT.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Bot](#running-the-bot)
5. [Code Structure](#code-structure)
6. [Contributing](#contributing)

## Prerequisites

Before using the bot, ensure you have the following:

1. Python 3.7 or later
2. A Discord bot token from the Discord Developer Portal
3. A Google API service account with access to Google Drive API
4. The folder ID in Google Drive where you want to upload the images
5. The user ID of the specific person whose reactions should trigger the upload

## Installation

1. Clone this repository or download the source code.

2. Install the required packages using pip:

```sh
pip install discord.py aiohttp google-auth google-api-python-client google-auth-httplib2
```

## Configuration

1. Update the `config.ini` file with your credentials and settings:

```ini
[Discord]
Token = your_discord_bot_token
SpecificPersonID = 123456789

[GoogleDrive]
CredentialsFile = your_google_drive_credentials.json
FolderID = your_google_drive_folder_id
```

Replace the placeholders with your actual values:

- `your_discord_bot_token`: Your Discord bot token from the Discord Developer Portal.
- `123456789`: The user ID of the specific person whose reactions should trigger the upload.
- `your_google_drive_credentials.json`: The path to your Google API service account JSON key file.
- `your_google_drive_folder_id`: The folder ID in Google Drive where you want to upload the images.

## Running the Bot

To run the bot, execute `bot.py`:

```sh
python bot.py
```

The bot will connect to Discord and start monitoring reactions. Images reacted to by the specific user will be uploaded to the configured Google Drive folder.

## Code Structure

The code is organized into three main files:

- `bot.py`: The main script that initializes and runs the bot.
- `discord_bot.py`: Contains the `ImageUploaderBot` class, which handles Discord events and manages the upload queue.
- `drive_api.py`: Contains the `GoogleDrive` class, which provides a wrapper for interacting with the Google Drive API.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork this repository and create a new branch for your feature or bugfix.
2. Make your changes, ensuring that the code is well-structured and follows best practices.
3. Add tests if applicable and make sure existing tests pass.
4. Update the documentation if necessary.
5. Submit a pull request with a clear description of your changes.

Before submitting a pull request, please make sure that your code is well-documented, follows best practices, and passes all tests.
