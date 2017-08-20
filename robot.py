import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from arxivApiClient import *
from json import JSONDecoder as decoder
options = ["Machine Learning", "Optimization", "Graph Theory", "Computer Vision", "Bioethanol"]
ansKeyboard = [KeyboardButton(text=option) for option in options]


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
                                keyboard=[
                                    ansKeyboard
                                ], resize_keyboard=True
                            ))
        elif msg["text"] == "/help":
            bot.sendMessage(chat_id, "/news - para receber ultimos artigos da area desejada")
        elif msg["text"] in options:
            answer = retrievePaperInfo([msg["text"]])
            for message in parseJsonToMessages(answer):
                bot.sendMessage(chat_id, "*" + message["title"] + "* - " + message["published"] + " - " + message["link"], parse_mode="Markdown")
        else :
            bot.sendMessage(chat_id, "Digite /help para saber como posso te ajudar")

bot = telepot.Bot("420962963:AAECydIqoM2CfaTNQsZ1OVyV6WEm94Ql0F0")
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)
