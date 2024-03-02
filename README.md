# Template for Python Telegram bot

This is a template for easy uasge of python-telegram-bot. No need to register handlers explictly in your application. Just focus on the handler login not on setting up the project.  

# Table of Contents
1. [Usage](#usage)

## Usage
It is pretty simple to use this template just a take pull, create a file with having prefix "handler" and use the following decorators on your functions to define the type of handler you want and will be registered automatically.

1. @command_handler
2. @message_handler
3. @conversation_handler
4. @error_handler

```python
# File name command_handler.py

@command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hello")
```