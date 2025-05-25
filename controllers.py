from telebot import types, TeleBot
from models import Model

title = {}
description = {}
question = {}
survey_id_in_work = {}
user_states = {}
user_answers = {}
survey_complete = {}

class Controller:
    def __init__(self, bot):
        self.bot: TeleBot = bot


    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data='find_survey'),
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(*buttons)

            Model.is_user_in_base(message.chat.id, 
                                  message.from_user.username)


            self.bot.send_message(message.chat.id, 
                                  f'Привет!  \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \nВыбери действие:', 
                                  reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'main_menu')
        def main_menu(callback: types.CallbackQuery):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data='find_survey'),
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'),
                types.InlineKeyboardButton('Мои опросы', callback_data='my_surveys')
            ]
            keyboard.add(*buttons)

            self.bot.edit_message_text(f'Привет!  \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \nВыбери действие:', 
                                       callback.message.chat.id, 
                                       callback.message.id, 
                                       reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'my_surveys')
        def my_surveys(callback: types.CallbackQuery):
            my_surveys_list = Model.get_my_survey_list(callback.message.chat.id)
            reply = f'Вот список твоих опросов:'
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = []

            if my_surveys_list:
                for survey in my_surveys_list:
                    buttons.append(types.InlineKeyboardButton(survey[0], callback_data=f'survey_{survey[1]}'))

            else:
                reply = 'Вы еще не создали ни одного опроса'
                buttons.append(types.InlineKeyboardButton('Создать опрос', 
                                                          callback_data='add_survey'))

            buttons.append(types.InlineKeyboardButton('Главное меню', 
                                                      callback_data='main_menu'))

            keyboard.add(*buttons)
            self.bot.edit_message_text(reply, callback.message.chat.id, callback.message.id, reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'find_survey')
        def find_survey(callback: types.CallbackQuery):
            survey_list = Model.find_not_completed_survey_list(callback.message.chat.id)
            reply = 'Вот список опросов для прохождения:'
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = []

            if survey_list:
                for survey in survey_list:
                    buttons.append(types.InlineKeyboardButton(survey[0], callback_data=f'survey_{survey[1]}'))

            else:
                reply = 'Еще нет опросов для прохождения'

            buttons.append(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

            keyboard.add(*buttons)
            self.bot.edit_message_text(reply, 
                                       callback.message.chat.id, 
                                       callback.message.id, 
                                       reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('survey_'))
        def survey(callback: types.CallbackQuery):
            survey = Model.my_survey(int(callback.data.strip('survey_')))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            if Model.is_this_my_survey(callback.message.chat.id, survey.id):
                buttons = [
                types.InlineKeyboardButton('Добавить вопрос', callback_data=f'update_survey_{survey.id}'),
                types.InlineKeyboardButton('Удалить опрос', callback_data=f'delete_survey_{survey.id}'),
                types.InlineKeyboardButton('Результаты опроса', callback_data=f'results_{survey.id}'),
                types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
                ]
                keyboard.add(*buttons)

                reply = f'ID: {survey.id} \nНазвание: {survey.title} \nОписание: {survey.description} \nПрошло человек: {survey.passed} \n \nВыберите действие:'

            else:
                buttons = [
                types.InlineKeyboardButton('Пройти опрос', callback_data=f'complete_survey_{survey.id}'),
                types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
                ]
                keyboard.add(*buttons)
                author = Model.user_info_by_survey_id(survey.id)
                if author.username == None:
                    author = 'Неизвестен'
                else:
                    author = author.username

                reply = f'ID: {survey.id} \nАвтор: {author} \nНазвание: {survey.title} \nОписание: {survey.description} \nПрошло человек: {survey.passed} \n \nВыберите действие:'

            self.bot.edit_message_text(reply, 
                                       callback.message.chat.id, 
                                       callback.message.id, 
                                       reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('delete_survey_'))
        def delete_survey(callback: types.CallbackQuery):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
            types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
            ]
            keyboard.add(*buttons)

            Model.delete_survey(int(callback.data.strip('delete_survey_')))

            self.bot.edit_message_text('Опрос удален. \nВыберите действие:', 
                                       callback.message.chat.id, 
                                       callback.message.id, 
                                       reply_markup=keyboard)

        
        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('update_survey_'))
        def update_survey(callback: types.CallbackQuery):
            global survey_id_in_work
            survey_id_in_work[callback.message.chat.id] = callback.data.strip('update_survey_')

            msg = self.bot.edit_message_text('Введите вопрос:', 
                                             callback.message.chat.id, 
                                             callback.message.id)
            self.bot.register_next_step_handler(msg, lambda m: self.get_question_title(m))


        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'add_survey')
        def add_survey(callback: types.CallbackQuery):
            msg = self.bot.edit_message_text('Введите название вашего опроса:', 
                                             callback.message.chat.id, 
                                             callback.message.id)
            self.bot.register_next_step_handler(msg, lambda m: self.title_text(m))


        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('results_'))
        def get_results(callback: types.CallbackQuery):
            msg = ''
            for question, answers in Model.get_results(callback.data.strip('results_')).items():
                if not question:
                    msg = 'Опрос пуст.\n'
                else:
                    msg += f'{question}:\n'
                    for answ, count in answers.items():
                        msg += f'   {answ}: {count}\n'
            msg += 'Выберите действие:'
            
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))
            self.bot.edit_message_text(msg, 
                                       callback.message.chat.id, 
                                       callback.message.id, 
                                       reply_markup=keyboard)


        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('complete_survey_'))
        def complete_survey(callback: types.CallbackQuery):
            survey_complete[callback.message.chat.id] = callback.data.strip('complete_survey_')

            survey_id = survey_complete[callback.message.chat.id]

            questions = Model.get_questions(survey_id)

            user_states[callback.message.chat.id] = iter(questions.items())
            user_answers[callback.message.chat.id] = {}

            send_next_question(callback, 
                               survey_id)    


        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('answer_'))
        def handle_answer(callback: types.CallbackQuery):
            survey_id = survey_complete[callback.message.chat.id]

            selected_answer = callback.data.strip('answer_')
    
            current_question = callback.message.text
    
            user_answers[callback.message.chat.id][current_question] = selected_answer
    
            send_next_question(callback, 
                               survey_id)

        
        def send_next_question(callback, 
                               survey_id):
                try:
                    question, answers = next(user_states[callback.message.chat.id])
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
        
                    for answer in answers:
                        keyboard.add(types.InlineKeyboardButton(text=answer, callback_data=f'answer_{answer}'))

                        self.bot.edit_message_text(question, 
                                                   callback.message.chat.id, 
                                                   callback.message.id, 
                                                   reply_markup=keyboard)
    
                except StopIteration:
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    keyboard.add(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))
                    self.bot.edit_message_text("Опрос завершен!", 
                                               callback.message.chat.id, 
                                               callback.message.id, 
                                               reply_markup=keyboard)

                    Model.write_answers(survey_id, user_answers[callback.message.chat.id], callback.message.chat.id)

                    del user_states[callback.message.chat.id]
                    del user_answers[callback.message.chat.id]


        
    def title_text(self, message):
        global title
        title[message.chat.id] = message.text
        msg = self.bot.send_message(message.chat.id, 
                                    'Введите описание вашего опроса:')
        self.bot.register_next_step_handler(msg, 
                                            lambda m: self.description_text(m))


    def description_text(self, message):
        global description
        description[message.chat.id] = message.text

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Создать опрос', callback_data='add_survey'), 
            types.InlineKeyboardButton('Главное меню', callback_data='main_menu')]
        keyboard.add(*buttons)

        Model.add_survey(title[message.chat.id], description[message.chat.id], message.chat.id)
        del title[message.chat.id]
        del description[message.chat.id]
        self.bot.send_message(message.chat.id, 
                              'Опрос добавлен! \nВыберите действие:', 
                              reply_markup=keyboard)

    
    def get_question_title(self, message):
        global question
        question[message.chat.id] = message.text

        msg = self.bot.send_message(message.chat.id, 
                                    'Введите варианты ответа (каждый на новой строке):')
        self.bot.register_next_step_handler(msg, lambda m: self.get_answers(m))


    def get_answers(self, message):
        global survey_id_in_work
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Добавить вопрос', callback_data=f'update_survey_{survey_id_in_work[message.chat.id]}'),
            types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
            ]
        keyboard.add(*buttons)
        
        answer = message.text

        Model.update_survey(survey_id_in_work[message.chat.id], question[message.chat.id], answer)
        del survey_id_in_work[message.chat.id]
        self.bot.send_message(message.chat.id, 
                              'Вопрос добавлен! \nВыберите действие:', 
                              reply_markup=keyboard)