from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import telegram.bot
import pandas as pd


updater = Updater("",
				use_context=True)
token = ""
chat_id = ""

def help(update: Update, context: CallbackContext):
	update.message.reply_text("WORKING ON IT!")


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

def unique_visitors(update: Update, context: CallbackContext):
	df = pd.read_csv("test.csv")
	number_of_visitors = df[df["unique_visitors"]==1].count()["unique_visitors"]
	update.message.reply_text(f"This elderly has {int(number_of_visitors)} visitors this month.")

def where_is_elderly(update: Update, context: CallbackContext):
	location = "Living Room"
	duration = 0
	update.message.reply_text(
		f"Karen is in {location} for {duration} min" % update.message.text)


def bot(update: Update, context: CallbackContext) -> None:
	keyboard = [
		[
		InlineKeyboardButton("Elderly whereabout", callback_data='1'),
		InlineKeyboardButton("Details on unique visitors", callback_data='2'),
		]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text("Replying to text", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    
    # Now u can define what choice ("callback_data") do what like this:
    if choice == '1':
        where_is_elderly()

    if choice == '2':
        unique_visitors()

def profile(update: Update, context: CallbackContext):
	name = "Karen Thiam Siew Siew"
	age = 88
	illness = ["Arthritis", "Have history of falls", "Mild Dementia"]
	dietary = ["No seafood", "G6PD"]
	religion = "Buddist"
	update.message.reply_text(
		f"Name: {name}\nage: {age}\nillness: {','.join(illness)} \nDietary: {','.join(dietary)}\nreligion: {religion}")
	bot.send_document(chat_id="", document=open("known_faces/hoching.jpeg", 'rb'))

updater.dispatcher.add_handler(CommandHandler('profile',profile))
updater.dispatcher.add_handler(CommandHandler('start', bot))
updater.dispatcher.add_handler(CommandHandler('where',where_is_elderly))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('unique', unique_visitors))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

bot = telegram.Bot(token=token)
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()

updater.idle()