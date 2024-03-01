from telegram import Update
from telegram.ext import ContextTypes

from core.decorators import command_handler

@command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Sends explanation on how to use the bot."""

    await update.message.reply_text("Hello")