import sqlite3
import requests
import logging

logging.basicConfig(filename="file.log", filemode='w', level=logging.INFO,
                    format='[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

CREATE_USER_SQL = ''' CREATE TABLE USER (
           CHAT_ID INTEGER PRIMARY KEY NOT NULL,
           TOKEN TEXT,
           USER_ID INT,
           USERNAME TEXT
        );'''

CREATE_STATUS_SQL = ''' CREATE TABLE STATUS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CHAT_ID INT NOT NULL,
            IS_LOGIN BOOLEAN DEFAULT 0,
            IS_VOTING BOOLEAN DEFAULT 0,
            FOREIGN KEY(CHAT_ID) REFERENCES USER(ID) ON DELETE CASCADE
); '''

CREATE_VOTING_SQL = ''' CREATE TABLE VOTING (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CHAT_ID INT NOT NULL,
        VOT_ID INT NOT NULL,
        NAME TEXT NOT NULL,
        DESC TEXT NOT NULL,
        P TEXT NOT NULL,
        G TEXT NOT NULL,
        Y TEXT NOT NULL,
        FOREIGN KEY(CHAT_ID) REFERENCES USER(ID) ON DELETE CASCADE
); '''

CREATE_OPTION_SQL = ''' CREATE TABLE OPTION (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        VOTING_ID INT NOT NULL,
        NUMBER INT NOT NULL,
        TEXT TEXT NOT NULL,
        FOREIGN KEY(VOTING_ID) REFERENCES VOTING(ID) ON DELETE CASCADE
); '''

def check_user(id):
    conn = get_db()
    cursor = conn.execute(''' SELECT * FROM USER WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(id):
    conn = get_db()
    conn.execute(''' INSERT INTO USER (CHAT_ID) VALUES (%s); ''' % id)
    conn.execute(''' INSERT INTO STATUS (CHAT_ID) VALUES (%s); ''' % id)
    conn.commit()
    conn.close()

def create_db():
    conn = get_db()
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.execute(''' DROP TABLE IF EXISTS STATUS; ''')
    conn.execute(''' DROP TABLE IF EXISTS VOTING; ''')
    conn.execute(''' DROP TABLE IF EXISTS OPTION; ''')
    conn.commit()
    conn.execute(CREATE_USER_SQL)
    conn.execute(CREATE_STATUS_SQL)
    conn.execute(CREATE_VOTING_SQL)
    conn.execute(CREATE_OPTION_SQL)
    conn.commit()
    conn.close()
    logging.info("Base de datos creada correctamente.")

def reset_db(bot, message):
    conn = get_db()
    bot.send_message(message.from_user.id, "Base de datos conectada correctamente.")
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.execute(''' DROP TABLE IF EXISTS STATUS; ''')
    conn.execute(''' DROP TABLE IF EXISTS VOTING; ''')
    conn.execute(''' DROP TABLE IF EXISTS OPTION; ''')
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos eliminada correctamente.")
    conn.execute(CREATE_USER_SQL)
    conn.execute(CREATE_STATUS_SQL)
    conn.execute(CREATE_VOTING_SQL)
    conn.execute(CREATE_OPTION_SQL)
    conn.commit()
    bot.send_message(message.from_user.id, "Base de datos creada correctamente.")
    conn.close()

def set_is_login(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_LOGIN = 'TRUE' WHERE CHAT_ID = %s; ''' % id)
    conn.execute(''' UPDATE USER SET USERNAME = NULL, USER_ID = NULL, TOKEN = NULL WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def set_is_not_login(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_LOGIN = 'FALSE' WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def check_value(id, value, table):
    conn = get_db()
    cursor = conn.execute(''' SELECT %s FROM %s WHERE CHAT_ID = %s; ''' % (value, table, id))
    conn.commit()
    v = cursor.fetchone()
    conn.close()
    return v[0]

def save_value(id, value, column, table):
    conn = get_db()
    conn.execute(''' UPDATE %s SET %s = '%s' WHERE CHAT_ID = %s; ''' % (table, column, value, id))
    conn.commit()
    conn.close()

def delete_value(id, column, table):
    conn = get_db()
    conn.execute(''' UPDATE %s SET %s = %s WHERE CHAT_ID = %s; ''' % (table, column, 'null', id))
    conn.commit()
    conn.close()

def get_save_token_and_id(id, base_url, password):
    res = False
    username = check_value(id, "USERNAME", "USER")
    form = {
        "username": username,
        "password": password
    }
    response = requests.post(url=base_url + "/gateway/authentication/login/", data=form)
    if response.status_code is 200:
        token = response.json()['token']
        save_value(id, token, "TOKEN", "USER")
        res = True

        form = {"token": token}
        response = requests.post(url=base_url + "/gateway/authentication/getuser/", data=form)
        if response.status_code is 200:
            user_id = response.json()['id']
            save_value(id, user_id, "USER_ID", "USER")

    return res

def get_db():
    return sqlite3.connect('sqlite.db')