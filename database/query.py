import psycopg2
from psycopg2 import sql
import json
from model.user import User

def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
            return credentials
    except FileNotFoundError:
        print(f"File 'credentials.json not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in credentials.json")
        return None

def get_user_db(id):
    print(f'Requested user with id {id}')
    credentials = load_credentials()
    conn = psycopg2.connect(f"dbname={credentials.get('dbname')} user={credentials.get('user')} host='{credentials.get('host')}' password='{credentials.get('password')}'")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users where id = '{id}'")
    ret = cur.fetchone()
    if ret:
        return User(*ret)
    
def insert_user_db(user_info):
    print(f'Inserting {user_info}')
    credentials = load_credentials()
    conn = psycopg2.connect(f"dbname={credentials.get('dbname')} user={credentials.get('user')} host='{credentials.get('host')}' password='{credentials.get('password')}'")
    cur = conn.cursor()
    fields = [*user_info]
    values = [*user_info.values()]
    try:
        cur.execute(""" 
            INSERT INTO users ({}) VALUES ({}); """.format(', '.join(fields), ', '.join(['%s'] * len(fields))), values)
        conn.commit()
        return {'msg': f"Database updated"}, 200
    except(Exception, psycopg2.Error) as err:
        return {'msg': "Error while interacting with PostgreSQL...\n",'err': str(err)}, 400
