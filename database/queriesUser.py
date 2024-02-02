import psycopg2
from psycopg2 import sql
from model.user import User

def get_user_db(id, database):
    print(f'Requested user with id {id}')
    connection = psycopg2.connect(database)
    with connection.cursor() as cur:
        cur.execute(f'''
                    SELECT id, email, emailverified, 
                            profilepictureurl, provider, username, 
                            CAST(COUNT(roomId) AS INT) AS matchesPlayed, 
                            CAST(SUM(CASE
                                    WHEN results = 0 AND id = userIdOne THEN 1
                                    WHEN results = 1 AND id = userIdTwo THEN 1
                                    ELSE 0
                                END) AS INT) AS matchesWon,
                            elorank, country, 
                            TO_CHAR(signupDate:: DATE, 'dd Mon yyyy') 
                    FROM 
                        users
                    LEFT JOIN
                        matches ON (id = userIdOne OR id = userIdTwo) and matchType = 'ONLINE'
                    WHERE 
                        id = '{id}'
                    GROUP BY id;
                    ''')
        ret = cur.fetchone()
        print("ENTRO")
        print(ret)
        if ret:
            return User(*ret)
        else:
            return None


def insert_user_db(user_info, database):
    print(f'Inserting {user_info}')
    connection = psycopg2.connect(database)

    with connection.cursor() as cur:
        fields = list(user_info.keys())
        values = list(user_info.values())
        print(fields, values)
        try:
            cur.execute(""" 
                INSERT INTO users ({}) VALUES ({}); """.format(', '.join(fields), ', '.join(['%s'] * len(fields))), values)
            connection.commit()
            return {'msg': f"Insert user into the database"}, 200
        except (Exception, psycopg2.Error) as err:
            return {'msg': "Error while interacting with PostgreSQL...\n", 'err': str(err)}, 400


def update_user_db(id, user_info, database):
    print(f'Updating user with id {id} to {user_info}')
    connection = psycopg2.connect(database)

    with connection.cursor() as cur:
        fields = list(user_info.keys())
        values = list(user_info.values())
        set_clause = sql.SQL(', ').join(sql.SQL("{} = %s").format(
            sql.Identifier(field)) for field in fields)

        try:
            cur.execute("""
                UPDATE users SET {} WHERE id = %s;""".format(', '.join(['{}=%s'.format(field) for field in fields])), values + [id])
            connection.commit()
            return {'msg': f"User updated successfully"}, 200
        except (Exception, psycopg2.Error) as err:
            return {'msg': "Error while updating user in PostgreSQL...\n", 'err': str(err)}, 400


def delete_user_db(id, database):
    print(f'Deleting user with id {id}')
    connection = psycopg2.connect(database)
    with connection.cursor() as cur:
        try:
            cur.execute("DELETE FROM users WHERE id = %s;", (id,))
            connection.commit()
            return {'msg': f"User deleted successfully"}, 200
        except (Exception, psycopg2.Error) as err:
            return {'msg': "Error while deleting user in PostgreSQL...\n", 'err': str(err)}, 400

