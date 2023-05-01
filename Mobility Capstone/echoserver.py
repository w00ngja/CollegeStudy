# Packages
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, CallbackContext
# Enable logging
logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO )
logger = logging.getLogger(__name__)

# Message Handlers
def start(update: Update, context: CallbackContext) -> None:
    """send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text('start')
    print(update.message.chat_id)

def help_command(update: Update, context: CallbackContext) -> None:
    """send a message when the command /help is issued."""
    update.message.reply_text('start')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def calc(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
    tokens = update.message.text.split(' ')
    arg1 = int(tokens[1])
    op = tokens[2]
    arg2 = int(tokens[3])

    if op == '+':
        update.message.reply_text(f'{arg1 + arg2}')
    elif op == '-':
        update.message.reply_text(f'{arg1 - arg2}')
    elif op == '*':
        update.message.reply_text(f'{arg1 * arg2}')
    elif op == '/':
        update.message.reply_text(f'{arg1 / arg2}')
    elif op == '^':
        update.message.reply_text(f'{arg1 ** arg2}')

    pass

def main() -> None:
    """Start the bot."""
# Create the Updater and pass it your bot's token.
    updater = Updater("6076808748:AAF9c9YEEK1bHhig8bIIE4IQvYe6q-SDGmQ")
# Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
# on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("calc", calc))
# on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the Bot
    updater.start_polling()
# Run the bot until you press Ctrl-C or the process receives SIGINT, # SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()