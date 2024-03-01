import json
import logging
from common import reflector
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)

from core.metadata import CommandHandlerMetadata, ConversationHandlerMetadata, ErrorHandlerMetadata, MessageHandlerMetadata

class TelegramHelper:
    def __init__(self):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
    #----------------------------------------------------------------------------    
    def register_command_handler(
        self,
        application: Application, parameters: CommandHandlerMetadata
    ):
        self.logger.debug(parameters)
        application.add_handler(
            CommandHandler(parameters.command, parameters.callback, parameters.filters, parameters.block)
        )
    #----------------------------------------------------------------------------------
    def register_message_handler(
        self,
        application: Application, parameters: MessageHandlerMetadata
    ):
        self.logging.debug(parameters)
        application.add_handler(
            MessageHandler(parameters.filters, parameters.callback, parameters.block)
        )
    #----------------------------------------------------------------------------------
    def register_conversation_handler(
        self,
        application: Application, parameters: ConversationHandlerMetadata
    ):
        self.logging.debug(parameters)
        application.add_handler(
            ConversationHandler(
                parameters.entry_points,
                parameters.states,
                parameters.fallbacks,
                parameters.allow_reentry,
                parameters.per_chat,
                parameters.per_user,
                parameters.per_message,
                parameters.conversation_timeout,
                parameters.name,
                parameters.persistent,
                parameters.map_to_parent,
                parameters.block,
            )
        )
    #----------------------------------------------------------------------------------
    def register_error_handler(
        self,
        application: Application, parameters: ErrorHandlerMetadata
    ):
        self.logging.debug(parameters)
        application.add_error_handler(parameters.callback)
    #----------------------------------------------------------------------------------
    def get_all_handlers(self):
        self.logger.info("Searching for handler files...")
        handlers = reflector.get_all_handlers()

        if len(handlers) == 0:
            self.logger.info("No hanlder files found.")
        else:
            self.logger.info(f"Handler files found {json.dumps(handlers)}")
        return handlers
    #----------------------------------------------------------------------------------
    def load_module(sefl, handler):
        return reflector.load_module(handler)
    #----------------------------------------------------------------------------------
    def load_modules(self, handlers):
        self.logger.info("Loading handler modules...")
        modules = []
        for handler in handlers:
            modules.append(self.load_module(handler))

        self.logger.debug(f"Loaded modules {modules}")
        self.logger.info("Handler modules loaded successfully.")
        return modules
    #----------------------------------------------------------------------------------
    def load_handler_modules(self):
        return self.load_modules(self.get_all_handlers())
    #----------------------------------------------------------------------------------
    def register_all_handlers(self, application: Application):
        self.register_handlers(application, self.get_all_handlers())
    #----------------------------------------------------------------------------------
    def register_handlers(self, application: Application, handlers: list[str]):
        for handler in handlers:
            loaded_module = self.load_module(handler)
            self.register_handlers_from_module(application, loaded_module)
    #----------------------------------------------------------------------------------
    def register_handlers_from_modules(self, application: Application, loaded_modules: list):
        for loaded_module in loaded_modules:
            self.register_handlers_from_module(application, loaded_module)
    #----------------------------------------------------------------------------------
    def register_handlers_from_module(self, application: Application, loaded_module):
        for func in reflector.get_functions(loaded_module):
            if hasattr(func, "metadata") is False:
                continue

            metadata_type = type(func.metadata)
            metadata = func.metadata
            self.logger.info("Registering handlers...")
            if metadata_type is CommandHandlerMetadata:
                self.register_command_handler(application, metadata)
            elif metadata_type is MessageHandlerMetadata:
                self.register_message_handler(application, metadata)
            elif metadata_type is ConversationHandlerMetadata:
                self.register_conversation_handler(application, metadata)
            elif metadata_type is ErrorHandlerMetadata:
                self.register_error_handler(metadata)
            else:
                raise TypeError(str(type(func)) + " is not supported.")
            self.logger.info("Handler registration successfull.")
    #----------------------------------------------------------------------------------