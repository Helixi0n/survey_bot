import telebot, json

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_survey = telebot.types.KeyboardButton('Пройти опрос')
btn_completed_survey = telebot.types.KeyboardButton('Пройденные опросы')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     'Привет! Я - бот-опросник. \nЗдесь регулярно будут появляться опросы на разные темы, которые ты можешь пройти. Не хочешь пройти мой опрос? \nЕсли что-то не понятно - нажми /help',
                     reply_markup=keyboard)
    keyboard.add(btn_survey, btn_completed_survey)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот список моих команд: \n/start - запуск бота \n/help - список команд \n')


def create_dict(**qwargs):
    d = {k: v for k, v in qwargs.items()}
    return d


@bot.message_handler(regexp='Пройти опрос')
def survey_choose(message):
    data = create_dict()
    with open(f'{message.chat.id}.json', 'w', encoding="utf-8") as f:
        json.dump(data, f)
    bot.send_message(message.chat.id, 'Выбери интересующий тебя опрос: ')


@bot.message_handler(regexp='Пройденные опросы')
def completed_survey(message):
    with open(f'{message.chat.id}.json', 'r') as f:
        data = json.load(f)


print('Сервер запущен.')

bot.polling(
    non_stop=True,
    interval=1
)