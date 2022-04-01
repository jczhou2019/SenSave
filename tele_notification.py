import requests
import telegram.bot

def send_message(message, file_name):
    bot.send_document(chat_id=chat_id, document=open(file_name, 'rb'))
    url = 'https://api.telegram.org/bot5113109308:AAENaQru78uzWvK74dMxdvuNkovU8Q_RH-A/sendMessage?chat_id=-607935510&text='
    url += message
    requests.get(url)

token = "5113109308:AAENaQru78uzWvK74dMxdvuNkovU8Q_RH-A"
chat_id = "-607935510"
bot = telegram.Bot(token=token)