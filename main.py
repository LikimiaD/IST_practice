import logging
from dataclasses import dataclass
from settings import TelegramBotSettings

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# from cogs.user import User
# from cogs.schedule import Schedule
# from cogs.owner import Owner
from cogs.callback import Callback
# from cogs.rights import set_admin_list

# from data.mongo import MongoDataBase
from cogs.admin import set_admin_list
from cogs.user import UserInterface
from cogs.map import MapInterface
from cogs.quiz import QuizInterface

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

        # schedule = Schedule()
        # schedule.register_handlers(self.dp)

        # Owner(self.bot).register_handlers(self.dp)
        # User().register_handlers(self.dp, self.Form)
        
        #класс с квизом реализую его отдельно от всех
        QuizInterface().register_handlers(self.dp, self.Form)
        
        # классы для взаимодействия с пользователем
        # UserInterface().register_handlers(self.dp, self.Form)
        # MapInterface().register_handlers(self.dp, self.Form)
        # Callback(self.bot).register_handlers(self.dp, self.Form)
        
    def start(self):
        executor.start_polling(self.dp, skip_updates=True)

if __name__ == "__main__":
    ITAMBot(TelegramBotSettings.telegram_token.value).start()