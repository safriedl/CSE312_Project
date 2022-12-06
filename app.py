import json

from flask import request, Flask, abort, render_template, redirect, send_from_directory, send_file, url_for, make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit


from dbCode import *
from problem import *

CreateTables()

# calls to insert data.
user1 = postgresql_system("addUsersFull", ("a", "xyz", "b", 3, 4))
user2 = postgresql_system("addUsersFull", ("b", "xyz", "b", 7, 129))
user3 = postgresql_system("addUsersFull", ("c", "xyz", "b", 5, 69))
user4 = postgresql_system("addUsersFull", ("d", "xyz", "b", 0, 3))
user5 = postgresql_system("addUsersFull", ("e", "xyz", "b", 11, 2222))

app = Flask("Math Duels")
socket = SocketIO(app)

lobbies = []  # list of groups of max size 2

connected = []

lobby_counter = 0

# New Code
userTokens = []


# 1 Served at the path /, loads up the homepage, and sets the homepage as unauthorized and needs to log in, or already logged in.







#New Code
userTokens = []
#1 Served at the path /, loads up the homepage, and sets the homepage as unauthorized and needs to log in, or already logged in.
@app.route('/', methods=['GET'])
def home():
    auToken = request.cookies.get('userAuToken')


    if auToken in userTokens:  # Then authenitcated.
        loginForm = '''<h1>New User? Sign-Up:</h1>
            <form action="/sign-up" id="sign-up" method="post">
                <label for="username">Username: </label>
                <input id="username" type="text" name="username">
                <br />
                <label for="password">Password: </label>
                <input id="password" type="text" name="password">
                <input type="submit" value="sign-up">
            </form style="background-color:aquamarine;>
            <h1>Or login:</h1>
            <form action="/login" id="login" method="post">
                <label for="username">Username: </label>
                <input id="username" type="text" name="username">
                <br />
                <label for="password">Password: </label>
                <input id="password" type="text" name="password">
                <input type="submit" value="login">
            </form style="background-color:#1E90FF;>'''
            
    if auToken in userTokens: #Then authenitcated.
        loginForm = '''<h1>New User? Sign-Up:</h1>
        <form action="/sign-up" id="sign-up" method="post">

            <label for="username">Username: </label>
            <input id="username" type="text" name="username">

            <br />
            <label for="password">Password: </label>
            <input id="password" type="text" name="password">
            <input type="submit" value="sign-up">

        </form style="background-color:aquamarine;>



        <h1>Or login:</h1>
        <form action="/login" id="login" method="post">

            <label for="username">Username: </label>
            <input id="username" type="text" name="username">

            <br />
            <label for="password">Password: </label>
            <input id="password" type="text" name="password">
            <input type="submit" value="login">

        </form style="background-color:#1E90FF;>'''

    else:
        loginForm = "<p style='background-color:red;' >You are currently not logged in, please sign-up and login to play the game.</p>"
        return render_template("home_page.html ", loginForm=loginForm)

    # return render_template("home_page.html")
    # Note that this route, /, does not add or change auTokens or signs up or logs in users, etc. ust checks if users authenticated or not.


# automatically signs up users and adds them to the db.
def sign_up():
    user = request.form['username']
    pwd = request.form['password']  # ***Should hash pwd.

    userInfo = (user, pwd, "salt", 0, 0)  # (id, username, password, salt, gamesWon, gamesPlayed)
    result = postgresql_system("addUsersFull", userInfo)

    # Now user successfully signed-up, return to homepage.
    return redirect(url_for('/'))


def login():
    user_name = request.form['username']
    pwd = request.form['password']
    info = postgresql_system("getUser", user_name)
    if info[2] == pwd:  # ***should hash pwd.
        # Then authenticated, serve homepage again with setting the cookie.

        ALL_CHARS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        auth_token = ''.join([random.choice(ALL_CHARS) for _ in range(30)])
        result = postgresql_system("Update_auth_token", auth_token, user_name)

        loginForm = "<p style='background-color:#0000A0;' >Login Success, click start to join a lobby and begin a match.</p>"
        resp = make_response(
            render_template("home_page.html", loginForm=loginForm))  # sets in the http headers earlier here.
        resp.set_cookie('userAuToken', auth_token)  # Set the cookie in the http respone.
        return resp  # Now, users are logged in, and accessing any route will check if they have an auth_token, and serve custom responses. For example, requesting homepage will serve logged in homepage.

    else:
        redirect(url_for(
            '/'))  # Redirect to homepage, just like after signing up, without setting the auToken. Can also serve homepage and set loginForm to state that incorrect pwd entered.


# End of NewCode.
=======
    #return render_template("home_page.html")
    #Note that this route, /, does not add or change auTokens or signs up or logs in users, etc. ust checks if users authenticated or not.


