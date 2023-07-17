from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from localization import StartDialogue

from dataclasses import dataclass

@dataclass
class UserInterface:
    # ...
    # def __post_init__(self):
    #     ...
    
    async def welcome(self, message: types.Message):
        await message.answer(text=StartDialogue.welcome.value)
        
    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state
        
        dp.register_message_handler(self.welcome, commands=['start', 'help'])