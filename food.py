from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from credits import bot_token

bot = Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

def get_data_from_file(day):
    f = open(day, "r", encoding = "utf8")
    data = f.read()
    f.close()
    return data

def write_to_wall(update, context):
    wall = open('wall.txt', 'a', encoding="utf8")
    result = ''
    for arg in context.args:
        result += arg + ' '
    wall.write(str(update.message.from_user['username']) + ": " + result + '\n')
    wall.close()

def show_wall(update, context):
    context.bot.send_message(update.effective_chat.id, get_data_from_file("wall.txt"))

def start(update, context):
    context.bot.send_message(update.effective_chat.id, "Это бот для расписания! Ничего не забывай!")
    
def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Команды:\n /start\n /info\n /get_day")
    
def get_day(update, context):
    keyboard = [[InlineKeyboardButton("Понедельник", callback_data='1'), InlineKeyboardButton("Вторник", callback_data='2')],
                [InlineKeyboardButton("Среда", callback_data='3'), InlineKeyboardButton("Четверг", callback_data='4')],
                [InlineKeyboardButton("Пятница", callback_data='5')]]
    update.message.reply_text('Выбери день недели', reply_markup=InlineKeyboardMarkup(keyboard))
    


def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "1":
        context.bot.send_message(update.effective_chat.id, get_data_from_file("mon.txt"))
    elif query.data == "2":
        context.bot.send_message(update.effective_chat.id, get_data_from_file("tue.txt"))
    elif query.data == "3":
        context.bot.send_message(update.effective_chat.id, get_data_from_file("wed.txt"))
    
start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
get_day_handler = CommandHandler('get_day', get_day)
button_handler= CallbackQueryHandler(button)
write_to_wall_handler = CommandHandler('writewall', write_to_wall)
show_wall_handler = CommandHandler('showwall', show_wall)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(get_day_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(write_to_wall_handler)
dispatcher.add_handler(show_wall_handler)

updater.start_polling()
updater.idle()