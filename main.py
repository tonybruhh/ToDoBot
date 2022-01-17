import random
import nltk
import json
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# база интентов для обучения бота
with open('bot_intents.json', encoding='utf-8') as intents_file:
    intents_file = json.load(intents_file)


def get_intent(text):
    for intent in intents_file['intents']:
        for example in intents_file['intents'][intent]['examples']:
            s1 = clean(example)
            s2 = clean(text)
            if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
                return intent
    return 'интент не найден'


# генерация ответа на сообщение
def bot(text):
    intent = get_intent(text)
    if intent != 'интент не найден':
        return random.choice(intents_file['intents'][intent]['responses'])
    else:
        return 'интент не найден'


def clean(text):
    clean_text = ''
    for char in text.lower():
        if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz':
            clean_text += char
    return clean_text


# # основной рабочий цикл
# input_text = ''
# while input_text != 'stop':
#     input_text = input()
#     response = bot(input_text)
#     print(response)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
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
    """Echo the user message."""
    input_text = update.message.text
    output_text = bot(input_text)
    update.message.reply_text(output_text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5054349266:AAGAHLTO1iyDXzqH7TGj1da32KA4mDK8f84")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
