import telebot
import json
import auxiliar
import logging
from telebot import types


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

@bot.message_handler(commands=['vote'])
def vote_func(message):
    try:
        auxiliar.set_is_voting(message.from_user.id)
        bot.send_message(message.from_user.id, "Ahora, vas a transmitir un voto para una votación")
        bot.send_message(message.from_user.id, "Por favor,indica el id de la votación en la que quieres participar")
    except Exception as e:
        logging.error("Ha ocurrido un problema al iniciar el proceso de login.", exc_info=True)

@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.send_message(message.from_user.id, "¡Aquí tienes la lista de comandos disponibles!")
        bot.send_message(message.from_user.id, "/start: Inicio del Bot.")
        bot.send_message(message.from_user.id, "/login: Inicia sesión en Decide con tus credenciales.")
        bot.send_message(message.from_user.id, "/vote: Emite un voto en Decide.")
    except Exception as e:
        logging.error("Ha ocurrido un problema al mostrar el mensaje de ayuda.", exc_info=True)

@bot.message_handler(func=lambda m: True)
def any_message(message):
    chat_id = message.from_user.id
    text = str(message.text).strip()
    if auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS") and not auxiliar.check_value(chat_id, "USERNAME", "USER"):
        try:
            auxiliar.save_value(chat_id, text, "USERNAME", "USER")
            bot.send_message(chat_id, "¿Y tu contraseña?")
        except Exception as e:
            logging.error("Ha ocurrido un problema al guardar el username.", exc_info=True)
    elif auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS") and auxiliar.check_value(chat_id, "USERNAME", "USER") and not auxiliar.check_value(chat_id, "IS_VOTING", "STATUS"):
        try:
             if auxiliar.get_save_token_and_id(chat_id, BASE_URL, text):
                 auxiliar.set_is_not_login(chat_id)
                 bot.send_message(message.from_user.id, "¡Perfecto!")
                 bot.send_message(message.from_user.id, "Ya hemos guardado tus credenciales.")
             else:
                 bot.send_message(message.from_user.id, "Lo sentimos, los datos introducidos deben ser incorrectos.")
                 login(message)
        except Exception as e:
            logging.error("Ha ocurrido un problema al obtener las credenciales.", exc_info=True)
            
    elif auxiliar.check_value(chat_id, "IS_VOTING", "STATUS") and not auxiliar.check_value(chat_id, "IS_SENDING", "STATUS") :
        try:
             res , numbers , options  = auxiliar.get_find_voting_and_get_options(chat_id, BASE_URL, text)
             if res:
                 bot.send_message(message.from_user.id, "¡Se han encontrado coincidencias!")
                 bot.send_message(message.from_user.id, "Ahora, selecciona la opción que quieras votar")
                 markup = types.ReplyKeyboardMarkup(row_width=2 , one_time_keyboard= True)
                 for i in range(0,len(options)):
                     option = options[i]
                     number  = numbers[i]
                     optKeyboard = text + '.' +  str(number) + '#' + option
                     itembtn = types.KeyboardButton(optKeyboard)
                     markup.add(itembtn)  
                     auxiliar.create_option(text , number , option)
                 bot.send_message(chat_id, "Elige una opción:", reply_markup=markup)
                 auxiliar.set_is_sending(chat_id)
             else:
                 bot.send_message(message.from_user.id, "Lo sentimos, no se ha encontrado ninguna votación con dicho Id.")
                 bot.send_message(message.from_user.id, "Prueba de nuevo a enviar el id de la votación que quieres buscar.")
                 auxiliar.set_is_not_sending(chat_id)
                 vote_func(message)
        except Exception as e:
            logging.error("Ha ocurrido un problema al obtener tu voto.Vuelve a intentar votar", exc_info=True)

    elif auxiliar.check_value(chat_id, "IS_VOTING", "STATUS") and auxiliar.check_value(chat_id, "IS_SENDING", "STATUS") :
        try:
            texto_recibido = text.split('.') #La opción llega con formato idVotacion.opcion # textoopcion 
            vot_id = texto_recibido[0]
            parteVoto= texto_recibido[1].split('#')
            n_option = parteVoto[0]
            texto_option = parteVoto[1].strip()
            options = auxiliar.select_all_options_from_voting(vot_id)
            if texto_option in options:
                bot.send_message(message.from_user.id, "¡Perfecto!")
                bot.send_message(message.from_user.id, "Ahora, procederemos a procesar tu voto....")
                pup_key = auxiliar.make_pup_key(chat_id)
                a, b = auxiliar.encrypt(pup_key,n_option)
                user = str(auxiliar.select_param_user(chat_id ,'USER_ID' ))
                token  =  str(auxiliar.select_param_user(chat_id ,'TOKEN' ))
                vote =  [a, b]
                final =  auxiliar.send_data(user, token, vot_id, vote, BASE_URL)
                if final.status_code is 200:
                    bot.send_message(message.from_user.id, "Su voto ha sido procesado, gracias por participar en la votación!")
                else:
                    bot.send_message(message.from_user.id, "Su voto no ha podido procesarse, por favor, vuelve a intentarlo")
                    auxiliar.set_is_not_sending(chat_id)
                    vote_func(message)
              
            else:
                bot.send_message(message.from_user.id, "No se ha detectado ninguna respuesta perteneciente a la votación.Por favor, repite el proceso otra vez.")
                auxiliar.set_is_not_sending(chat_id)
                vote_func(message)
                
        except Exception as e:
            logging.error("Ha ocurrido un problema con el proceso. Por favor, vuelve a intentarlo", exc_info=True) 
            bot.send_message(message.from_user.id, "No se ha detectado ninguna respuesta perteneciente a la votación.Por favor, repite el proceso otra vez.")
            auxiliar.set_is_not_sending(chat_id)
            vote_func(message)
         
            

bot.polling(none_stop=True, timeout=120)