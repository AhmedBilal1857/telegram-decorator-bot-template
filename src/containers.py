
import logging.config
from dependency_injector import containers, providers
import core.bot


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    bot_config = providers.Singleton(
        core.bot.BotConfig,
        config.telegram.bot_token
    )

    bot_service = providers.Factory(
        core.bot.TelegramBotService,
        bot_config = bot_config
    )