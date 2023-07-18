from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from localization import StartDialogue
import json
import random
from dataclasses import dataclass

@dataclass
class QuizInterface:
    def load_questions_from_json(self):
        with open('cogs/quiz_data.json', 'r', encoding='utf-8') as file:
            questions = json.load(file)
        return questions
    
    async def quizinfo(self, message: types.Message):
        await message.answer(text=StartDialogue.quizstart.value)

        button_start = InlineKeyboardButton("LetsGo", callback_data="start")
        button_back = InlineKeyboardButton("Back", callback_data="back")

        keyboard = InlineKeyboardMarkup().add(button_start, button_back)
        await message.answer("Выберите действие:", reply_markup=keyboard)
        

    async def handle_start_command(self, query: CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            if "current_question" not in data:
                # Выбираем случайный вопрос и ответы из списка
                random_question = random.choice(self.questions)
                question_text = random_question['question']
                answers = random_question['answers']
                correct_answer = random.choice(answers)

                # Сохраняем данные в контексте пользователя
                await state.update_data({
                    'current_question': question_text,
                    'answers': answers,
                    'correct_answer': correct_answer
                })

                # Создаем кнопки ответов
                buttons = [InlineKeyboardButton(answer, callback_data=answer) for answer in answers]
                keyboard = InlineKeyboardMarkup().add(*buttons)

                await query.message.edit_text(question_text, reply_markup=keyboard)




    async def handle_user_answer(self, query: CallbackQuery, state: FSMContext):
        user_answer = query.data
        async with state.proxy() as data:
            if "current_question" in data:
                current_question = data['current_question']
                correct_answer = None
                for question in self.questions:
                    if question['question'] == current_question:
                        correct_answer = question['correct_answer']
                        break

                if user_answer == correct_answer:
                    await query.answer("Правильный ответ!")
                else:
                    await query.answer("Неправильный ответ!")

                if user_answer == "Выход":
                    await query.message.edit_text("Вы вышли из викторины.")
                    await state.finish()
                else:
                    # Выбор нового случайного вопроса
                    random_question = random.choice(self.questions)
                    question_text = random_question['question']
                    answers = random_question['answers']
                    correct_answer = random.choice(answers)

                    # Обновление данных в состоянии пользователя
                    data['current_question'] = question_text
                    data['answers'] = answers
                    data['correct_answer'] = correct_answer

                    # Создание новых кнопок ответов
                    buttons = [InlineKeyboardButton(answer, callback_data=answer) for answer in answers]
                    buttons.append(InlineKeyboardButton("Выход", callback_data="Выход"))
                    keyboard = InlineKeyboardMarkup().add(*buttons)

                    # Обновление сообщения с новым вопросом и кнопками
                    await query.message.edit_text(question_text, reply_markup=keyboard)




    def register_handlers(self, dp: Dispatcher, state: object):
        self.state = state
        self.questions = self.load_questions_from_json()

        dp.register_message_handler(self.quizinfo, commands=['quiz'])
        dp.register_callback_query_handler(self.handle_start_command, lambda query: query.data == "start")
        dp.register_callback_query_handler(self.handle_user_answer)