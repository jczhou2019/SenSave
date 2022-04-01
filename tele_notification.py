import requests
import telegram.bot

def send_message(message, file_name):
    bot.send_document(chat_id=chat_id, document=open(file_name, 'rb'))
    url = 'https://api.telegram.org//sendMessage?chat_id='
    url += message
    requests.get(url)

token = ""
chat_id = ""
bot = telegram.Bot(token=token)