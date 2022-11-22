import psycopg2


def postgresql_system(operation, values=None, values2=None):
    """Connects to the database and executes pre-built queries, with the option of two values as parameters.
        The queries are:
            addUsers) Adds a user where value1=username, value2=password\n

            addPoint) Increments a user's gamesWon value, where value1=username

            allUsers) Returns the entire users table

            getUser) Returns all the data from the table of a user, where value1=username

            getLeaderboard) Returns all data from the leaderboard table sorted by gamesWon"""
    result = None
    # Connecting to db. May need to change if setting up to connect to a local db.
    db_host = "DB_postgreSQL"
    database = "MathGameDB"
    username = "user345"
    pwd = "password345"
    port_id = 5432

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=db_host,
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

        elif operation == "getLeaderboard":
            get_script = '''SELECT distinct * FROM users ORDER BY gamesWon DESC fetch first 10 rows only'''
            cur.execute(get_script, values)
            data = cur.fetchall()
            result = data
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

        # cur.execute("DROP TABLE IF EXISTS users") #will clear the table.
        create_user = ''' CREATE TABLE IF NOT EXISTS users (
            id serial Primary Key NOT NULL,
            username varchar(40),
            password varchar(30),
            gamesWon Int default 0,
            gamesPLayed Int default 0)'''
        cur.execute(create_user)

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    # return result
