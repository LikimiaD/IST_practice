import logging
from dataclasses import dataclass
from settings import TelegramBotSettings

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from cogs.callback import Callback
from cogs.admin import set_admin_list
from cogs.user import UserInterface
from cogs.map import MapInterface
from cogs.club import ClubInterface

@dataclass
class ITAMBot:
    token: str
    bot: Bot = None
    dp: Dispatcher = None

    class Form(StatesGroup):
        name = State()

    def __post_init__(self) -> None:
        set_admin_list(TelegramBotSettings.owners.value)
        logging.basicConfig(level=logging.INFO)
        self.bot = Bot(token=self.token)
        storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=storage)
        
        UserInterface().register_handlers(self.dp, self.Form)
        MapInterface().register_handlers(self.dp, self.Form)
        Callback(self.bot).register_handlers(self.dp, self.Form)
        ClubInterface().register_handlers(self.dp, self.Form)
        
    def start(self):
        executor.start_polling(self.dp, skip_updates=True)

if __name__ == "__main__":
    ITAMBot(TelegramBotSettings.telegram_token.value).start()