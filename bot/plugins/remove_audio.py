from pyrogram import Client, filters
import os, subprocess

@Client.on_message(filters.command("RemoveAudio"))
async def remove_audio(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("⚠️ Reply to a file with `/RemoveAudio <lang>`")

    lang = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not lang:
        return await message.reply_text("⚠️ Please specify audio language.")

    file_path = await message.reply_to_message.download()
    output_file = f"no_{lang}_{os.path.basename(file_path)}"

    cmd = [
        "mkvmerge", "-o", output_file,
        "--audio-tracks", "!" + lang, file_path
    ]
    subprocess.run(cmd)

    await message.reply_document(output_file, caption=f"✅ Audio '{lang}' removed.")
    os.remove(file_path)
    os.remove(output_file)
