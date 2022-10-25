from flask import request, Flask, abort, render_template
import psycopg2

app = Flask("project name")


# --------------------------------Database Code-----------------------------|
def postgresql_system(operation, values=None,
                      values2=None):  # two functions should be allocated within another file, and called from here only.
    result = None
    # Connecting to db. May need to change if setting up to connect to a local repo.
    DBhost = "DB_postgreSQL"
    database = "MathGameDB"
    username = "user345"
    pwd = "password345"
    port_id = 5432

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=DBhost,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )
        cur = conn.cursor()

        if operation == "addUsers":
            insert_script = 'INSERT INTO users (username, password) VALUES (%s,%s)'  # add username.
            cur.execute(insert_script, values)

            cur.execute('SELECT * FROM users where username = %s', (values[0],))  # return added username.
            tuple = cur.fetchone()
            result = tuple

        elif operation == "addPoint":
            update_script = '''UPDATE users SET gamesWon = gamesWon + 1 
                                where username = %s'''
            cur.execute(update_script, (values2,))

        elif operation == "allUsers":
            cur.execute('SELECT * FROM users', ())
            tuple = cur.fetchall()
            result = tuple

        elif operation == "getUser":
            get_script = '''SELECT * FROM users WHERE username = %s'''
            cur.execute(get_script, values)
            data = cur.fetchone()
            result = data

        # elif operation == "":
        # elif operation == "":
        # elif operation == "":
        # else:
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return result


def CreateTables():
    result = None
    # Connecting to Database. May need to change if setting up to connect to a local repo.
    DBhost = "DB_postgreSQL"
    database = "MathGameDB"
    username = "user345"
    pwd = "pasword345"
    port_id = 5432

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=DBhost,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )
        cur = conn.cursor()

        # cur.execute("DROP TABLE IF EXISTS users") #will clear the table.
        create_user = ''' CREATE TABLE IF NOT EXISTS users (
            id serial Primary Key NOT NULL,
            username varchar(40),
            password varchar(30),
            gamesWon Int default 0)'''
        cur.execute(create_user)

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return result


# |--------------------------------Database Code-----------------------------|
# example calls
CreateTables()
user = postgresql_system("addUsers", ("a", "xyz"), None)
user2 = postgresql_system("addUsers", ("b", "website"), None)
user3 = postgresql_system("addUsers", ("c", "website3"), None)
user4 = postgresql_system("addUsers", ("d", "website4"), None)
user5 = postgresql_system("addUsers", ("e", "website5"), None)

LeaderBoard = postgresql_system("allUsers", None, None)
print(LeaderBoard)  # This is printed


@app.route('/profile/<user_name>', methods=['GET'])
def hello(user_name):
    user_data = postgresql_system("getUser", user_name)
    if user_data:
        wins = 42  # leaderboard db not implemented yet, QUERY HERE
        games_played = 420  # leaderboard db not implemented yet, QUERY HERE
        return render_template('user_profile_template.html', wins=wins, played=games_played, user=user_name)
    else:
        abort(404)
