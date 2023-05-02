import os
import discord
import aiohttp
import mimetypes
import asyncio
from discord.ext import commands

class ImageUploaderBot(commands.Bot):
    def __init__(self, drive_api, token, specific_person_id):
        super().__init__(command_prefix='!')
        self.drive_api = drive_api
        self.token = token
        self.specific_person_id = specific_person_id
        self.upload_queue = asyncio.Queue()
        self.loop.create_task(self.process_upload_queue())

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_reaction_add(self, reaction, user):
        if user.id == self.specific_person_id:
            message = reaction.message
            for attachment in message.attachments:
                file_ext = os.path.splitext(attachment.filename)[1].lower()
                if file_ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'):
                    await self.upload_queue.put(attachment)

    async def process_upload_queue(self):
        while True:
            attachment = await self.upload_queue.get()
            await self.upload_attachment(attachment)
            self.upload_queue.task_done()

    async def upload_attachment(self, attachment):
        downloaded = await self.download_file(attachment.url, attachment.filename)
        if downloaded:
            mime_type, _ = mimetypes.guess_type(attachment.filename)
            success = await self.drive_api.upload_to_drive(attachment.filename, attachment.filename, mime_type)
            if success:
                os.remove(attachment.filename)
                print(f"{attachment.filename} uploaded to Google Drive")
            else:
                print(f"Failed to upload {attachment.filename} to Google Drive")

    async def download_file(self, url, filename, nattempts=2):
        for i in range(nattempts):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(filename,'wb') as f:
                            f.write(await resp.read())
                            return True
                    else:
                        print(f"Failed to download {filename} from {url}. Attempt #{i+1} of {nattempts}.")
            await asyncio.sleep(1)
        return False

    def run(self):
        super().run(self.token)

