from pyrogram import Client, filters
import zipfile, os
from pyrogram.types import Message

zip_sessions = {}

@Client.on_message(filters.command("Start_Zip"))
async def zip_start(client, message: Message):
    user_id = message.from_user.id
    zip_sessions[user_id] = []
    await message.reply_text("📦 Zip session started. Send me the files.")

@Client.on_message(filters.command("End_Zip"))
async def zip_end(client, message: Message):
    user_id = message.from_user.id
    if user_id not in zip_sessions or not zip_sessions[user_id]:
        return await message.reply_text("⚠️ No files to zip.")

    zip_name = f"{user_id}_archive.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in zip_sessions[user_id]:
            zipf.write(file, os.path.basename(file))

    await message.reply_document(zip_name, caption="✅ Your ZIP File")
    for f in zip_sessions[user_id]: os.remove(f)
    os.remove(zip_name)
    del zip_sessions[user_id]

@Client.on_message(filters.document)
async def collect_zip_files(client, message: Message):
    user_id = message.from_user.id
    if user_id in zip_sessions:
        file_path = await message.download()
        zip_sessions[user_id].append(file_path)
        await message.reply_text(f"📥 Added to zip: `{os.path.basename(file_path)}`")
