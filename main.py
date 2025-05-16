from telebot import TeleBot
from controllers import Controller
from constants import TOKEN

bot = TeleBot(TOKEN)
controller = Controller(bot)

controller.register_handlers()

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()