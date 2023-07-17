from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from localization import Club

class ClubInterface:
    def __init__(self):
        self.club_keyboard = None

    def post_init(self):
        self.club_keyboard = InlineKeyboardMarkup(row_width=1)
        self.club_keyboard.add(
            InlineKeyboardButton("CTF", callback_data="club_ctf"),
            InlineKeyboardButton("Дизайн", callback_data="club_design"),
            InlineKeyboardButton("Хакатон", callback_data="club_hackaton"),
            InlineKeyboardButton("GameDev", callback_data="club_gamedev"),
            InlineKeyboardButton("Robotics", callback_data="club_robotics"),
        )

    async def club_message(self, message: types.Message):
        await message.reply(Club.select.value, reply_markup=self.club_keyboard)

    def register_handlers(self, dp: Dispatcher, state: object):
        self.post_init()
        self.state = state
        dp.register_message_handler(self.club_message, lambda msg: msg.text.lower() == 'клубы')