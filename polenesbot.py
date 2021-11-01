import scrape
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ForceReply
import os
import logging

from dotenv import load_dotenv
load_dotenv()


PORT = int(os.environ.get('PORT', '8443'))
TOKEN = os.environ.get('TELEGRAM_TOKEN')
URL = os.environ.get('URL')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}, me puedes preguntar por el nivel de polen y te responderé\. Los datos son de polenes\.cl, puedes visitarlos para tener más información\.',
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
    matches = []
    for name, value in polenes.items():
        if text.find(name.lower()) != -1:
            matches.append((name, value))
    if not matches:
        update.message.reply_text(
            f"Los tipos de polenes soportados son: {', '.join(scrape.KEYWORDS[:-1])} y {scrape.KEYWORDS[-1]}.")
    else:
        for name, value in matches:
            update.message.reply_text(
                f"Actualmente hay {value} g/m^3 de polen de {scrape.FULL_NAMES[name]}")


def main() -> None:
    # Create the Updater and pass it the token
    updater = Updater(TOKEN)

    # Get the dispatcher to registre handlers
    dispatcher = updater.dispatcher

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, polenes))

    # Start the Bot
    updater.start_webhook(listen='0.0.0.0',
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=URL + TOKEN)

    # Run the but until you press Ctrl-C or the process recieves SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time.
    updater.idle()


if __name__ == '__main__':
    main()
