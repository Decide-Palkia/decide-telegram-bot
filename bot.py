import telebot
import json
import auxiliar
import logging

logging.basicConfig(filename="file.log", filemode='w', level=logging.INFO,
                    format='[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

try:
    TELEGRAM_TOKEN = json.load(open('data.json'))['telegram-token']
    logging.info("TELEGRAM_TOKEN cargado correctamente.")
    CREATE_DB_COMMAND = json.load(open('data.json'))['create-db-command']
    logging.info("CREATE_DB_COMMAND cargado correctamente.")
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    logging.info("Bot @%s conectado correctamente." % str(bot.get_me().username))
    BASE_URL = json.load(open('data.json'))['base-url']
    auxiliar.create_db()
except Exception as e:
    logging.error("Ha ocurrido un problema durante la inicialización.", exc_info=True)

@bot.message_handler(commands=[CREATE_DB_COMMAND])
def reset_database(message):
    try:
        auxiliar.reset_db(bot, message)
    except Exception as e:
        logging.error("Ha ocurrido un problema al restaurar la base de datos.", exc_info=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user = auxiliar.check_user(message.from_user.id)
        if user is None:
            bot.send_message(message.from_user.id, "¡Bienvenido a Decide, " + str(message.from_user.first_name) + "!")
            bot.send_message(message.from_user.id, "¡Encantado de conocerte!")
            auxiliar.create_user(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, "¡Hola de nuevo, " + str(message.from_user.first_name) + "!")
    except Exception as e:
        logging.error("Ha ocurrido un problema al enviar el mensaje de bienvenida.", exc_info=True)

@bot.message_handler(commands=['login'])
def login(message):
    try:
        auxiliar.set_is_login(message.from_user.id)
        bot.send_message(message.from_user.id, "¡Vamos a guardar tus credenciales!")
        bot.send_message(message.from_user.id, "¿Cuál es tu usuario?")
    except Exception as e:
        logging.error("Ha ocurrido un problema al iniciar el proceso de login.", exc_info=True)

@bot.message_handler(func=lambda m: True)
def any_message(message):
    user_id = message.from_user.id
    text = str(message.text).strip()
    if auxiliar.check_value(user_id, "IS_LOGIN") and not auxiliar.check_value(user_id, "USERNAME") \
            and not auxiliar.check_value(user_id, "PASSWORD"):
        try:
            auxiliar.save_value(user_id, text, "USERNAME")
            bot.send_message(user_id, "¿Y tu contraseña?")
        except Exception as e:
            logging.error("Ha ocurrido un problema al guardar el username.")
    elif auxiliar.check_value(user_id, "IS_LOGIN") and auxiliar.check_value(user_id, "USERNAME") \
            and not auxiliar.check_value(user_id, "PASSWORD"):
        try:
            auxiliar.save_value(user_id, text, "PASSWORD")
            auxiliar.set_is_not_login(user_id)
        except Exception as e:
            logging.error("Ha ocurrido un problema al guardar el password.", exc_info=True)
        try:
             if auxiliar.get_save_token_and_id(user_id, BASE_URL):
                 bot.send_message(message.from_user.id, "¡Perfecto!")
                 bot.send_message(message.from_user.id, "Ya hemos guardado tus credenciales.")
             else:
                 bot.send_message(message.from_user.id, "Lo sentimos, los datos introducidos deben ser incorrectos.")
                 login(message)
        except Exception as e:
            logging.error("Ha ocurrido un problema al obtener las credenciales.", exc_info=True)

bot.polling(none_stop=True, timeout=120)