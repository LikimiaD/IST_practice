from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from localization import StartDialogue
from .keyboard import Keyboard
from dataclasses import dataclass

@dataclass
class UserInterface:
    board: Keyboard = None;
    def __post_init__(self):
        self.board = Keyboard()
        
    async def welcome(self, message: types.Message):
        await message.answer(text=StartDialogue.welcome.value)
    
    async def test_key(self, message: types.Message):
        await message.answer(text="Загрузил клаву", reply_markup=self.board.user_keyboard)
        
    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state
        
        dp.register_message_handler(self.welcome, commands=['start', 'help'])
        dp.register_message_handler(self.test_key, commands=['test'])