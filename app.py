import hashlib
import json
import geventwebsocket

from flask import request, Flask, abort, render_template, redirect, send_from_directory, send_file, url_for, \
    make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit

from dbCode import *
from problem import *
import hashlib

CreateTables()


'''user1 = postgresql_system("addUsersFull", ("a", "xyz", "b", 3, 4))
user2 = postgresql_system("addUsersFull", ("b", "xyz", "b", 7, 129))
user3 = postgresql_system("addUsersFull", ("c", "xyz", "b", 5, 69))
user4 = postgresql_system("addUsersFull", ("d", "xyz", "b", 0, 3))
user5 = postgresql_system("addUsersFull", ("e", "xyz", "b", 11, 2222)) need to add more values for new attributes. can also use form to add users now.'''

app = Flask("Math Duels")
socket = SocketIO(app)

lobbies = []  # list of groups of max size 2

connected = []

answers = []

lobby_counter = 0


def escape_html(text):
    """Returns a version of the input string with escaped html."""
    return text.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt')


# --NEW EDITED CODE--
# Given the token, get user all info. May be used by any route that requires checking if user is authenticated and requires getting the user info.
def getUserWithToken(auToken):
    hashed_auth_token = hashlib.sha256(auToken.encode()).hexdigest()
    print(hashed_auth_token)
    users = postgresql_system("allUsers")
    for u in users:
        print(u)
        if u[6] == hashed_auth_token:
            return u  # u = #(id, username, password, salt, gamesWon, gamesPlayed, auToken)
    print("END")
    return None


# 1 Served at the path /, loads up the homepage, and sets the homepage as unauthorized and needs to log in, or already logged in.
@app.route('/', methods=['GET'])
def home():
    auth_token = request.cookies.get('userAuToken')

    user = getUserWithToken(auth_token) if auth_token != None else None
    print("USER", user)
    if user != None:  # Then authenitcated.
        username = user[1]
        return render_template("home_page_au.html", user=username)

    else:
        return render_template("home_page.html", replace="You've accessed the landing page.")
    # Note that this route, /, does not add or change auTokens or signs up or logs in users, etc. just checks if users authenticated or not.


# Automatically signs up users and adds them to the db.
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    user = request.form['username']
    pwd = request.form['password']  # ***Should hash pwd.

    ALL_CHARS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    salt = ''.join([random.choice(ALL_CHARS) for _ in range(10)])
    saltB = salt.encode()
    saltedandhashedpwd = hashlib.sha256(pwd.encode() + saltB).hexdigest()

    userInfo = (
    user, saltedandhashedpwd, salt, 0, 0, None)  # (id, username, password, salt, gamesWon, gamesPlayed, auToken)
    result = postgresql_system("addUsersFull", userInfo)

    # Now user successfully signed-up, return to homepage.
    return render_template("home_page.html",
                           replace="You've successfully signed-up and registered an account, now you can sign-in to play!")


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_name = request.form['username']
    pwd = request.form['password']

    info = postgresql_system("getUser", user_name)

    if info == None:  # When an auToken value doesn't exist in db.
        return render_template("home_page.html",
                               replace="Incorrect username or password, please login or sign-up with a new account.")  # <- This also notifies user of login error, instead of redirect('/', 302)
    # else user info exists in db.

    salt = info[3]
    saltB = salt.encode()
    saltedandhashedpwd = hashlib.sha256(pwd.encode() + saltB).hexdigest()

    if info[2] == saltedandhashedpwd:
        # Then authenticated, serve homepage again with setting the cookie.

        ALL_CHARS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        auth_token = ''.join([random.choice(ALL_CHARS) for _ in range(30)])

        hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
        result = postgresql_system("Update_auth_token", hashed_auth_token, user_name)

        resp = make_response(
            render_template("home_page_au.html", username=info[1]))  # sets in the http headers earlier here.
        resp.set_cookie('userAuToken', auth_token)  # Set the cookie in the http response.
        return resp  # Now, users are logged in, and accessing any route will check if they have an auth_token, and serve custom responses. For example, requesting homepage will serve authorized homepage with username shown.

    else:
        return render_template("home_page.html",
                               replace="Incorrect username or password, please login or sign-up with a new account.")
        # Redirect to homepage, just like after signing up, without setting the auToken. Can also serve homepage and set loginForm to state that incorrect pwd entered. -Already done.


