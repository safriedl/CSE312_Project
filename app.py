from flask import request, Flask, abort, render_template

from dbCode import *
CreateTables()



#calls to insert data.
user = postgresql_system("addUsers", ("a", "xyz"))
user2 = postgresql_system("addUsers", ("b", "website"))
user3 = postgresql_system("addUsers", ("c", "website3"))
user4 = postgresql_system("addUsers", ("d", "website4"))
user5 = postgresql_system("addUsers", ("e", "website5"))



app = Flask("project name")


@app.route('/', methods=['GET'])
def h():
    return "hello"


@app.route('/leaderboard', methods=['GET'])
def leader_board():
    users = postgresql_system("getLeaderboard")
    return render_template("leaderboard.html", users=users)  


@app.route('/profile/<user_name>', methods=['GET'])
def hello(user_name):
    user_data = postgresql_system("getUser", user_name)
    if user_data:
        wins = user_data[1] #42  # leaderboard db not implemented yet, QUERY HERE
        games_played = user_data[4] #420  # leaderboard db not implemented yet, QUERY HERE
        return render_template('user_profile_template.html', wins=wins, played=games_played, user=user_name)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
