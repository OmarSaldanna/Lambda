# libraries
import os
import json
import asyncio

# flask stuff
from flask_cors import CORS
from flask import Flask, request, jsonify

# the Lambda Brain and AI
from core.brain import Brain
from core.ai import AI


# instance the flask app
app = Flask(__name__)
CORS(app)
# detect dev mode
dev = True if os.getenv("dev") == 'yes' else False
# the Lambda's Brain
brain = Brain()

# simple function used to parse errors
def err (error_env):
	return { "type": "error", "content": os.environ[error_env]}


# Lambda requests: special functions
# {
#   "user": "user id",
# 	"server": "web | api",
# 	"prompt": "promt to process"
# }
@app.route('/', methods=['GET'])
async def lambda_special ():
	# get the json content of the request
	data = request.json
	# 
	if request.method == 'GET':
		# extract the message from the request
		message = data.get('prompt')
		server = data.get('server')
		user_id = data.get('user')
		# check params
		if None in [message, server, user_id] or "" in [message, server, user_id]:
			return jsonify(err("MISSING_PARAMS_ERROR"))
		# then
		# process the message
		answer = brain(message, user_id, server)
		# and send the anser
		return jsonify(answer)


# Lambda requests: for chat, also admits images
# {
#   "user": "user id",
# 	"prompt": {"text": "promt text"},
# 	"server": "web | api"
# }
########################################################
# {
#   "user": "user id",
# 	"prompt": {"image": ["image encoded in base64", "prompt"]},
# 	"server": "web | api"
# }
@app.route('/chat', methods=['GET'])
async def lambda_simple ():
	# get the json content of the request
	data = request.json

	if request.method == 'GET':
		# extract the message from the request
		message = data.get('prompt')
		server = data.get('server')
		user_id = data.get('user')
		# check params
		if None in [message, server, user_id] or "" in [message, server, user_id]:
			return jsonify(err("MISSING_PARAMS_ERROR"))
		# else: run the prompt
		# instance the AI
		ai = AI(user_id, server)
		# use the chat on the default mode
		# try:
		return jsonify(ai(message, "chat"))
		# except:
			# return jsonify(err("CHAT_PROCESSING_ERROR"))


# run the app, on localhost only
app.run(port=int(os.environ["LAMBDA_PORT"]), host=os.environ["LAMBDA_HOST"], debug=dev)