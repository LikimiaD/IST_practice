from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum
import random

from localization import StartDialogue, Quest
from .keyboard import Keyboard
from dataclasses import dataclass
from .jsonfile import DataHandler


@dataclass
class UserInterface:
    bot: Bot
    state: object = None
    board: Keyboard = None
    db: DataHandler = DataHandler()
    direction_keyboard: InlineKeyboardMarkup = None

    def __post_init__(self):
        self.board = Keyboard()
        self.direction_keyboard = InlineKeyboardMarkup(row_width=1)
        for location in Directions:
            button = InlineKeyboardButton(location.value, callback_data=location.name)
            self.direction_keyboard.insert(button)

    async def welcome(self, message: types.Message, state: FSMContext):
        self.db = DataHandler()
        self.db.create_record(id=message.from_user.id)
        self.db.save_data()
        await state.set_state(self.state.name)
        print(self.state.name)
        await message.answer(text=StartDialogue.welcome.value)

    async def test_key(self, message: types.Message):
        await message.answer(text="Loaded keyboard", reply_markup=self.board.user_keyboard)

    async def user_profile(self, message: types.Message):
        record = self.db.search_record(message.from_user.id)
        template = """User Information:\n
                      ID: {0}\n
                      Name: {1}\n
                      Preferred Department: {2}\n
                      Experience: {3}\n
                      """.format(record["id"],
                                 record["name"],
                                 *record["directions"],
                                 record["score"])
        await message.answer(text=template)

    async def echo(self, message: types.Message, state: FSMContext):
        print(message.text, message.from_user.id)
        record = self.db.search_record(message.from_user.id)
        if record:
            if record["name"] is None:
                self.db = DataHandler()
                self.db.create_record(id=message.from_user.id, name=message.text)
                self.db.save_data()
                await message.answer(StartDialogue.after_name.value, reply_markup=self.direction_keyboard)
                await state.finish()
            elif record["quest"] is not None:
                print("RECORD DETECTED")
                id_quest = record["quest"]
                id_status = record["quest_status"]
                if (id_status == 1):
                    print(str(eval(f"Quest.quest{id_quest}_correct.value")).lower())
                    if(message.text.lower() == str(eval(f"Quest.quest{id_quest}_correct.value")).lower()):
                        print(eval(f"Quest.quest{id_quest}_accept.value"))
                        await message.answer(eval(f"Quest.quest{id_quest}_accept.value"))
                        self.db = DataHandler()
                        self.db.create_record(
                            id=message.from_user.id,
                            quest_status=0
                        )
                        await state.finish()
                    else:
                        vars: int = eval(f"Quest.quest{id_quest}_wrong_vars.value")
                        choice = random.randint(1,vars)
                        await message.answer(eval(f"Quest.quest{id_quest}_wrong{choice}.value"))
                        
    async def take_quest(self, message: types.Message, state: FSMContext):
        self.db = DataHandler()
        print(self.state.name)
        record = self.db.export_record(id=message.from_user.id)
        if record:
            if record["quest_status"] != 1 and record["quest"] < 3:
                self.db.create_record(id=message.from_user.id, quest=1 if record["quest"] is None else record["quest"] + 1, quest_status=1)
                self.db.save_data()
                print(self.state.name)
            else:
                if record["quest"] >= 3 and record["quest_status"] == 0:
                    await message.answer(Quest.quest_empty.value)
                else:
                    id_quest = record["quest"]
                    await message.answer(f"Ты еще не закончил текущий квест, давай я тебе напомню его:\n\n{eval(f'Quest.quest{id_quest}_text.value')}")
            if (record["quest"] < 3):
                match record["quest"]:
                    case 1:
                        await message.answer(text=Quest.quest1_text.value.format(record["name"]))
                    case 2:
                        await message.answer(text=Quest.quest2_text.value)
                    case 3:
                        await message.answer(text=Quest.quest3_text.value)
                await state.set_state(self.state.name)

    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state
        dp.register_message_handler(self.welcome, commands=['start', 'help'])
        dp.register_message_handler(self.test_key, commands=['test'])
        dp.register_message_handler(self.echo, state=self.state.name)
        dp.register_message_handler(self.take_quest, lambda msg: msg.text.lower() == 'взять квест')


class Directions(Enum):
    direction_loshki = "Department of Economics and Management"
    direction_gigachad = "Department of Computer Science"
    direction_minecraft = "Mining Institute"
    direction_shithappens = "Institute of Technologies"
    direction_cyberminecraft = "Institute of New Materials"