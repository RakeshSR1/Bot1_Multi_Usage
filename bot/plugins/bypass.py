from pyrogram import Client, filters
from shorten_berly_bypass import bypass_url

@Client.on_message(filters.command("bypass"))
async def bypass_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Send `/bypass <link>`")
    url = message.command[1]
    result = bypass_url(url)
    await message.reply_text(f"🔗 Original Link:\n{result}")
