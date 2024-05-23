import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = "6745939952:AAFd0OSxtOG9jR-wImr7v9U9VuJNRHMM--Y"

# Pomodoro timer settings (in seconds)
POMODORO_DURATION = 1 * 60  # 25 minutes
SHORT_BREAK_DURATION = 1 * 60  # 5 minutes
LONG_BREAK_DURATION = 1 * 60  # 15 minutes
POMODORO_CYCLES_BEFORE_LONG_BREAK = 4  # After 4 pomodoros, take a long break


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Pomodoro Bot! Use /pomodoro to start your Pomodoro session.")


def start_pomodoro(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.user_data['pomodoro_cycles'] = 0
    update.message.reply_text("Pomodoro started! Focus for 25 minutes.")
    context.job_queue.run_once(pomodoro_timer, POMODORO_DURATION,
                               context={'chat_id': chat_id, 'user_data': context.user_data})


def pomodoro_timer(context: CallbackContext):
    job = context.job
    chat_id = job.context['chat_id']
    user_data = job.context['user_data']
    pomodoro_cycles = user_data['pomodoro_cycles'] + 1
    user_data['pomodoro_cycles'] = pomodoro_cycles

    context.bot.send_message(chat_id=chat_id, text="Time's up! Take a short 5-minute break.")

    if pomodoro_cycles < POMODORO_CYCLES_BEFORE_LONG_BREAK:
        context.job_queue.run_once(short_break_timer, SHORT_BREAK_DURATION,
                                   context={'chat_id': chat_id, 'user_data': user_data})
    else:
        context.job_queue.run_once(long_break_timer, SHORT_BREAK_DURATION,
                                   context={'chat_id': chat_id, 'user_data': user_data})


def short_break_timer(context: CallbackContext):
    job = context.job
    chat_id = job.context['chat_id']
    user_data = job.context['user_data']
    pomodoro_cycles = user_data['pomodoro_cycles']

    context.bot.send_message(chat_id=chat_id, text="Short break over! Time for another Pomodoro session.")
    context.job_queue.run_once(pomodoro_timer, POMODORO_DURATION, context={'chat_id': chat_id, 'user_data': user_data})


def long_break_timer(context: CallbackContext):
    job = context.job
    chat_id = job.context['chat_id']
    user_data = job.context['user_data']

    context.bot.send_message(chat_id=chat_id, text="Long break started! Take a 15-minute break.")
    context.job_queue.run_once(start_pomodoro_job, LONG_BREAK_DURATION,
                               context={'chat_id': chat_id, 'user_data': user_data})


def start_pomodoro_job(context: CallbackContext):
    job = context.job
    chat_id = job.context['chat_id']
    user_data = job.context['user_data']
    user_data['pomodoro_cycles'] = 0

    context.bot.send_message(chat_id=chat_id, text="Pomodoro started! Focus for 25 minutes.")
    context.job_queue.run_once(pomodoro_timer, POMODORO_DURATION, context={'chat_id': chat_id, 'user_data': user_data})


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pomodoro", start_pomodoro))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
