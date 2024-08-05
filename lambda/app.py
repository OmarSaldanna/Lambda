# libraries
import os
import asyncio
# flask stuff
from flask_cors import CORS
from flask import Flask, request, jsonify
# the lambda brain
from core.brain import AI

# instance the flask app
app = Flask(__name__)
CORS(app)

# and the lambda AI
ai = AI()

# lambda requests for general usage
@app.route('/lambda', methods=['GET'])
async def lambda_call():
	# get the json content of the request
	data = request.json
	if request.method == 'GET':
		# extract the message from the request
		message = data.get('message')
		author = data.get('author')
		server = data.get('server')
		# process the message
		answer = ai(message, author, server)
		# and send the anser
		return jsonify({'answer': answer})


# lambda requests for chat
@app.route('/lambda/chat', methods=['GET'])
async def lambda_conversation():
	# get the json content of the request
	data = request.json
	if request.method == 'GET':
		# extract the message from the request
		message = data.get('message')
		author = data.get('author')
		server = data.get('server')
		# process the message
		answer = ai.chat(message, author, server)
		# and send the answer
		return jsonify({'answer': answer})


# lambda requests for fast usage
# this one doesn't save context
@app.route('/lambda/fast', methods=['GET'])
async def lambda_fast():
	# get the json content of the request
	data = request.json
	if request.method == 'GET':
		# extract the message from the request
		message = data.get('message')
		author = data.get('author')
		server = data.get('server')
		# process the message
		answer = ai.fast(message, author, server)
		# and send the answer
		return jsonify({'answer': answer})


# set the dev mode based on the .env variable
dev = True if os.getenv("dev") == 'yes' else False
# run the app, on localhost only
app.run(port=31416, host="127.0.0.1", debug=dev)