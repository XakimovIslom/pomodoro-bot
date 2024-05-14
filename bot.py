import time
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)


SHORT_BREAK_INTERVAL = 1 * 60  # 5 minutes in seconds
LONG_BREAK_INTERVAL = 1 * 60  # 15 minutes in seconds


# Global variables
time_intervals = {"/15": 1 * 60, "/20": 1 * 60, "/25": 25 * 60, "/30": 30 * 60}
session_count = 0
in_break = False


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Pomodoro Timer! Send /start_pomodoro to begin a session."
    )


# Function to start the Pomodoro timer
def start_pomodoro(update, context):
    global session_count, in_break
    in_break = False
    session_count += 1
    if session_count % 4 == 0:
        update.message.reply_text(
            "Pomodoro started! Select a time interval.",
            reply_markup=ReplyKeyboardMarkup(
                [["/15", "/20", "/25", "/30"]],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
    else:
        update.message.reply_text(
            "Pomodoro started! Select a time interval.",
            reply_markup=ReplyKeyboardMarkup(
                [["/15", "/20", "/25", "/30"]],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )


# Function to handle time interval selection
def select_time_interval(update, context):
    global session_count
    selected_interval = update.message.text
    if selected_interval not in time_intervals:
        update.message.reply_text(
            "Invalid time interval. Please select a valid interval."
        )
        return
    interval_seconds = time_intervals[selected_interval]
    update.message.reply_text(f"Pomodoro started for {selected_interval}. Focus!")

    # Sleep for the selected interval
    time.sleep(interval_seconds)

    # Send a message when the interval ends
    update.message.reply_text("Time's up!")
    if session_count % 4 == 0:
        update.message.reply_text(
            "Long break time! Take 15 minutes break.",
            reply_markup=ReplyKeyboardMarkup(
                [["Start Pomodoro Break"]], resize_keyboard=True
            ),
        )
        time.sleep(LONG_BREAK_INTERVAL)
    else:
        update.message.reply_text(
            "Short break time! Take 5 minutes break.",
            reply_markup=ReplyKeyboardMarkup(
                [["Start Pomodoro Break"]], resize_keyboard=True
            ),
        )
        time.sleep(SHORT_BREAK_INTERVAL)


# Function to handle the /stop command
def stop_pomodoro(update, context):
    global in_break
    if in_break == False:
        update.message.reply_text("Pomodoro session is already paused.")
    else:
        in_break = True
        update.message.reply_text("Pomodoro session paused. Type /start to resume.")


# Function to handle all messages
# def echo(update, context):
#     global in_break
#     if in_break:
#         update.message.reply_text(
#             "Please use the /start command to resume the Pomodoro session."
#         )
#     else:
#         update.message.reply_text(
#             "You're currently in a Pomodoro session. Please focus until the break."
#         )


def main():
    # Set up the Telegram bot
    updater = Updater(
        "6745939952:AAFd0OSxtOG9jR-wImr7v9U9VuJNRHMM--Y", use_context=True
    )
    dp = updater.dispatcher

    # Define handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("start_pomodoro", start_pomodoro))

    dp.add_handler(CommandHandler("stop", stop_pomodoro))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(
        MessageHandler(Filters.regex(r"^/15$|^/20$|^/25$|^/30$"), select_time_interval)
    )

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
