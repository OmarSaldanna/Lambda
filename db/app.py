# libraries
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
# functions from memory
# from core.memory import get_memory, app_to_log
# controllers
import controllers

# this server, won't include the try and catch, since 
# normaly databases throw error on bad requests


# instance the flask app
app = Flask(__name__)
CORS(app)

# db requests for member data: members/, images/
# example request
# {
#	"type": "get|put",
#	"db": "members|images",
#	"id": "[id]"
#	*"data": {data}
# }
@app.route('/db/members', methods=['GET','PUT'])
def members():
	# extract the message from the request
	author_id = request.headers.get('id')
	database = request.headers.get('db')
	
	if request.method == 'GET':
		# get the user json
		data = controllers.get_user_data(author_id, database)
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
#	"type": "get|put",
#	"id": "[id]"
#	*"data": {data}
# }
@app.route('/db/servers', methods=['GET'])
def servers():
	if request.method == 'GET':
		# extract the message from the request
		req_type = request.headers.get('type')
		server_id = request.headers.get('id')

		# get is to return data
		if req_type == "get":
			# get the server json
			data = controllers.get_server_data(server_id)
			# and return
			return jsonify({'answer': data})
		# put is to update data
		elif req_type == "put":
			# aditional info to update
			update = request.headers.get('data')
			# update the user json
			data = controllers.update_server_data(server_id, update)
			# and return
			return jsonify({'answer': data})
		# method unknown
		else:
			return jsonify({'answer': f'Request type error: {req_type}'})

# log requests, to save the logs only
# then only admins can read them
# {
#	"type": "post",
#	"db": "bin|admins|errors|general"
#	"data": "message to add"
# }
@app.route('/db/log', methods=['GET'])
def log():
	if request.method == 'GET':
		# extract the message from the request
		req_type = request.headers.get('type')
		database = request.headers.get('db')
		data = request.headers.get('data')

		# save to log
		if req_type == "post":
			# use the controller
			data = controllers.add_to_log(database, data)
			# and return
			return jsonify({'answer': data})

		# method unknown
		else:
			return jsonify({'answer': f'Request type error: {req_type}'})

# errors requests, to save the errors only
# then only admins can read them
# {
#	"type": "post",
#	"data": "message to add"
# }
@app.route('/db/log', methods=['GET'])
def errors():
	if request.method == 'GET':
		# extract the message from the request
		req_type = request.headers.get('type')
		data = request.headers.get('db')

		# save to log
		if req_type == "post":
			# use the controller
			data = controllers.handle_log(database, data)
			# and return
			return jsonify({'answer': data})

		# method unknown
		else:
			return jsonify({'answer': f'Request type error: {req_type}'})

# run the app, on localhost only
app.run(port=8083, host="127.0.0.1", debug=True)