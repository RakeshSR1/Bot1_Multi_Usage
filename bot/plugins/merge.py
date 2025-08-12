from pyrogram import Client, filters
import os
from pyrogram.types import Message

merge_sessions = {}

@Client.on_message(filters.command("Merge_Start"))
async def merge_start(client, message: Message):
    user_id = message.from_user.id
    merge_sessions[user_id] = []
    await message.reply_text("✅ Merge session started. Send me the files.")

@Client.on_message(filters.command("Merge_End"))
async def merge_end(client, message: Message):
    user_id = message.from_user.id
    if user_id not in merge_sessions or not merge_sessions[user_id]:
        return await message.reply_text("⚠️ No files to merge.")
    
    files = merge_sessions[user_id]
    merged_file = f"{user_id}_merged.mkv"

    with open(merged_file, "wb") as outfile:
        for fname in files:
            with open(fname, "rb") as infile:
                outfile.write(infile.read())

    await message.reply_document(merged_file, caption="✅ Merged File")
    for f in files: os.remove(f)
    os.remove(merged_file)
    del merge_sessions[user_id]

@Client.on_message(filters.document)
async def collect_merge_files(client, message: Message):
    user_id = message.from_user.id
    if user_id in merge_sessions:
        file_path = await message.download()
        merge_sessions[user_id].append(file_path)
        await message.reply_text(f"📥 Added: `{os.path.basename(file_path)}`")
