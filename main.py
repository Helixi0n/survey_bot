import telebot, json
from survey_bot.constants import TOKEN

bot = telebot.TeleBot(TOKEN)
keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
btn_back = telebot.types.InlineKeyboardButton("Вернуться назад", callback_data="back")


@bot.message_handler(commands=['start'])
def handle_start(message):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_survey_choice = telebot.types.InlineKeyboardButton('Пройти опрос', callback_data='1')
    btn_completed_survey = telebot.types.InlineKeyboardButton('Пройденные опросы', callback_data='2')
    btn_make_survey = telebot.types.InlineKeyboardButton('Создать свой опрос', callback_data='3')
    keyboard.add(
        btn_survey_choice,
        btn_completed_survey,
        btn_make_survey)
    bot.send_message(
        message.chat.id,
        'Привет! Я - бот-опросник. \nЗдесь регулярно будут появляться опросы на разные темы, которые ты можешь пройти. Не хочешь пройти мой опрос? \nЕсли что-то не понятно - нажми /help',
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'back')
def main_menu(callback):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_survey_choice = telebot.types.InlineKeyboardButton('Пройти опрос', callback_data='1')
    btn_completed_survey = telebot.types.InlineKeyboardButton('Пройденные опросы', callback_data='2')
    btn_make_survey = telebot.types.InlineKeyboardButton('Создать свой опрос', callback_data='3')
    keyboard.add(
        btn_survey_choice,
        btn_completed_survey,
        btn_make_survey)
    bot.edit_message_text(
        'Выбери действие:',
        callback.message.chat.id,
        callback.message.id,
        reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def handle_help(message):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn_back)
    bot.send_message(
        message.chat.id,
        'Вот список моих команд: \n/start - запуск бота \n/help - список команд \n',
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == '1')
def survey_choice(callback):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    with open(f'Users/{callback.message.chat.id}.json', 'w', encoding="utf-8") as file:
        json.dump({}, file)
    for elem in json.load(open(f'survey.json', 'rb')).keys():
        keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    keyboard.add(btn_back)
    bot.edit_message_text(
        'Выбери интересующий тебя опрос:',
        callback.message.chat.id,
        callback.message.id,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda callback: callback.data == '2')
def completed_survey(callback):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    completed = ''
    for elem in json.load(open(f'Users/{callback.message.chat.id}.json', 'rb')).keys():
        completed += f'{elem} \n'
    keyboard.add(btn_back)
    bot.edit_message_text(
        f'Вот список опросов, которые ты прошел: \n{completed}',
        callback.message.chat.id,
        callback.message.id,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda callback: callback in json.load(open(f'survey.json', 'rb')).keys())
def survey(callback):
    srv = json.load(open(f'survey.json', 'rb'))[callback]



print('Сервер запущен.')

bot.polling(
    non_stop=True,
    interval=1
)