import os
os.system('clear')
from flask import Flask, render_template
from flask_cors import CORS
import requests

# here are defined the hosts
lambda_api = "127.0.0.1:8080"
game_server = "127.0.0.1:8000"

# instance the flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# game web server

# to add players to the database
@app.route('/game/login', methods=['GET'])
def login():
	# host is where the lambda api is
	settings = requests.get(f"http://{lambda_api}/lambda/game/challenge/settings").json()['settings']
	settings['gamehost'] = game_server
	return render_template("login.html", sets=settings)

# to submit answers to the different tasks
@app.route('/game/challenge', methods=['GET'])
def challenge():
	# ch [block | none] it says wether the buttons are shown
	# host is where the lambda api is
	# title is the title for the page, it depends on the week
	# links are where are the chalenges' descriptions
	# then, generate the parameters based on the db
	settings = requests.get(f"http://{lambda_api}/lambda/game/challenge/settings").json()['settings']
	# send the page with the settings based on the db
	return render_template("challenge.html", sets=settings)

# to see the descrption of the challenge
@app.route('/game/challenge/<_id>', methods=['GET'])
def challenge_description(_id):
	description = requests.get(f"http://{lambda_api}/lambda/game/challenge/info/{_id}").json()['description']
	print(description)
	return description

# run the app
print("[SERVER] -> game server running in {game_server}/game")
app.run(port=8000, host="0.0.0.0", debug=True)