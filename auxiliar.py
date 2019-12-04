import sqlite3

def check_user(id):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.execute(''' SELECT * FROM USER WHERE ID = %s; ''' % id)
    conn.commit()
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(id):
    conn = sqlite3.connect('sqlite.db')
    conn.execute(''' INSERT INTO USER (ID) VALUES (%s); ''' % (id,))
    conn.commit()
    conn.close()

def create_db():
    conn = sqlite3.connect('sqlite.db')
    conn.execute(''' DROP TABLE IF EXISTS USER; ''')
    conn.commit()
    conn.execute(''' CREATE TABLE USER (
           ID INT PRIMARY KEY NOT NULL,
           USERNAME TEXT,
           PASSWORD TEXT
        ); ''')
    conn.commit()
    conn.close()
    print("Base de datos creada correctamente.")