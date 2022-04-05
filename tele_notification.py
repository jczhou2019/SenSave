import requests
import telegram.bot

def send_message(message, file_name):
    bot.send_document(chat_id=chat_id, document=open(file_name, 'rb'))
    url = 'https://api.telegram.org/bot<TOKEN_ID>/sendMessage?chat_id=<CHAT_ID>&text='
    url += message
    requests.get(url)

def send_alert_abnormal(predicted_location, actual_location, duration):
    message = f"Elderly has abnormal movement for {duration} minutes, current location at {actual_location}, predicted location at {predicted_location}."
    url = 'https://api.telegram.org/bot<TOKEN_ID>/sendMessage?chat_id=<CHAT_ID>&text='
    url += message
    requests.get(url) 

def send_alert_not_moving(actual_location, duration):
    message = f"Elderly has not been moving for {duration} minutes, last location at {actual_location}."
    url = 'https://api.telegram.org/bot<TOKEN_ID>/sendMessage?chat_id=<CHAT_ID>&text='
    url += message
    requests.get(url) 

def send_alert_elderleave():
    message = f"Elderly has left the house."
    url = 'https://api.telegram.org/bot<TOKEN_ID>/sendMessage?chat_id=<CHAT_ID>&text='
    url += message
    requests.get(url) 

def send_alert_strangerleave():
    message = f"Stranger has left the house."
    url = 'https://api.telegram.org/bot<TOKEN_ID>/sendMessage?chat_id=<CHAT_ID>&text='
    url += message
    requests.get(url) 

token = "<TOKEN_ID>"
chat_id = "<CHAT_ID>"
bot = telegram.Bot(token=token)