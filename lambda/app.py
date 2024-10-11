# libraries
import os
import asyncio
# flask stuff
from flask_cors import CORS
from flask import Flask, request, jsonify
# the lambda brain
from core.brain import Brain
from modules.ai import AI
# and the security module
from auth import Auth


# instance the flask app
app = Flask(__name__)
CORS(app)
# detect dev mode
dev = True if os.getenv("dev") == 'yes' else False
# the Lambda's Brain
brain = Brain()
# the security module
secure = Auth()
# Default error answer for chat functions
api_key_err = { "type": "error", "content": os.environ["BAD_API_KEY_ERROR"] }


# Lambda requests: special functions
@app.route('/', methods=['GET'])
async def lambda_special():
	# get the json content of the request
	data = request.json
	if request.method == 'GET':
		# extract the message from the request
		message = data.get('message')
		author = data.get('author')
		server = data.get('server')
		api_key = data.get('api_key')
		# verify null params
		# if secure.has_nulls([message, author, server, api_key])
			# return {}
		# check the api key
		if secure.look_for(api_key, user_id):
			# process the message
			answer = brain(message, author, server)
			# and send the anser
			return jsonify({'answer': answer})
		# there were an error in the api key
		else:
			return jsonify({'answer': api_key_err})


# Lambda requests: for chat
# {
# 	"message": "¿Cuál es la capital de Perú?",
# 	"server": "web | api"
# }
@app.route('/chat', methods=['GET'])
async def lambda_simple():
	# get the json content of the request
	data = request.json
	# the headers for the auth
	api_key = request.headers["x-api-key"]

	if request.method == 'GET':
		# extract the message from the request
		message = data.get('message')
		server = data.get('server')
		# check null params
		if secure.has_nulls([api_key, message, server]):
			return jsonify({'answer': os.environ["BAD_REQUEST_ERROR"]})

		# look for the user api_key and the user id
		found_user_id = secure.look_for(api_key)
		if found_user_id:
			# instance the AI
			ai = AI(found_user_id, server)
			# use the chat on the default mode
			answer = ai({ "text": message }, "chat")
			# and send the answer
			return jsonify({'answer': answer['content']})
		# there were an error in the api key
		else:
			return jsonify({'answer': api_key_err})


# Security requests: token actions
@app.route('/auth', methods=['POST','PUT'])
async def lambda_security():
	# get the json content of the request
	data = request.json
	# the headers for the auth
	server_api_key = request.headers["x-api-key"]
	user_id = request.headers["user-id"]
	# check for null params
	if secure.has_nulls([server_api_key, user_id]):
		return jsonify({'answer': os.environ["BAD_REQUEST_ERROR"]})

	# POST is for generating tokens for users
	if request.method == 'POST':
		# use the secure module to generate the new key
		answer = secure.new_api_key(user_id, server_api_key)
		# finally return the false or the api key
		# the client will handle the key or show the error
		return jsonify({'answer': answer})

	# PUT is for reload the users' usage credits
	if request.method == 'PUT':
		# extract the data from the request
		credits = int(data.get('credits'))
		# also check the credits to not be null
		if secure.has_nulls([credits]):
			return jsonify({'answer': os.environ["BAD_REQUEST_ERROR"]})

		# verify the server_api_key
		if server_api_key == os.environ["LAMBDA_API_KEY"]:
			# update the user usage through ai module
			ai = AI(user_id, "billing") # this mode is symbolic
			# change
			ai.user_data["usage"]["budget"] += credits
			ai.user_data["usage"]["images"] += credits * int(os.environ["IMAGES_PER_CREDIT"])
			# save changes
			ai.db.put('/members', {
				"id": user_id,
				"data": {
					"usage": ai.user_data["usage"],
				}
			})
			return jsonify({'answer': True})
		# bad api key
		else:
			return jsonify({'answer': False})


# Starting requests: get user data
@app.route('/start', methods=['GET'])
async def lambda_start():
	# the headers for the auth
	api_key = request.headers["x-api-key"]

	if request.method == 'GET':
		# check null params
		if secure.has_nulls([api_key]):
			return jsonify({'answer': os.environ["BAD_REQUEST_ERROR"]})

		# look for the user api_key and the user id
		found_user_id = secure.look_for(api_key)
		if found_user_id:
			# instance the AI
			ai = AI(found_user_id, "chat")
			# and return the user data
			return jsonify({'answer': ai.user_data})
		# in case of a bad api key
		else:
			return jsonify({'answer': os.environ["BAD_API_KEY_ERROR"]})


# run the app, on localhost only
app.run(port=int(os.environ["LAMBDA_PORT"]), host=os.environ["LAMBDA_HOST"], debug=dev)