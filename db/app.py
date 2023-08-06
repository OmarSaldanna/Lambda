# libraries
import json
import asyncio
from flask_cors import CORS
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# db controllers
import controllers

# this server, won't include the try and catch, since 
# normaly databases throw error on bad requests

# load the .env variables
load_dotenv()

# instance the flask app
app = Flask(__name__)
CORS(app)


# db requests for member data: members/, images/
# example request
# {
#	"db": "members|images",
#	"id": "[id]",
#	*"data": {data}
# }
@app.route('/members', methods=['GET','PUT'])
async def members():
	# extract the message from the request
	author_id = request.headers.get('id')
	database = request.headers.get('db')
	server = request.headers.get('server')

	print(f"{request.method} -> /members -> {database} -> {author_id}")

	# get is to read data
	if request.method == 'GET':
		# get the user json
		data = controllers.get_user_data(author_id, database, server)
		# and return
		return jsonify({'answer': data})
		# put is to update data

	elif request.method == 'PUT':
		# aditional info to update
		update = json.loads(request.headers.get('data'))
		# update the user json
		data = controllers.update_user_data(author_id, database, update)
		# and return
		return jsonify({'answer': data})


# db requests for server
# example request
# {
#	"id": "[id]"
#	*"data": {data}
# }
@app.route('/servers', methods=['GET', 'PUT'])
async def servers():
	# extract the message from the request
	server_id = request.headers.get('id')
	
	print(f"{request.method} -> /servers -> {server_id}")

	# get is to read data
	if request.method == 'GET':
		# get the server json
		data = controllers.get_server_data(server_id)
		# and return
		return jsonify({'answer': data})

	# put is to update data
	if request.method == 'PUT':
		# aditional info to update
		update = json.loads(request.headers.get('data'))
		# update the user json
		data = controllers.update_server_data(server_id, update)
		# and return
		return jsonify({'answer': data})


# verbs database 
# {
#	"verb": "[verb]"
#	"data": {
#       "type": "general|multi"
# 		"object": "function name",
#		*"function": "function name"
#		...
# 	}
# }
@app.route('/verbs', methods=['GET','PUT','POST'])
async def verbs():
	# extract the message from the request
	verb = request.headers.get('verb')

	print(f"{request.method} -> /verbs -> {verb}")


	# post to add info
	if request.method == 'GET':
		# use the controller
		ans = controllers.get_verb_data(verb)
		# and return
		return jsonify({'answer': ans})

	# post to add info
	elif request.method == 'POST':
		# get the extra data
		data = json.loads(request.headers.get('data'))
		# use the controller
		ans = controllers.add_verb_data(verb, data)
		# and return
		return jsonify({'answer': ans})

	# post to add info
	elif request.method == 'PUT':
		# get the extra data
		data = json.loads(request.headers.get('data'))
		# use the controller
		ans = controllers.update_verb_data(verb, data)
		# and return
		return jsonify({'answer': ans})
		

# log requests, to save the logs only
# then only admins can read them
# {
#	"db": "bin|admins|errors|general"
#	"data": "message to add"
# }
@app.route('/logs', methods=['POST'])
async def log():
	# extract the message from the request
	database = request.headers.get('db')
	# data in this case is just a string
	data = request.headers.get('data')
	
	print(f"{request.method} -> /logs -> {database}")

	# post to add info
	if request.method == 'POST':
		# use the controller
		ans = controllers.add_to_log(database, data)
		# and return
		return jsonify({'answer': ans})


# errors requests, to save the errors only
# then only admins can read them
# {
#	"data": {
#		"call": lambda call that generated the error
# 		"code": error code
# 		"member": user id
# 		"server": server
# 	}
# }
@app.route('/errors', methods=['POST'])
async def errors():
	# extract the message from the request
	data = json.loads(request.headers.get('data'))
	
	# print(f"{request.method} -> /members -> {author_id}")

	# post to add info
	if request.method == 'POST':
		# use the controller
		ans = controllers.add_to_errors(data)
		# and return
		return jsonify({'answer': ans})

dev = True if os.getenv("dev") == 'yes' else False

# run the app, on localhost only
app.run(port=8081, host="127.0.0.1", debug=dev)