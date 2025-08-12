import os
import logging
from pyrogram import Client, filters
from bot import (
    APP_ID,
    API_HASH,
    BOT_TOKEN,
    DOWNLOAD_DIRECTORY
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# File to store Google Drive Folder ID
GDRIVE_ID_FILE = "gdrive_id.txt"

# Load GDrive ID from file if exists
if os.path.exists(GDRIVE_ID_FILE):
    with open(GDRIVE_ID_FILE, "r") as f:
        gdrive_folder_id = f.read().strip()
else:
    gdrive_folder_id = None

@Client.on_message(filters.command("gd_id") & filters.private)
async def set_gdrive_id(client, message):
    global gdrive_folder_id
    try:
        if len(message.command) == 1:
            if gdrive_folder_id:
                await message.reply_text(f"✅ Current Google Drive Folder ID: `{gdrive_folder_id}`")
            else:
                await message.reply_text("❌ No Google Drive Folder ID set yet.\nUsage: `/gd_id FOLDER_ID`", quote=True)
            return
        
        gdrive_folder_id = message.command[1]
        with open(GDRIVE_ID_FILE, "w") as f:
            f.write(gdrive_folder_id)
        await message.reply_text(f"✅ Google Drive Folder ID saved:\n`{gdrive_folder_id}`", quote=True)
    
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`", quote=True)

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    plugins = dict(root="bot/plugins")
    app = Client(
        "G-DriveBot",
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins,
        parse_mode="markdown",
        workdir=DOWNLOAD_DIRECTORY
    )
    LOGGER.info('Starting Bot !')
    app.run()
    LOGGER.info('Bot Stopped !')
