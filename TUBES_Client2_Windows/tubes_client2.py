# TUGAS BESAR PPLJ
# CLIENT 2 
# Reference : https://github.com/BekBrace/postgresql-connection-to-python-
# https://www.reddit.com/r/learnpython/comments/duu49c/sha256_hash_and_salt_with_python_different/


# SHA-256
# import hashlib
# salt = 'YXBweTJoZWxwYW5hbHl0aWNz'
# input_string = '183863'
# salted_input_string = input_string+salt
# hashlib.sha256(salted_input_string.encode('utf-8')).hexdigest()

import psycopg2

from config import config

def connect():
    connection = None
    try:
        params  = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        #create cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

if __name__== "__main__":
    connect()