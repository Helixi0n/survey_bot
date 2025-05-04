from telebot import types
from models import Model

keyboard = types.InlineKeyboardMarkup(row_width=1)
title = ''
description = ''

class Controller:
    def __init__(self, bot):
        self.bot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data='complete_survey'),
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(buttons)

            self.bot.send_message(message.chat.id, f'Привет! 😀 \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \n Выбери действие:', reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'main_menu')
        def main_menu(callback):
            buttons = [
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Пройти опрос', callback_data='complete_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(buttons)

            self.bot.edit_message_text(callback.message.chat.id, callback.message.id, f'Привет! 😀 \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \n Выбери действие:', reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'my_surveys')
        def my_surveys(callback):
            my_surveys_list = Model.get_my_survey_list(callback.message.chat.id)
            reply = f'Вот список твоих опросов:\n'
            buttons = []

            if my_surveys_list:
                for survey in my_surveys_list:
                    reply += f'{survey[0]}, ID: {survey[1]}\n'
                    buttons.append(types.InlineKeyboardButton(survey[0], callback_data=survey[1]))

            else:
                reply = 'Вы еще не создали ни одного опроса'
                buttons.append(types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'))
                buttons.append(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

            keyboard.add(buttons)
            self.bot.edit_message_text(reply, callback.message.chat.id, callback.message.id, reply_markup=keyboard)

            @self.bot.callback.query.handler()
            def my_survey(callback):
                survey = Model.my_survey(int(callback.text))
                reply = f'''ID: {survey.id}\n
                            Название: {survey.title}\n
                            Описание: {survey.description}\n
                            Прошло человек: {survey.passed}\n
                            \n
                            Выберите действие:
                            '''
                buttons = [
                types.InlineKeyboardButton('Изменить опрос', callback_data='update_survey'),
                types.InlineKeyboardButton('Удалить опрос', callback_data='delete_survey'),
                types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
                ]
                keyboard.add(buttons)

                self.bot.edit_message_text(reply, callback.message.chat.id, callback.message.id, reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'add_survey')
        def add_survey(callback):
            global title, description
            title = ''
            description = ''
            self.bot.edit_message_text('Введите название вашего опроса:', callback.message.chat.id, callback.message.id)

            @self.bot.message_handler()
            def title_text(message):
                global title
                title = message.text

                self.bot.edit_message_text('Введите описание опроса (необязательно):', callback.message.chat.id, callback.message.id)

                @self.bot.message_handler()
                def description_text(message):
                    global description
                    description = message.text

                    buttons = [types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'), 
                               types.InlineKeyboardButton('Главное меню', callback_data='main_menu')]
                    keyboard.add(buttons)

                    Model.add_survey(title=title, description=description, user_id=message.chat.id)
                    self.bot.edit_message_text('Опрос добавлен!:', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

        