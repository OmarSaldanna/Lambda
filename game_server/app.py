import os
os.system('clear')
from flask import Flask, render_template
from flask_cors import CORS
import requests

# instance the flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# game web server

# to add players to the database
@app.route('/game/login', methods=['GET'])
def login():
	# host is where the lambda api is
	settings = {'host': '127.0.0.1:8080'}
	return render_template("login.html", sets=settings)

# to submit answers to the different tasks
@app.route('/game/challenge', methods=['GET'])
def challenge():
	# ch [block | none] it says wether the buttons are shown
	# host is where the lambda api is
	# title is the title for the page, it depends on the week
	# links are where are the chalenges' descriptions
	# then, generate the parameters based on the db
	settings = requests.get("http://127.0.0.1:8080/lambda/game/challenge/settings").json()['settings']
	# send the page with the settings based on the db
	return render_template("challenge.html", sets=settings)

# to see the descrption of the challenge
@app.route('/game/challenge/<_id>', methods=['GET'])
def challenge_description():
	return "desafio 1"

# run the app
print("[SERVER] -> game server running in 127.0.0.1:8000/game")
app.run(port=8000, host="0.0.0.0", debug=True)