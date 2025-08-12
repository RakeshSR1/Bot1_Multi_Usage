import os
import logging
from pyrogram import Client
from bot import (
from gdrive_id_handler import *
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
from pyrogram import Client, filters

# Store Google Drive Folder ID (temporary storage, not permanent database)
gdrive_folder_id = None

@Client.on_message(filters.command("gd_id") & filters.private)
async def set_gdrive_id(client, message):
    global gdrive_folder_id
    try:
        # If user sends /gd_id without argument, show current ID
        if len(message.command) == 1:
            if gdrive_folder_id:
                await message.reply_text(f"✅ Current Google Drive Folder ID: `{gdrive_folder_id}`")
            else:
                await message.reply_text("❌ No Google Drive Folder ID set yet.\nUsage: `/gd_id FOLDER_ID`", quote=True)
            return
        
        # If user sends /gd_id with argument, set it
        gdrive_folder_id = message.command[1]
        await message.reply_text(f"✅ Google Drive Folder ID set to:\n`{gdrive_folder_id}`", quote=True)
    
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{str(e)}`", quote=True)

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    plugins = dict(
        root="bot/plugins"
    )
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
