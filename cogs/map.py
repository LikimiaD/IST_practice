from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from localization import Map

from dataclasses import dataclass
from enum import Enum

@dataclass
class MapInterface:
    # ...

    async def location_keyboard(self, message: types.Message):
        keyboard = InlineKeyboardMarkup(row_width=5)
        for location in University:
            button = InlineKeyboardButton(location.value[0], callback_data=location.name)
            keyboard.insert(button)

        await message.reply(Map.start.value, reply_markup=keyboard)
        
    async def send_map(self, message: types.Message):
        photo_url = 'https://media.discordapp.net/attachments/1130170679124312067/1130548002419900520/image.png'
        
        await message.answer_photo(photo=photo_url, caption=Map.map.value)
        
    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state
        dp.register_message_handler(self.location_keyboard, commands=['location'])
        dp.register_message_handler(self.send_map, commands=['map'])

class University(Enum):
    building_main = ("Главное", (55.728606736915005, 37.60912654595173))
    building_b = ("Корпус Б", (55.728499733989366, 37.60920960561965))
    building_k = ("Корпус К", (55.7297971402562, 37.61015731836858))
    building_varshava = ("Варшава", (55.72865230825865, 37.61077469091155))
    building_a = ("Корпус А", (55.727071431714435, 37.607977752355694))
    building_g = ("Корпус Г", (55.72706245053072, 37.607116532770085))
    building_d = ("Корпус Д", (55.72751804968044, 37.60652992954495))
    building_v = ("Корпус В", (55.72791831164964, 37.60749820698741))
    building_l = ("Корпус Л", (55.72774159272158, 37.60631267062425))
    building_gym = ("Спортзал", (55.726844391967774, 37.605793658631384))