import sys
import time
import telepot
import os
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from arxivApiClient import *
from json import JSONDecoder as decoder
options = ["Machine Learning", "Otimizacao", "Teoria dos Grafos", "Visao Computacional", "Bioetanol", "Smart Cities"]
translations = {"Otimizacao": "Optimization", "Teoria dos Grafos": "Graph Theory", "Bioetanol" : "Bioethanol", "Visao Computacional": "Computer Vision"}
ansKeyboard = [[KeyboardButton(text="Machine Learning"), KeyboardButton(text="Otimizacao")], [KeyboardButton(text="Teoria dos Grafos"), KeyboardButton(text="Visao Computacional")], [KeyboardButton(text="Smart Cities"), KeyboardButton(text="Bioetanol")]]

def parseJsonToMessages(jsonFile):
    data = decoder().decode(jsonFile)
    n = len(data)
    messages = []
    for i in range(n):
        message = {}
        message["title"] = data[i]["entry"]["title"]
        message["link"] = data[i]["entry"]["id"]
        message["published"] = data[i]["entry"]["published"][:10]
        messages.append(message)
    return messages

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == '/news':
            bot.sendMessage(chat_id, 'Escolha uma categoria',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=ansKeyboard, resize_keyboard=True
                            ))
        elif msg["text"] == "/help":
            bot.sendMessage(chat_id, "/news - para receber ultimos artigos da area desejada")
        elif msg["text"] in options:
            queryTerm = msg["text"]
            if queryTerm in translations:
                queryTerm = translations[queryTerm]
            answer = retrievePaperInfo([queryTerm])
            bot.sendMessage(chat_id, "Ultimos artigos sobre *" + msg["text"] + "*", parse_mode="Markdown")
            for message in parseJsonToMessages(answer):
                bot.sendMessage(chat_id, "*" + message["title"] + "* - " + message["published"] + " - " + message["link"], parse_mode="Markdown")
        else :
            bot.sendMessage(chat_id, "Digite /help para saber como posso te ajudar")

token = os.environ["TELEGRAM_TOKEN"]
bot = telepot.Bot(token)
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)
