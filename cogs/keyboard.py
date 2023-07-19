from aiogram import types, Bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboard():
    user_keyboard: ReplyKeyboardMarkup = None

    def __init__(self):
        user_lst: list = [KeyboardButton("Взять квест", callback_data="Взять квест"),
                    KeyboardButton("Клубы", callback_data="Клубы"),
                    KeyboardButton("Карта НИТУ МИСИС", callback_data="Карта НИТУ МИСИС"),
                    KeyboardButton("Найти корпус", callback_data="Найти корпус"),
                    KeyboardButton("Профиль", callback_data="Профиль"),]
        
        self.user_keyboard = ReplyKeyboardMarkup(row_width=3)
        for button in user_lst:
            self.user_keyboard.add(button)