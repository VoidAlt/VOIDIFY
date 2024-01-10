from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Client("6432487919:AAGnYcWl3VRWNeq8ToeOxpHo2bJQzhKK9EA", api_id=17807190, api_hash="87d7db377d986df687a32d8230314e7f")

broadcast_data = {}

# Command handler for /broadcast
@app.on_message(filters.command("broadcast") & filters.private & filters.user("owner_user_id"))
def start_broadcast(_, message):
    message.reply_text("Send a picture for your broadcast.")

# Handle picture sent by owner
@app.on_message(filters.private & filters.photo & filters.user("owner_user_id"))
def receive_picture(_, message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    broadcast_data[chat_id] = {"photo": file_id}
    
    message.reply_text("Great! Now send the caption for your broadcast.")

# Handle caption sent by owner
@app.on_message(filters.private & filters.text & filters.user("owner_user_id"))
def receive_caption(_, message):
    chat_id = message.chat.id
    caption = message.text
    broadcast_data[chat_id]["caption"] = caption
    
    message.reply_text("Now, send the inline buttons for your broadcast in JSON format.")

# Handle inline buttons sent by owner
@app.on_message(filters.private & filters.text & filters.user("owner_user_id"))
def receive_inline_buttons(_, message):
    chat_id = message.chat.id
    inline_buttons = message.text
    broadcast_data[chat_id]["buttons"] = inline_buttons
    
    preview_message = f"Preview your broadcast:\n\n{caption}"
    buttons = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    app.send_photo(chat_id, photo=broadcast_data[chat_id]["photo"], caption=preview_message, reply_markup=buttons)

# Handle /confirm command to broadcast the message
@app.on_message(filters.command("confirm") & filters.private & filters.user("owner_user_id"))
def confirm_broadcast(_, message):
    chat_id = message.chat.id
    if chat_id in broadcast_data:
        app.send_photo(chat_id, photo=broadcast_data[chat_id]["photo"], caption=broadcast_data[chat_id]["caption"])
        del broadcast_data[chat_id]
        message.reply_text("Broadcast sent successfully!")
    else:
        message.reply_text("No ongoing broadcast found.")

app.run()
