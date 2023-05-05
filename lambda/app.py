from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.controllers import * # here are all the lambda functions
from modules.memory import get_memory, app_to_log


# load the port and the host
info = get_memory('info')
port = info['HOST']['lambda_port']
host = info['HOST']['lambda_ip']
# add the initial message to the logs
# app_to_log(f"[LAMBDA] -> lambda server running in {host}:{port}/lambda\n")


# instance the flask app
app = Flask(__name__)
CORS(app)

# to use gpt3
@app.route('/lambda/discordo/gpt', methods=['GET'])
def discordo():
	if request.method == 'GET':
		# extract the message from the request
		msg = request.headers.get('msg')
		# process the message
		ans, log = discord_gpt(msg)
		# add the usage to the log file
		message = f'[LAMBDA] -> request on /lambda/discordo/gpt'
		# answer = f'\n[LAMBDA] -> Sending Answer:\n{ans}\n\n'
		app_to_log(f'{message}')
		# and send the anser
		return jsonify({'answer': ans})


# discord api for specific commands
@app.route('/lambda/discordo/commands', methods=['GET'])
def discordo_commands():
	if request.method == 'GET':
  	# extract the message
 		msg = request.headers.get('msg')
 		# process the message
 		ans = discord_comm(msg)
 		# and send the anser
 		return jsonify({'answer': ans})


# run the app, on localhost only
app.run(port=port, host=host, debug=True)