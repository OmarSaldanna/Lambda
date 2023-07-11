# libraries
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
# db controllers
import controllers

# this server, won't include the try and catch, since 
# normaly databases throw error on bad requests

# instance the flask app
app = Flask(__name__)
CORS(app)


# db requests for member data: members/, images/
# example request
# {
#	"db": "members|images",
#	"id": "[id]"
#	*"data": {data}
# }
@app.route('/db/members', methods=['GET','PUT'])
def members():
	# extract the message from the request
	author_id = request.headers.get('id')
	database = request.headers.get('db')

	# get is to read data
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
#	"id": "[id]"
#	*"data": {data}
# }
@app.route('/db/servers', methods=['GET', 'PUT'])
def servers():
	# extract the message from the request
	server_id = request.headers.get('id')

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
# 		"object": "function name",
#		...
# 	}
# }
@app.route('/db/verbs', methods=['GET','PUT','POST'])
def verbs():
	# extract the message from the request
	verb = request.headers.get('verb')

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
@app.route('/db/logs', methods=['POST'])
def log():
	# extract the message from the request
	database = request.headers.get('db')
	# data in this case is just a string
	data = request.headers.get('data')
	
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
# 		"user": user id
# 		"server": server
# 	}
# }
@app.route('/db/errors', methods=['POST'])
def errors():
	# extract the message from the request
	data = json.loads(request.headers.get('data'))
	
	# post to add info
	if request.method == 'POST':
		# use the controller
		ans = controllers.add_to_errors(data)
		# and return
		return jsonify({'answer': ans})


# run the app, on localhost only
app.run(port=8083, host="127.0.0.1", debug=True)