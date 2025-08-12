from pyrogram import Client, filters
import zipfile, os
from bot.helpers.drive import GoogleDriveHelper
from bot.helpers.progress import progress_bar  # existing helper in repo
from pyrogram.types import Message

@Client.on_message(filters.command("Gdrive_Link"))
async def gdrive_link_cmd(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("⚠️ Reply to a video or zip file.")

    # Download with progress
    file_path = await message.reply_to_message.download(
        progress=progress_bar,
        progress_args=("📥 Downloading...", message)
    )

    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall("unzipped")

        links = []
        for f in os.listdir("unzipped"):
            f_path = os.path.join("unzipped", f)
            link = GoogleDriveHelper().upload(
                f_path,
                message,  # so it can also show progress
                f"☁️ Uploading {f}..."
            )
            links.append(f"📁 {f}: {link}")
        await message.reply_text("\n".join(links))

    else:
        link = GoogleDriveHelper().upload(
            file_path,
            message,
            f"☁️ Uploading {os.path.basename(file_path)}..."
        )
        await message.reply_text(f"🎥 {os.path.basename(file_path)}: {link}")

    os.remove(file_path)
