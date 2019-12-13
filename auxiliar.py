import sqlite3
import requests
import logging

logging.basicConfig(filename="file.log", filemode='w', level=logging.INFO,
                    format='[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

CREATE_DB_SQL = ''' CREATE TABLE USER (
           ID INT PRIMARY KEY NOT NULL,
           IS_LOGIN BOOLEAN DEFAULT 0,
           TOKEN TEXT,
           USER_ID INT,
           USERNAME TEXT,
           PASSWORD TEXT
        ); '''

def check_user(id):
    conn = get_db()
    cursor = conn.execute(''' SELECT * FROM USER WHERE ID = %s; ''' % id)
    conn.commit()
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(id):
    conn = get_db()
    conn.execute(''' INSERT INTO USER (ID) VALUES (%s); ''' % (id,))
    conn.commit()
    conn.close()

def create_db():
    conn = get_db()
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.commit()
    conn.execute(CREATE_DB_SQL)
    conn.commit()
    conn.close()
    logging.info("Base de datos creada correctamente.")

def reset_db(bot, message):
    conn = get_db()
    bot.send_message(message.from_user.id, "Base de datos conectada correctamente.")
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos eliminada correctamente.")
    conn.execute(CREATE_DB_SQL)
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos creada correctamente.")
    conn.close()

def set_is_login(id):
    conn = get_db()
    conn.execute(''' UPDATE USER SET IS_LOGIN = TRUE, USERNAME = Null, PASSWORD = Null, TOKEN = Null WHERE ID = %s; ''' % id)
    conn.commit()
    conn.close()

def set_is_not_login(id):
    conn = get_db()
    conn.execute(''' UPDATE USER SET IS_LOGIN = FALSE WHERE ID = %s; ''' % id)
    conn.commit()
    conn.close()

def check_value(id, value):
    conn = get_db()
    cursor = conn.execute(''' SELECT %s FROM USER WHERE ID = %s; ''' % (value, id))
    conn.commit()
    v = cursor.fetchone()
    conn.close()
    return v[0]

def save_value(id, value, column):
    conn = get_db()
    conn.execute(''' UPDATE USER SET %s = '%s' WHERE ID = %s; ''' % (column, value, id))
    conn.commit()
    conn.close()

def delete_value(id, column):
    conn = get_db()
    conn.execute(''' UPDATE USER SET %s = %s WHERE ID = %s; ''' % (column, 'null', id))
    conn.commit()
    conn.close()

def get_save_token_and_id(id, base_url):
    res = False
    username = check_value(id, "USERNAME")
    pasword = check_value(id, "PASSWORD")
    form = {
        "username": username,
        "password": pasword
    }
    response = requests.post(url=base_url + "/gateway/authentication/login/", data=form)
    if response.status_code is 200:
        token = response.json()['token']
        save_value(id, token, "TOKEN")
        res = True

        form = {"token": token}
        response = requests.post(url=base_url + "/gateway/authentication/getuser/", data=form)
        if response.status_code is 200:
            user_id = response.json()['id']
            save_value(id, user_id, "USER_ID")
            delete_value(id, "PASSWORD")

    return res

def get_db():
    return sqlite3.connect('sqlite.db')