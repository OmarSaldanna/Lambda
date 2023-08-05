# libraries
from flask_cors import CORS
import asyncio
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
	if request.method == 'GET':
		# extract the message from the request
		message = request.headers.get('message')
		author = request.headers.get('author')
		server = request.headers.get('server')
		# process the message
		answer = ai(message, author, server)
		# and send the anser
		return jsonify({'content': answer})


# lambda requests for fast usage
@app.route('/lambda/chat', methods=['GET'])
async def lambda_conversation():
	if request.method == 'GET':
		# extract the message from the request
		message = request.headers.get('message')
		author = request.headers.get('author')
		server = request.headers.get('server')
		# process the message
		answer = ai.chat(message, author, server)
		# and send the answer
		return jsonify({'content': answer})


# run the app, on localhost only
app.run(port=8080, host="127.0.0.1", debug=True)