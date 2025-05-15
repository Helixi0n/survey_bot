from telebot import types
from models import Model

title = ''
description = ''
question = ''
survey_id_in_work = 0

class Controller:
    def __init__(self, bot):
        self.bot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data='complete_survey'),
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(*buttons)

            self.bot.send_message(message.chat.id, f'Привет! 😀 \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \nВыбери действие:', reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'main_menu')
        def main_menu(callback):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data='complete_survey'),
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(*buttons)

            self.bot.edit_message_text(f'Привет! 😀 \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \nВыбери действие:', callback.message.chat.id, callback.message.id, reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'my_surveys')
        def my_surveys(callback):
            my_surveys_list = Model.get_my_survey_list(callback.message.chat.id)
            reply = f'Вот список твоих опросов:'
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = []

            if my_surveys_list:
                for survey in my_surveys_list:
                    buttons.append(types.InlineKeyboardButton(survey[0], callback_data=f'survey_{survey[1]}'))

            else:
                reply = 'Вы еще не создали ни одного опроса'
                buttons.append(types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'))

            buttons.append(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

            keyboard.add(*buttons)
            self.bot.edit_message_text(reply, callback.message.chat.id, callback.message.id, reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('survey_'))
        def my_survey(callback):
            survey = Model.my_survey(int(callback.data[7:]))
            reply = f'ID: {survey.id} \nНазвание: {survey.title} \nОписание: {survey.description} \nПрошло человек: {survey.passed} \n \nВыберите действие:'
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
            types.InlineKeyboardButton('Изменить опрос', callback_data=f'update_survey_{survey.id}'),
            types.InlineKeyboardButton('Удалить опрос', callback_data=f'delete_survey_{survey.id}'),
            types.InlineKeyboardButton('Результаты опроса', callback_data=f'results_{survey.id}'),
            types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
            ]
            keyboard.add(*buttons)

            self.bot.edit_message_text(reply, callback.message.chat.id, callback.message.id, reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('delete_survey_'))
        def delete_survey(callback):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
            types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
            ]
            keyboard.add(*buttons)

            Model.delete_survey(int(callback.data[14:]))

            self.bot.edit_message_text('Опрос удален. \nВыберите действие:', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

        
        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('update_survey_'))
        def update_survey(callback):
            msg = self.bot.edit_message_text('Введите вопрос:')
            self.bot.register_next_step_handler(msg, lambda m: self.get_question_title(m))

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'add_survey')
        def add_survey(callback):
            msg = self.bot.edit_message_text('Введите название вашего опроса:', callback.message.chat.id, callback.message.id)
            self.bot.register_next_step_handler(msg, lambda m: self.title_text(m))
            

    def title_text(self, message):
        global title
        title = message.text
        msg = self.bot.send_message(message.chat.id, 'Введите описание вашего опроса (необязательно):')
        self.bot.register_next_step_handler(msg, lambda m: self.description_text(m))


    def description_text(self, message):
        global description
        description = message.text

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'), 
                    types.InlineKeyboardButton('Главное меню', callback_data='main_menu')]
        keyboard.add(*buttons)

        Model.add_survey(title=title, description=description, user_id=message.chat.id)
        self.bot.send_message(message.chat.id, 'Опрос добавлен! \nВыберите действие:', reply_markup=keyboard)

    
    def get_question_title(self, message):
        global question
        question = message.text

        msg = self.bot.send_message(message.chat.id, 'Введите варианты ответа (каждый на новой строке):')
        self.bot.register_next_step_handler(msg, lambda m: self.get_answers)

    def get_answers(self, message):
        answers = message.split('\n')

        