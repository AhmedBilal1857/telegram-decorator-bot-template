import logging
import zope.interface
from telegram.ext import Application

from core.helper import TelegramHelper


class BotService(zope.interface.Interface):
    def start(self):
        pass

class BotConfig():
    def __init__(self, token: str) -> None:
        self.token = token

@zope.interface.implementer(BotService)
class TelegramBotService:
    
    def __init__(self, bot_config: BotConfig):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.application = Application.builder().token(bot_config.token).build()
        self.telegram_helper = TelegramHelper()
        self.loaded_modules = None

        self.logger.debug("Bot instantiated.")
    #----------------------------------------------------------------------------
    def start(self):
        self.logger.info("Starting bot...")
        self.loaded_modules = self.load_modules()
        self.register_handlers()
        self.logger.info("Bot started.")

        self.application.run_polling()
    #----------------------------------------------------------------------------
    def load_modules(self):
        return self.telegram_helper.load_handler_modules()
    #----------------------------------------------------------------------------
    def register_handlers(self):
        self.__register_handlers(self.application, self.loaded_modules)
    #----------------------------------------------------------------------------
    def __register_handlers(self, application: Application, modules):
        self.telegram_helper.register_handlers_from_modules(application, modules)
    #----------------------------------------------------------------------------