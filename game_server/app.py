import os
os.system('clear')
from flask import Flask, render_template
from flask_cors import CORS

# instance the flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# game web server

# to add players to the database
@app.route('/game/login', methods=['GET'])
def login():
	return render_template("login.html")

# to submit answers to the different tasks
@app.route('/game/challenge', methods=['GET'])
def challenge():
	return render_template("challenge.html")


# run the app
app.run(port=8000, host="0.0.0.0", debug=True)