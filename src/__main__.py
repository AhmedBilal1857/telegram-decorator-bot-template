import logging
import sys
from dependency_injector.wiring import Provide, inject

from containers import Container
from core.bot import BotService

@inject
def main(bot_service: BotService = Provide[Container.bot_service]) -> None:
    try: 
        bot_service.start()
    except Exception as exp:
        logging.fatal(exp)

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])