# has been modified it to directly use the auth_token instead.
@app.route('/profile', methods=['GET'])
def profile():
    auth_token = request.cookies.get('userAuToken')  # 1. get auToken.

    info = getUserWithToken(
        auth_token) if auth_token != None else None  # 2. get user_info for the auToken, if auToken exists and valid.
    print("USER", info)
    if info != None:  # 3. Then authenticated.
        username = info[1]
        wins = info[4]
        games_played = info[5]
        return render_template('user_profile_template.html', wins=wins, played=games_played, user=username)

    else:
        return render_template("home_page.html",
                               replace="Please Login first to access your profile.")  # abort(404) #or may send a redirect to homepage.


# --END OF NEW EDITED CODE--


@app.route('/leaderboard', methods=['GET'])
def leader_board():
    users = postgresql_system("getLeaderboard")
    return render_template("leaderboard.html", users=users) #Works now.


@app.route('/scripts/<script>')
def serve_js(script):
    return send_from_directory('scripts', script)


#--Live Game Management--
@app.route('/localgame', methods=['GET'])
def local_game():
    problemTuple = generate_question()
    # REMOVE THE PRINT STATEMENT, DEBUG ONLY
    print("hi")
    print(problemTuple)
    return render_template("local_problem.html", problem=problemTuple[0], ans=problemTuple[1])


@app.route('/lobby')
def join_lobby():
    print("made it to lobby", flush=True)
    cookies = request.cookies
    print(cookies, flush=True)
    auth_token = cookies.get('userAuToken')
    hashed_auth_token = hashlib.sha256(auth_token.encode()).hexdigest()
    username = postgresql_system("getUserByAuthToken", values=hashed_auth_token)[0]
    print(f"FOUND USERNAME: {username}", flush=True)
    if username is not None:
        lobbies_open = sum(1 for lob in lobbies if len(lob) != 2)
        print(f"LOBBIES OPEN: {lobbies_open}", flush=True)
        if lobbies_open == 0:
            lobbies.append([username])
            connected.append([])
            answers.append(0)
            return render_template("lobby.html", user=username, num=len(lobbies) - 1,
                                   async_mode=socket.async_mode)
        else:
            for lob in sorted(lobbies, key=lambda x: len(x), reverse=True):
                if len(lob) < 2:
                    if username not in lob:
                        lob.append(username)
                        return render_template("lobby.html", user=username, num=lobbies.index(lob),
                                               async_mode=socket.async_mode)
    else:
        return "You must logged in to join a lobby."


@app.route('/functions.js')
def send_functions():
    return send_file('functions.js', "text/javascript")


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
    answers[int(room)] = ans
    emit("problem", json.dumps({'question': qst, 'answer': ans}), to=room)


@socket.event
def validate_answer(data):
    username = data["user"]
    room = data["room"]
    answer = data["answer"]
    print(data, flush=True)
    print(answers, flush=True)
    if int(answer) != int(answers[int(room)]):
        emit("answered_incorrect", f"{username} guesses {answer}. They are INCORRECT!", to=room)
    else:
        emit("answered_correct", json.dumps({"user": username, "answer": answers[int(room)]}), to=room)


@socket.event
def solved_and_won(data):
    user = data["winner"]
    print(data, flush=True)
    postgresql_system("addPoint", values2=user)
    postgresql_system("addPlayed", values2=user)


@socket.event
def solved_and_lost(data):
    user = data["loser"]
    print(data, flush=True)
    postgresql_system("addPlayed", values2=user)


@socket.event
def clear_room(data):
    room = int(data["room"])
    leave_room(data["room"])
    lobbies[room] = []
    connected[room] = []
    answers[room] = 0


if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=8000, debug=True, log_output=True)
