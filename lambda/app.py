import os
os.system('clear')
from flask import Flask, request, jsonify
from modules.controllers import * # here are all the lambda functions

# instance the flask app
app = Flask(__name__)


# discord api for general commands
#		   lambda how many chapters has steins;gate?
#      lambda turn on the light 1
# 		 lambda pon hikaru-nara
@app.route('/lambda/discordo', methods=['GET'])
def discordo():
	if request.method == 'GET':
  	# extract the message
 		msg = request.headers.get('msg')
 		# process the message
 		ans = discord_msg(msg)
 		# and send the anser
 		return jsonify({'answer': ans})
 		# para recibir, solamente es ans.json() y ya

# discord api for specific commands:
#     l turn on the light 1
#     l request
@app.route('/lambda/discordo/commands', methods=['GET'])
def discordo_commands():
	if request.method == 'GET':
  	# extract the message
 		msg = request.headers.get('msg')
 		# process the message
 		ans = discord_cmd(msg)
 		# and send the anser
 		return jsonify({'answer': ans})
 		# para recibir, solamente es ans.json() y ya



# telegram api
@app.route('/lambda/telegram', methods=['GET'])
def telegram():
	if request.method == 'GET':
  		# extract the message
 		msg = request.headers.get('msg')
 		return 'this is a get request'



# app for the game
@app.route('/lambda/game', methods=['GET','POST'])
def game():
	# to register the players
	if request.method == 'POST':
		# extract the message
		name = request.headers.get('name')
		_id = request.headers.get('id')
		# append the player
		ok = append_player((name,_id))
		return jsonify({'answer': ok})


# run the app
app.run(port=8000, host="127.0.0.1", debug=True)