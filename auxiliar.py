import sqlite3
import requests
import logging
import json
from Crypto.Random import random


logging.basicConfig(filename="file.log", filemode='w', level=logging.INFO,
                    format='[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

CREATE_USER_SQL = ''' CREATE TABLE USER (
           CHAT_ID INTEGER PRIMARY KEY NOT NULL,
           TOKEN TEXT,
           USER_ID INT,
           USERNAME TEXT
        );'''

CREATE_STATUS_SQL = ''' CREATE TABLE STATUS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT ,
            CHAT_ID INT NOT NULL,
            IS_LOGIN BOOLEAN DEFAULT 0,
            IS_VOTING BOOLEAN DEFAULT 0,
            IS_SENDING BOOLEAN DEFAULT 0,
            FOREIGN KEY(CHAT_ID) REFERENCES USER(CHAT_ID) ON DELETE CASCADE
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
        FOREIGN KEY(CHAT_ID) REFERENCES USER(CHAT_ID) ON DELETE CASCADE
); '''

CREATE_OPTION_SQL = ''' CREATE TABLE OPTION (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        VOTING_ID INT NOT NULL,
        NUMBER INT NOT NULL,
        TEXT TEXT NOT NULL,
        FOREIGN KEY(VOTING_ID) REFERENCES VOTING(VOT_ID) ON DELETE CASCADE
); '''

def check_user(id):
    conn = get_db()
    cursor = conn.execute(''' SELECT * FROM USER WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    user = cursor.fetchone()
    conn.close()
    return user

def check_test(table,atribute,id):
    conn = get_db()
    cursor = conn.execute(''' SELECT * FROM %s WHERE %s = %s; '''  % (table,atribute,id))
    conn.commit()
    result = cursor.fetchone()
    conn.close()
    return result

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
    conn.execute(''' UPDATE STATUS SET IS_LOGIN = '0' WHERE CHAT_ID = %s; ''' % id)
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
    response = requests.post(url=base_url + "/authentication/login/", data=form)
    if response.status_code is 200:
        token = response.json()['token']
        save_value(id, token, "TOKEN", "USER")
        res = True

        form = {"token": token}
        response = requests.post(url=base_url + "/authentication/getuser/", data=form)
        if response.status_code is 200:
            user_id = response.json()['id']
            save_value(id, user_id, "USER_ID", "USER")

    return res


def get_db():
    return sqlite3.connect('sqlite.db')    

def set_is_voting(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_VOTING = 'TRUE' WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def set_is_not_voting(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_VOTING = '0' WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def set_is_sending(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_SENDING = 'TRUE' WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def set_is_not_sending(id):
    conn = get_db()
    conn.execute(''' UPDATE STATUS SET IS_SENDING = '0' WHERE CHAT_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def get_options_from_voting(id):
    conn = get_db()
    conn.execute(''' SELECT * FROM OPTION WHERE VOTING_ID = %s; ''' % id)
    conn.commit()
    conn.close()

def create_voting(chat_id, vot_id , name , desc , p, g , y ):
    conn = get_db()
    conn.execute(''' INSERT INTO VOTING(CHAT_ID, VOT_ID , NAME , DESC , P, G , Y) VALUES (%s,%s,'%s','%s','%s','%s','%s'); ''' % (chat_id, vot_id , name , desc , p, g , y ))
    conn.commit()
    conn.close()    

def create_option(voting_id , number , text):
    conn = get_db()
    conn.execute(''' INSERT INTO OPTION(VOTING_ID, NUMBER , TEXT) VALUES (%s,%s,'%s'); ''' % (voting_id, number , text ))
    conn.commit()
    conn.close()    



def get_find_voting_and_get_options(chat_id, base_url, voting_id):
    res = False
    form = {
        "voting": voting_id,
    }
    response = requests.post(url=base_url + "/booth/getvoting/", data=form)
    numbers =  []
    options =  []
    if response.status_code is 200:
        res = True
        vot_id = int(response.json()['id'])
        name = response.json()['name']
        desc = response.json()['desc']
        question = response.json()['question']
        optionsJSONs = question['options']
        for i in range(0, len(optionsJSONs)):
            number = question['options'][i]['number']
            option = question['options'][i]['option']
            numbers.append(number)
            options.append(option)
        pub_key = response.json()['pub_key']
        p = pub_key['p']
        g = pub_key['g']
        y = pub_key['y']
        create_voting(chat_id, vot_id , name , desc , p, g , y )

        

    return res , numbers , options

 
def send_data(user, token, voting, vote, base_url):
    data = json.dumps({
            'voter': int(user),
            'token': str(token),
            'voting': int(voting),
            'vote': {'a': str(vote[0]), 'b': str(vote[1])}
        })
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Token ' + token
    }
    r = requests.post(url = base_url + '/store/', data = data, headers = headers)
    return r


def encrypt(pk, M):
    M = int(M)
    k = random.StrongRandom().randint(1, int(pk["p"]) - 1)
    a = pow(int(pk["g"]), k, int(pk["p"]))
    b = (pow(int(pk["y"]), k, int(pk["p"])) * M) % int(pk["p"])
    return a, b

def select_all_options_from_voting(vot_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(''' SELECT TEXT FROM OPTION WHERE VOTING_ID = %s; ''' % vot_id)
    rows = [row[0] for row in cur.fetchall()]
    conn.commit()
    return rows

def select_param_voting(chat_id, param):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(''' SELECT %s FROM VOTING WHERE CHAT_ID = %s; ''' % ( param, chat_id))
    p = cur.fetchone()
    conn.commit()
    return p

def select_param_user(chat_id, param):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(''' SELECT %s FROM USER WHERE CHAT_ID = %s; ''' % ( param, chat_id))
    p = cur.fetchone()
    conn.commit()
    return p[0]

def make_pup_key(chat_id):
    p = select_param_voting(chat_id,'P')
    g = select_param_voting(chat_id,'G')
    y = select_param_voting(chat_id,'Y')
    pup_key = {
        'p': str(int(p[0])),
        'g': str(int(g[0])),
        'y': str(int(y[0])),
    }
    return pup_key
