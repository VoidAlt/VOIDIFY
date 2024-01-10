import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

IS_BROADCASTING = False

@app.on_message(filters.command("broadcast") & SUDOERS)
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING

    if not IS_BROADCASTING:
        IS_BROADCASTING = True
        await message.reply_text("Broadcast started. Please follow the instructions.")

        # Ask for a picture
        await message.reply_text("Send a picture for the broadcast.")
        picture_message = await app.ask(message.chat.id, "Waiting for picture...")

        # Ask for a caption
        await message.reply_text("Provide a caption for the broadcast.")
        caption_message = await app.ask(message.chat.id, "Waiting for caption...")

        # Ask for inline buttons
        await message.reply_text("Send inline buttons for confirmation.")
        buttons_message = await app.ask(message.chat.id, "Waiting for buttons...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Confirm", callback_data="confirm")]]))

        # Process the received messages
        picture = picture_message.photo[-1] if picture_message.photo else None
        caption = caption_message.text if caption_message.text else "No caption provided"
        buttons = buttons_message.text if buttons_message.text else "No buttons provided"

        await message.reply_text("Broadcast completed.")

        IS_BROADCASTING = False
