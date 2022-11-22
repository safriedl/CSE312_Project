from flask import request, Flask, abort, render_template, redirect, send_from_directory
from flask_socketio import SocketIO

from dbCode import *
from problem import *

CreateTables()

# calls to insert data.
user = postgresql_system("addUsers", ("a", "xyz"))
user2 = postgresql_system("addUsers", ("b", "website"))
user3 = postgresql_system("addUsers", ("c", "website3"))
user4 = postgresql_system("addUsers", ("d", "website4"))
user5 = postgresql_system("addUsers", ("e", "website5"))

app = Flask("Math Duels")
socket = SocketIO(app)

lobbies = []  # list of groups of max size 2

lobby_counter = 0


@app.route('/', methods=['GET'])
def home():
    return render_template("home_page.html")


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
    print(problemTuple)
    return render_template("local_problem.html", problem=problemTuple[0], ans=problemTuple[1])


@app.route('/profile/<username>', methods=['GET'])
def hello(username):
    user_data = postgresql_system("getUser", username)
    if user_data:
        wins = user_data[1]
        games_played = user_data[4]
        return render_template('user_profile_template.html', wins=wins, played=games_played, user=username)
    else:
        abort(404)


@app.route('/lobby')
def join_lobby():
    username = ""
    args = request.args
    if "name" in args.keys():
        username = args["name"]
    users = postgresql_system("allUsers")
    print(users)
    if username in users:
        lobbies_open = sum(1 for lob in lobbies if len(lob) != 2)
        if lobbies_open == 0:
            lobbies[len(lobbies)] = [username]
            return redirect(f"/lobby/{len(lobbies)}", 302)
        else:
            for lob in sorted(lobbies, key=lambda x: len(x), reverse=True):
                if len(lob) < 2:
                    if username not in lob:
                        lob.append(username)
                        return redirect(f"/lobby/{lobbies.index(lob)}", 302)
    else:
        return "You must register to join a lobby."


@app.route('/lobby/<lobby_num>')
def lobby(lobby_num):
    return render_template("lobby.html", num=lobby_num, names=", ".join(lobbies[lobby_num]),
                           async_mode=socket.async_mode)


def escape_html(text):
    """Returns a version of the input string with escaped html."""
    return text.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt')


if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=8000, debug=True, allow_unsafe_werkzeug=True)
