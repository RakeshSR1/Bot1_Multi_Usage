from bot import SUPPORT_CHAT_LINK
from pyrogram import Client, filters
from bot.config import Messages as tr
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.private & filters.incoming & filters.command(['start']), group=2)
def _start(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.START_MSG.format(message.from_user.mention),
        reply_to_message_id = message.message_id
    )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']), group=2)
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(c, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    c.edit_message_text(chat_id = chat_id,    message_id = message_id,
        text = tr.HELP_MSG[msg],    reply_markup = InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '-->', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):

        button = [
            [
             InlineKeyboardButton(text = 'Support Chat', url = SUPPORT_CHAT_LINK),

                help_text = """
**📝 Bot Commands List**

🔹 **General**
- `/start` → Start the bot
- `/help` → Show this help message

🔹 **Merge Files**
- `/merge_start` → Start collecting files to merge
- `/merge_end` → Merge the collected files into one

🔹 **Zip Files**
- `/zip_start` → Start collecting files for ZIP
- `/zip_end` → Create ZIP file

🔹 **Audio Tools**
- `/remove_audio` → Remove audio from a given video

🔹 **Google Drive**
- `/gdup` → Upload to Google Drive
- `/setgd` → Set Google Drive Folder ID
- `/gd_id` → Show current Google Drive Folder ID

🔹 **Other**
- `/showthumb` → Show your thumbnail
- `/setthumb` → Set custom thumbnail
- `/delthumb` → Delete thumbnail
"""
             InlineKeyboardButton(text = 'Feature Request', url = "https://github.com/viperadnan-git/google-drive-telegram-bot/issues/new")
            ],
            [InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}")]

        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '-->', callback_data = f"help+{pos+1}")
            ],
        ]
    return button

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

@Client.on_callback_query()
async def cb_handler(bot, query: CallbackQuery):
    if query.data == "help_cmd":
        await query.message.edit_text("📖 Help Menu\n\nUse /help to see all commands.")
    elif query.data == "about_dev":
        await query.message.edit_text("🤔 About Developer\n\nThis bot is made by @YourUsername ❤️")
