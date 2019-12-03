import telebot
import sqlite3
import json
import requests

try:
    TELEGRAM_TOKEN = json.loads(requests.get(json.load(open('urls.json'))['data1']).content)['telegram-token'] + json.loads(requests.get(json.load(open('urls.json'))['data2']).content)['telegram-token']
    CREATE_DB_COMMAND = json.loads(requests.get(json.load(open('urls.json'))['data1']).content)['create-db-command'] + json.loads(requests.get(json.load(open('urls.json'))['data2']).content)['create-db-command']
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    print("Bot conectado correctamente.")
except:
    print("Por favor, indique su TELEGRAM_TOKEN y su CREATE_DB_COMMAND.")

@bot.message_handler(commands=[CREATE_DB_COMMAND])
def create_database(message):
    conn = sqlite3.connect('sqlite.db')
    bot.send_message(message.from_user.id, "Base de datos conectada correctamente.")
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos eliminada correctamente.")
    conn.execute(''' CREATE TABLE USER (
       ID INT PRIMARY KEY NOT NULL
    ); ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos creada correctamente.")
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "¡Bienvenido a Decide, " + str(message.from_user.first_name) + "!")

@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message, message.text[message.json['entities'][0]['length']:])

bot.polling()