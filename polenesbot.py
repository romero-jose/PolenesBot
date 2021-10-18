import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import scrape

CREDENTIAL_FILE = 'credential.txt'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message"""
    update.message.reply_text(update.message.text)


def polenes(update: Update, context: CallbackContext) -> None:
    """Respond with the corresponding pollen level"""
    text = update.message.text
    text = text.lower()
    polenes = scrape.scrape_polenes()
    for name, value in polenes.items():
        if text.find(name.lower()) != -1:
            update.message.reply_text(
                f"Actualmente hay {value} g/m^3 de polen de {scrape.FULL_NAMES[name]}")


def main() -> None:
    # Creat the Updater and pass it to the bot's token from a file
    with open(CREDENTIAL_FILE) as file:
        updater = Updater(file.readline().strip())

    # Get the dispatcher to registre handlers
    dispatcher = updater.dispatcher

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, polenes))

    # Start the Bot
    updater.start_polling()

    # Run the but until you press Ctrl-C or the process recieves SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()