import os
os.system('clear')
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.controllers import * # here are all the lambda functions


# load the keys, ports and tokens
info = json.load(open('./info.json'))
lambda_api_port = info['HOST']['lambda_port']
lambda_api = info['HOST']['lambda_ip']
print(f"[SERVER] -> lambda server running in {lambda_api}:{lambda_api_port}/lambda")


# instance the flask app
app = Flask(__name__)
CORS(app)

# discord api for general commands
# lambda how many chapters has steins;gate?
# lambda turn on the light 1
# lambda pon hikaru-nara
@app.route('/lambda/discordo', methods=['GET'])
def discordo():
	if request.method == 'GET':
		# extract the message
		msg = request.headers.get('msg')
		print(f'\n[SERVER] -> /lambda/discordo: \n {msg}')
		# process the message
		ans = discord_msg(msg)
		# and send the anser
		print(f'[SERVER] -> Sending Answer: \n ans')
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




# run the app
app.run(port=lambda_api_port, host="0.0.0.0", debug=True)