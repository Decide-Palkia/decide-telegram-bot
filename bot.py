import telebot
import sqlite3
import json
import requests
import auxiliar

try:
    TELEGRAM_TOKEN = json.load(open('data.json'))['telegram-token']
    CREATE_DB_COMMAND = json.load(open('data.json'))['create-db-command']
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    print("Bot @%s conectado correctamente." % str(bot.get_me().username))
    auxiliar.create_db()
except:
    print("Por favor, indique su TELEGRAM_TOKEN y su CREATE_DB_COMMAND.")

@bot.message_handler(commands=[CREATE_DB_COMMAND])
def reset_database(message):
    conn = sqlite3.connect('sqlite.db')
    bot.send_message(message.from_user.id, "Base de datos conectada correctamente.")
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos eliminada correctamente.")
    conn.execute(''' CREATE TABLE USER (
       ID INT PRIMARY KEY NOT NULL,
       USERNAME TEXT,
       PASSWORD TEXT
    ); ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos creada correctamente.")
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = auxiliar.check_user(message.from_user.id)
    if user is None:
        bot.send_message(message.from_user.id, "¡Bienvenido a Decide, " + str(message.from_user.first_name) + "!")
        bot.send_message(message.from_user.id, "¡Encantado de conocerte!")
        auxiliar.create_user(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, "¡Hola de nuevo, " + str(message.from_user.first_name) + "!")

@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message, message.text[message.json['entities'][0]['length']:])

bot.polling(none_stop=True, timeout=120)