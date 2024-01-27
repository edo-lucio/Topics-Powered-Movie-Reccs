from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

import sys
sys.path.append('./src')

import os
from dotenv import load_dotenv
load_dotenv()

from src.scoring import Score
import pandas as pd

TOKEN = os.getenv("TOKEN")
ACC_DB = os.getenv("DB_ACC")

movies = pd.read_csv("./data/movies_collection.csv")
topics = pd.read_csv("./data/topics_collection.csv")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("say some words and i'll give you a movie")

def handle_user_input(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.split(" ")
    update.message.reply_text(f'a movie with {update.message.text} ? let me think about it')
    s = Score(movies, topics)

    try:
        reccomendations = s.top_k_similiar_movies(user_input, 12)
        update.message.reply_text('this is what you get:\n{}'.format('\n'.join(reccomendations)))
    except: 
        update.message.reply_text('no movies with such words :(\n')

        
def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Register a MessageHandler to handle all text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_input))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
