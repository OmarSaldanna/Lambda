import os
os.system('clear')
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.controllers import * # here are all the lambda functions

lambda_api = "127.0.0.1:8080"

# instance the flask app
app = Flask(__name__)
CORS(app)

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



###############################################
###############################################
#		Game functionality                    #
#		all the bellow is for web funcions    #
###############################################
###############################################



# game: add players
@app.route('/lambda/game/<name>/<_id>', methods=['GET'])
def game(name, _id):
	# extract the message
	print('name', name)
	# append the player
	msg = add_player((name,_id))
	# send the response
	return jsonify({'message': msg})

# game: send answer to challenge
@app.route('/lambda/game/challenge/<_id>/<challenge>/<answer>', methods=['GET'])
def game_answers(_id, challenge, answer):
	# check the answer
	msg = check_answer((_id, challenge, answer))
	# send the response
	return jsonify({'message': msg})

# game: get settings for the page
@app.route('/lambda/game/challenge/settings', methods=['GET'])
def game_settings():
	# get the settings
	settings = generate_settings()
	# send the response
	return jsonify({'settings': settings})

# game: get the descritpion for the challenges
@app.route('/lambda/game/challenge/info/<idx>', methods=['GET'])
def challenge_descroption(idx):
	# get the description
	descritpion = get_challenge_description(int(idx))
	# return it
	return jsonify({'description': descritpion})


# game: see leaderboard




# run the app
app.run(port=8080, host="0.0.0.0", debug=True)