#automatically signs up users and adds them to the db.
def sign_up():
   user = request.form['username']
   pwd = request.form['password']  #***Should hash pwd.

   userInfo = (user, pwd, "salt", 0, 0)  #(id, username, password, salt, gamesWon, gamesPlayed)
   result = postgresql_system("addUsersFull", userInfo )
   
   #Now user successfully signed-up, return to homepage.
   return redirect(url_for('/'))



def login():
   user_name = request.form['username']
   pwd = request.form['password']
   info = postgresql_system("getUser", user_name)
   if info[2] == pwd: #***should hash pwd.
       #Then authenticated, serve homepage again with setting the cookie.

       ALL_CHARS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
       auth_token = ''.join([random.choice(ALL_CHARS) for _ in range(30)])
       result = postgresql_system("Update_auth_token", auth_token, user_name)


       loginForm = "<p style='background-color:#0000A0;' >Login Success, click start to join a lobby and begin a match.</p>"
       resp = make_response(render_template("home_page.html", loginForm=loginForm)) #sets in the http headers earlier here.
       resp.set_cookie('userAuToken', auth_token) #Set the cookie in the http respone.
       return resp #Now, users are logged in, and accessing any route will check if they have an auth_token, and serve custom responses. For example, requesting homepage will serve logged in homepage.

   else:
       redirect(url_for('/')) #Redirect to homepage, just like after signing up, without setting the auToken. Can also serve homepage and set loginForm to state that incorrect pwd entered.
#End of NewCode.



@app.route('/leaderboard', methods=['GET'])
def leader_board():
    users = postgresql_system("getLeaderboard")
    return render_template("leaderboard.html", users=users)


@app.route('/scripts/<script>')
def serve_js(script):
    return send_from_directory('scripts', script)


@app.route('/localgame', methods=['GET'])
def local_game():
    problemTuple = generate_question()
    # REMOVE THE PRINT STATEMENT, DEBUG ONLY
    print("hi")
    print(problemTuple)
    return render_template("local_problem.html", problem=problemTuple[0], ans=problemTuple[1])


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user_data = postgresql_system("getUser", username)
    print(user_data)
    if user_data:
        wins = user_data[4]
        games_played = user_data[5]
        return render_template('user_profile_template.html', wins=wins, played=games_played, user=username)
    else:
        abort(404)


@app.route('/lobby')
def join_lobby():
    args = request.args.to_dict()
    print("made it to lobby", flush=True)
    print(args, flush=True)
    username = args.get("name")
    print(username)
    users = list(map(lambda x: x[0], postgresql_system("allUsers")))
    print(users, flush=True)
    if username in users:
        lobbies_open = sum(1 for lob in lobbies if len(lob) != 2)
        print(f"LOBBIES OPEN: {lobbies_open}", flush=True)
        if lobbies_open == 0:
            lobbies.append([username])
            connected.append([])
            return redirect(f"/lobby/{len(lobbies) - 1}?name={username}", 302)
        else:
            for lob in sorted(lobbies, key=lambda x: len(x), reverse=True):
                if len(lob) < 2:
                    if username not in lob:
                        lob.append(username)
                        return redirect(f"/lobby/{lobbies.index(lob)}?name={username}", 302)
    else:
        return "You must register to join a lobby."


@app.route('/functions.js')
def send_functions():
    return send_file('functions.js', "text/javascript")


@app.route('/lobby/<lobby_num>')
def lobby(lobby_num):
    args = request.args.to_dict()
    username = args.get("name")
    return render_template("lobby.html", user=username, num=lobby_num, names=", ".join(lobbies[int(lobby_num)]),
                           async_mode=socket.async_mode)


@socket.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    if username not in connected[int(room)]:
        join_room(room)  # adds current user to room
        connected[int(room)].append(username)
        print(connected, flush=True)
        print(data, flush=True)
        emit("joined", json.dumps({"username": username, "room_size": len(lobbies[int(room)])}), to=room)


@socket.event
def my_event(data):
    print(data, flush=True)


@socket.event
def get_problem(data):
    room = data['room']
    qst, ans = generate_question()
    print(f"QUESTION: {qst}, ANSWER: {ans}", flush=True)
    emit("problem", json.dumps({'question': qst, 'answer': ans}), to=room)


@socket.event
def validate_answer(data):
    username = data["user"]
    room = data["room"]
    answer = data["answer"]
    correct = data["correct"]
    print(data, flush=True)
    if answer != correct:
        emit("answered_incorrect", f"{username} guesses {answer}. They are INCORRECT!", to=room)
    else:
        emit("answered_correct", json.dumps({"user": username, "answer": correct}), to=room)


def escape_html(text):
    """Returns a version of the input string with escaped html."""
    return text.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt')


if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=8000, debug=True, log_output=True)
