from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler
from credits import bot_token

bot = Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

food_time_dict = {"курица": 3, "мясо": 5, "рыба": 2, "пицца":1}

#добавил комментарий

def food_list(update, context):
    food_str = '\n'
    for food in food_time_dict:
        food_str += str(food) + '\n'
    context.bot.send_message(update.effective_chat.id, 'Я знаю, сколько времени нужно на следующие блюда:' + food_str)


def food_ready(context):
    context.bot.send_message(context.job.context, "Ваше блюдо готово!")


def set_food_timer(update, context):
    due = food_time_dict.get(context.args[0])
    context.job_queue.run_once(food_ready, due, context=update.effective_chat.id)
    context.bot.send_message(update.effective_chat.id, 'Таймер установлен')


set_food_timer_handler = CommandHandler("setfoodtimer", set_food_timer)
food_list_handler = CommandHandler("foodlist", food_list)

dispatcher.add_handler(set_food_timer_handler)
dispatcher.add_handler(food_list_handler)

updater.start_polling()
updater.idle()
