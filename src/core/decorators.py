import datetime
from types import coroutine
from telegram.ext.filters import BaseFilter
from telegram.ext import BaseHandler
from core.metadata import CommandHandlerMetadata, ConversationHandlerMetadata, ErrorHandlerMetadata, MessageHandlerMetadata

#----------------------------------------------------------------------------
def command_handler(
    command: str = "", filters: BaseFilter = None, block: bool = True, has_args: bool = None
):
    def wrapper(func):
        func.metadata = CommandHandlerMetadata(command, coroutine(func), filters, block, has_args)
        return func
    return wrapper
#----------------------------------------------------------------------------
def message_handler(filters: BaseFilter, callback: coroutine, block: bool = True):
    def wrapper(func):
        func.metadata = MessageHandlerMetadata(filters, func, block)
        return func

    return wrapper
#----------------------------------------------------------------------------
def conversation_handler(
    entry_points: list[BaseHandler],
    states: dict[object, list[BaseHandler]],
    fallbacks: list[BaseHandler],
    allow_reentry: bool = False,
    per_chat: bool = True,
    per_user: bool = True,
    per_message: bool = False,
    conversation_timeout: datetime.timedelta = None,
    name: str = None,
    persistent: bool = False,
    map_to_parent: dict[object, object] = None,
    block: bool = True,
):
    def wrapper(func):
        func.metadata = ConversationHandlerMetadata(
            entry_points,
            states,
            fallbacks,
            allow_reentry,
            per_chat,
            per_user,
            per_message,
            conversation_timeout,
            name,
            persistent,
            map_to_parent,
            block,
        )
        return func

    return wrapper
#----------------------------------------------------------------------------
def error_handler():
    def wrapper(func):
        func.metadata = ErrorHandlerMetadata(func)
        return func

    return wrapper
#----------------------------------------------------------------------------
