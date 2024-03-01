
import inspect
from types import coroutine
from telegram.ext.filters import BaseFilter
import json 

#----------------------------------------------------------------------------
class MetadataBase:
    def __str__(self) -> str:
        dict = {}
        # a = json.dumps(self.__dict__.items())
        
        for key, value in self.__dict__.items():
            if inspect.iscoroutinefunction(value) is True or inspect.isfunction(value) is True:
                dict[key] = f"{value.__module__}.{value.__qualname__}"
            else:
                dict[key] = value

        return json.dumps(dict)
#----------------------------------------------------------------------------
class CommandHandlerMetadata(MetadataBase):
    def __init__(
        self,
        command: str,
        callback: coroutine,
        filters: BaseFilter = None,
        block: bool = True,
        has_args: bool = None,
    ):
        self.command = command
        self.callback = callback
        self.filters = filters
        self.block = block
        self.has_args = has_args
#----------------------------------------------------------------------------
class MessageHandlerMetadata(MetadataBase):
    def __init__(self, filters, callback, block):
        self.filters = filters
        self.callback = callback
        self.block = block
#----------------------------------------------------------------------------
class ConversationHandlerMetadata(MetadataBase):
    def __init__(
        self,
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
    ):
        self.entry_points = entry_points
        self.states = states
        self.fallbacks = fallbacks
        self.allow_reentry = allow_reentry
        self.per_chat = per_chat
        self.per_user = per_user
        self.per_message = per_message
        self.conversation_timeout = conversation_timeout
        self.name = name
        self.persistent = persistent
        self.map_to_parent = map_to_parent
        self.block = block
#----------------------------------------------------------------------------
class ErrorHandlerMetadata(MetadataBase):
    def __init__(self, callback):
        self.callback = callback

