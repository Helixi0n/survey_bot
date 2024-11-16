import telebot, json

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)


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


@bot.callback_query_handler(func=lambda callback: callback == 'back')
def handle_start(callback):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_survey_choice = telebot.types.InlineKeyboardButton('Пройти опрос', callback_data='1')
    btn_completed_survey = telebot.types.InlineKeyboardButton('Пройденные опросы', callback_data='2')
    btn_make_survey = telebot.types.InlineKeyboardButton('Создать свой опрос', callback_data='3')
    keyboard.add(
        btn_survey_choice,
        btn_completed_survey,
        btn_make_survey)
    bot.edit_message_text('Привет! Я - бот-опросник. \nЗдесь регулярно будут появляться опросы на разные темы, которые ты можешь пройти. Не хочешь пройти мой опрос? \nЕсли что-то не понятно - нажми /help',
        callback.message.chat.id,
        callback.message.id,
        reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(
        message.chat.id,
        'Вот список моих команд: \n/start - запуск бота \n/help - список команд \n')


def create_dict(**qwargs):
    d = {k: v for k, v in qwargs.items()}
    return d


@bot.callback_query_handler(func=lambda callback: callback.data == '1')
def survey_choice(callback):
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for elem in json.load(open(f'Polls/survey.json', 'rb')).keys():
        keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    keyboard.add(telebot.types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
    if len(json.load(open(f'Polls/survey.json', 'rb')).keys()) == 0:
        with open(f'Users/{callback.message.chat.id}.json', 'w', encoding="utf-8") as f:
            data = create_dict()
            json.dump(data, file=f)

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
    keyboard.add(telebot.types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
    bot.edit_message_text(
        f'Вот список опросов, которые ты прошел: \n{completed}',
        callback.message.chat.id,
        callback.message.id,
        reply_markup=keyboard
    )


print('Сервер запущен.')

bot.polling(
    non_stop=True,
    interval=1
)