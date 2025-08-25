from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Client.on_message(filters.command("start"))
async def start_cmd(bot, message):
    buttons = [
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Rakesh_HSR"),
            InlineKeyboardButton("😓 Help", callback_data="help_cmd"),
        ],
        [
            InlineKeyboardButton("🤔 About Dev", callback_data="about_dev"),
        ]
    ]
    await message.reply_text(
        text=f"👋 Hello **{message.from_user.first_name}**!\n\n"
             "I am your multi-usage bot.\n"
             "Use the buttons below 👇",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query()
async def cb_handler(bot, query: CallbackQuery):
    if query.data == "help_cmd":
        await query.message.edit_text("📖 Help Menu\n\nUse /help to see all commands.")
    elif query.data == "about_dev":
        await query.message.edit_text("🤔 About Developer\n\nThis Bot is Made By botskingdom ❤️")
