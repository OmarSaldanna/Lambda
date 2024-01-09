# libraries
import os
import json
import asyncio
from flask_cors import CORS
from flask import Flask, request, jsonify

# db controllers
import controllers
from modules import telegram_message

# this server, won't include the try and catch, since 
# normaly databases throw error on bad requests

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
	# get the json content
	data = request.json
	# extract the message from the request
	author_id = data.get('id')
	database = data.get('db')
	server = data.get('server')

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
		update = json.loads(data.get('data'))
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
	# get the json content
	data = request.json
	# extract the message from the request
	server_id = data.get('id')
	
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
		update = json.loads(data.get('data'))
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
	# get the json content
	data = request.json
	# extract the message from the request
	verb = data.get('verb')

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
		data = json.loads(data.get('data'))
		# use the controller
		ans = controllers.add_verb_data(verb, data)
		# and return
		return jsonify({'answer': ans})

	# post to add info
	elif request.method == 'PUT':
		# get the extra data
		data = json.loads(data.get('data'))
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
	# get the json content
	data = request.json
	# extract the message from the request
	database = data.get('db')
	# data in this case is just a string
	data = data.get('data')
	
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
	# get the json content
	data = request.json
	# extract the message from the request
	data = json.loads(data.get('data'))
	
	# print(f"{request.method} -> /members -> {author_id}")

	# post to add info
	if request.method == 'POST':
		# use the controller
		ans, error_hash = controllers.add_to_errors(data)
		# use telegram bot to notify
		telegram_message(f"Error on: {data['call']}")
		telegram_message(f"Error id: {error_hash}")
		telegram_message(f"Error: {data['code']}")
		# and return
		return jsonify({'answer': ans})


# db requests for member data: userlist
# example request
# {
#	"users": [user ids]
#   "role": "{role}"
# }
@app.route('/userlist', methods=['GET','POST','PUT', 'PATCH'])
async def userlist():	
	# get is to read data
	if request.method == 'GET':
		# use the controller
		ans = controllers.get_userlist()
		# and return the answer
		return jsonify({"answer": ans})

	# USED TO COUNT -1 IN ALL THE USERS DAYS LEFT
	# ALSO RETURNS ALL THE ROLES
	elif request.method == 'PUT':
		# use the controller
		ans = controllers.put_userlist()
		# and return the answer
		return jsonify({"answer": ans})

	# USED TO ADD A LIST OF USERS TO A ROLE
	elif request.method == 'POST':
		# load the users from the message
		role = request.json.get('role')
		users = request.json.get('users')
		# use the controller
		ans = controllers.post_users(role, users)
		# and return the answer
		return jsonify({"answer": ans})

	# USED TO RESTORE THE USAGES OF SELECTED USERS
	# {"role": [users], "role2": [users]}
	elif request.method == 'PATCH':
		# load the userlist reveipt
		userlist = json.loads(request.json.get('userlist'))
		# use the controller
		ans = controllers.patch_users(userlist)
		# and return the answer
		return jsonify({"answer": 'ok'})


# it only receives a {"content": "..."} 
# exceptional API to send alerts of errors on DB
@app.route('/alerts', methods=['POST'])
async def alerts():	
	# 
	if request.method == 'POST':
		# load the content of the alert
		content = request.json.get('content')
		# use the controller
		ans = controllers.telegram_alert(content)
		# and return the answer
		return jsonify({"answer": ans})


# detect dev mode
dev = True if os.getenv("dev") == 'yes' else False
# run the app, on localhost only
app.run(port=8081, host="127.0.0.1", debug=dev)