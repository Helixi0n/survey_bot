from telebot import types
from models import Model

class Controller:
    def __init__(self, bot):
        self.bot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            buttons = [
                types.InlineKeyboardButton('Создать опрос', callback_data='add_survey')
            ]
            self.bot.send_message(message.chat.id, f'Привет! 😀 \nЭто бот-опросник. Здесь ты можешь создавать свои опросы на разные темы и проходить опросы других людей. \n Выбери действие:')