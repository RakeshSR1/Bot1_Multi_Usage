from pyrogram import Client, filters

# Store folder ID in memory (you can change this to a database or file storage)
GDRIVE_FOLDER_ID = None

@Client.on_message(filters.command("gd_id") & filters.private)
async def set_gdrive_id(client, message):
    global GDRIVE_FOLDER_ID
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        GDRIVE_FOLDER_ID = args[1].strip()
        await message.reply(f"✅ Google Drive Folder ID set to:\n`{GDRIVE_FOLDER_ID}`")
    else:
        if GDRIVE_FOLDER_ID:
            await message.reply(f"📂 Current Google Drive Folder ID:\n`{GDRIVE_FOLDER_ID}`")
        else:
            await message.reply("⚠ No Google Drive Folder ID set.\n\nUse:\n`/gd_id YOUR_FOLDER_ID`")
