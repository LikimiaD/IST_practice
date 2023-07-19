from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from localization import StartDialogue, Quest
from .keyboard import Keyboard
from dataclasses import dataclass
from .jsonfile import DataHandler
from enum import Enum
import random

@dataclass
class UserInterface:
    bot: Bot
    state: object = None #FIX HERE
    board: Keyboard = None
    db: DataHandler = DataHandler()
    direction_keyboard: InlineKeyboardMarkup = None
    
    def __post_init__(self):
        self.board = Keyboard()
        self.direction_keyboard = InlineKeyboardMarkup(row_width=1)
        for location in Directions:
            button = InlineKeyboardButton(location.value, callback_data=location.name)
            self.direction_keyboard.insert(button)
        
    async def welcome(self, message: types.Message): 
        self.db.create_record(id=message.from_user.id)
        self.db.save_data()
        #self.state.name.set() #FIX HERE
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
            print(record)
            if record["name"] is None:
                print("TEST")
                self.db.create_record(id=message.from_user.id, name=message.text)
                self.db.save_data()
                await message.answer(StartDialogue.after_name.value, reply_markup=self.direction_keyboard)
                #await state.finish() #FIX HERE
            elif record["name"] is not None and record["directions"] is not None:
                id_quest = record["quest"] # need add column
                id_status = record["quest_status"] # need add column
                if (id_status == 0): #need start
                     message.answer(text=eval(eval(f"Quest.quest{0}_text.format(record[\"nane\"])".format(id_quest))))
                else:
                    user_answer = message.text
                    if (message == eval(f"Quest.quest{0}_correct".format(id_quest))):
                        message.answer(text=eval(f"Quest.quest{0}_accept".format(id_quest)))
                        self.db.create_record(id=message.from_user.id, quest=..., quest_status=..., score=...)
                    else:
                        wrong_vars = eval(f"Quest.quest{0}_wrong_vars".format(id_quest))
                        rnd_var = random.randint(1, wrong_vars)
                        message.answer(text=eval(f"Quest.quest{0}_wrong{1}".format(id_quest, rnd_var)))
        
    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state #FIX HERE
        dp.register_message_handler(self.welcome, commands=['start', 'help'])
        dp.register_message_handler(self.test_key, commands=['test'])
        #dp.register_message_handler(self.echo, state=self.state.name) FIX HERE
        dp.register_message_handler(self.echo)
        
class Directions(Enum):
    direction_loshki = "Department of Economics and Management"
    direction_gigachad = "Department of Computer Science"
    direction_minecraft = "Mining Institute"
    direction_shithappens = "Institute of Technologies"
    direction_cyberminecraft = "Institute of New Materials"