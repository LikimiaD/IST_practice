import re

from aiogram import Dispatcher, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from dataclasses import dataclass
from datetime import datetime, timedelta
from .map import University
from localization import Map
    
@dataclass
class Callback:
    bot: Bot
    state: object = None

    async def button_callback_handler(self, query: CallbackQuery):
        """Обработка callback со всей структуры бота

        Args:
            query (CallbackQuery): _description_
        """
        func_name,data = query.data.split("_")
        if (func_name == "building"):
            await self.location_chosen(query)
            
    async def location_chosen(self, query: CallbackQuery):
        location = query.data
        latitude, longitude = University[location].value[1]
        await self.bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=f"{Map.selected.value}{University[location].value[0]}"
        )
        await self.bot.send_location(
            chat_id=query.message.chat.id,
            latitude=latitude,
            longitude=longitude
        )
            
    def register_handlers(self, dp: Dispatcher, state: object):
        """Регистрация callback'a в Dispatcher'e

        Args:
            dp (Dispatcher): _description_
            state (object): _description_
        """
        self.state = state
        dp.register_callback_query_handler(self.button_callback_handler)
        