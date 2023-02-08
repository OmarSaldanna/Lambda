from flask import Flask, request, jsonify
from modules.controllers import * # here are all the lambda functions


# instance the flask app
app = Flask(__name__)


# discord api
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


# telegram api
@app.route('/lambda/telegram', methods=['GET'])
def telegram():
	if request.method == 'GET':
  	# extract the message
 		msg = request.headers.get('msg')
 		return 'this is a get request'


# run the app
app.run(port=8000, host="127.0.0.1", debug=True)