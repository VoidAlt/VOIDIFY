from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import get_served_chats, get_served_users, get_client
from config import adminlist

IS_BROADCASTING = False
broadcast_data = {}

@app.on_message(filters.command("broadcast") & SUDOERS)
async def broadcast_message(client, message):
    global IS_BROADCASTING
    chat_id = message.chat.id

    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("Please provide a message to broadcast.")

        query = message.text.split(None, 1)[1]
        IS_BROADCASTING = True
        await message.reply_text("Send a picture for your broadcast.")

        broadcast_data[chat_id] = {"query": query}

# Handle picture sent by owner
@app.on_message(filters.photo & filters.private)
async def receive_picture(client, message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    broadcast_data[chat_id]["photo"] = file_id

    await message.reply_text("Great! Now send the caption for your broadcast.")

# Handle caption sent by owner
@app.on_message(filters.text & filters.private)
async def receive_caption(client, message):
    chat_id = message.chat.id
    caption = message.text
    broadcast_data[chat_id]["caption"] = caption

    await message.reply_text("Now, send the inline buttons for your broadcast in JSON format.")

# Handle inline buttons sent by owner
@app.on_message(filters.text & filters.private)
async def receive_inline_buttons(client, message):
    chat_id = message.chat.id
    inline_buttons = message.text
    broadcast_data[chat_id]["buttons"] = inline_buttons

    preview_message = f"Preview your broadcast:\n\n{caption}"
    buttons = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    await app.send_photo(chat_id, photo=broadcast_data[chat_id]["photo"], caption=preview_message, reply_markup=buttons)

# Handle /confirm command to broadcast the message
@app.on_message(filters.command("confirm") & filters.private & SUDOERS)
async def confirm_broadcast(client, message):
    chat_id = message.chat.id
    if chat_id in broadcast_data:
        query = broadcast_data[chat_id]["query"]
        photo = broadcast_data[chat_id]["photo"]
        caption = broadcast_data[chat_id]["caption"]
        inline_buttons = broadcast_data[chat_id]["buttons"]

        sent = 0
        pin = 0
        await message.reply_text("Broadcast in progress...")

        # Add your broadcasting logic here using the provided data (query, photo, caption, inline_buttons)
        
        # Reset broadcast_data
        del broadcast_data[chat_id]
        IS_BROADCASTING = False
    else:
        await message.reply_text("No ongoing broadcast found.")
