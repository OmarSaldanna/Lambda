from flask_cors import CORS
from flask import Flask, request, jsonify
from modules.controllers import * # here are all the lambda functions
from modules.memory import get_memory, app_to_log


# load the port and the host
info = get_memory('info')
port = info['HOST']['lambda_port']
host = info['HOST']['lambda_ip']


# instance the flask app
app = Flask(__name__)
CORS(app)

# to use gpt3
@app.route('/lambda/discordo/gpt', methods=['GET'])
def discordo():
	if request.method == 'GET':
		# extract the message from the request
		msg = request.headers.get('msg')
		author = request.headers.get('author')
		# process the message
		ans = discord_gpt(msg)
		# add a log
		app_to_log(f'[LAMBDA] -> request on /lambda/discordo/gpt by: {author}')
		# and send the anser
		return jsonify({'answer': ans})


# to use DALL-E
@app.route('/lambda/discordo/dalle', methods=['GET'])
def discordo_commands():
	if request.method == 'GET':
  		# extract the message from the request
		msg = request.headers.get('msg')
		author = request.headers.get('author')
		# process the message
		ans = discord_dalle(msg)
		# add a log
		app_to_log(f'[LAMBDA] -> request on /lambda/discordo/dalle by: {author}')
		# and send the anser
		return jsonify({'answer': ans})



# run the app, on localhost only
app.run(port=port, host=host, debug=True)