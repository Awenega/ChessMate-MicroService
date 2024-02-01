import psycopg2
from psycopg2 import sql
from model.match import Match

def get_matches_db(id, database):
    connection = psycopg2.connect(database)
    with connection.cursor() as cur:
        cur.execute(f'''
                    SELECT 
                        roomId, matchtype, userIdOne, userIdTwo, 
                        results, COALESCE(username, 'Unknown') AS usernameUserTwo, 
                        COALESCE(profilePictureUrl, 'default.jpg') AS profilePictureUrlUserTwo
                    FROM 
                        matches 
                    LEFT JOIN 
                        users ON userIdTwo = id 
                    WHERE 
                        userIdOne = '{id}'

                    UNION

                    SELECT 
                        roomId, matchType, userIdTwo AS userIdOne, userIdOne AS userIdTwo,
                        results, COALESCE(username, 'Unknown') AS usernameUserTwo, 
                        COALESCE(profilePictureUrl, 'default.jpg') AS profilePictureUrlUserTwo
                        FROM 
                            matches 
                        LEFT JOIN 
                            users ON userIdOne = id 
                        WHERE 
                        userIdTwo = '{id}'
                    ''')
        matches = cur.fetchall()
        if len(matches) < 1:
            return None
        else:
            totalMatches = []
            for match in matches:
                totalMatches.append(Match(*match))
            return totalMatches

def insert_match_db(match_info, database):
    print(f'Inserting {match_info}')
    connection = psycopg2.connect(database)

    with connection.cursor() as cur:
        fields = list(match_info.keys())
        values = list(match_info.values())
        print(fields, values)
        try:
            cur.execute(""" 
                INSERT INTO matches ({}) VALUES ({}); """.format(', '.join(fields), ', '.join(['%s'] * len(fields))), values)
            connection.commit()
            return {'msg': f"Insert match into the database"}, 200
        except (Exception, psycopg2.Error) as err:
            return {'msg': "Error while interacting with PostgreSQL...\n", 'err': str(err)}, 400
    