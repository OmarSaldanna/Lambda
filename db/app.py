# libraries
import os
import json
import asyncio
from flask_cors import CORS
from flask import Flask, request, jsonify

# db controllers
import controllers
from modules import telegram_message

# detect dev mode
dev = True if os.getenv("dev") == 'yes' else False

# This DB server, won't include the try and catch,
# since normaly databases throw error on bad requests

# instance the flask app
app = Flask(__name__)
CORS(app)

# requests for member data:
# {
#	"id": "[user id]",
#   *"server": "[server name]" *only for GET requests
#	*"data": "{data}" *only for PUT requests
# }
# Note: the server ins't receipt in PUT requests since those requests
# are made by the Lambda modules, after the GET requests.
@app.route('/members', methods=['GET','PUT'])
async def members():
	# get the json content
	data = request.json
	# extract the message from the request
	user = data.get('id')

	if dev:
		print(f"{request.method} -> /members -> {user}")

	# get is to read data
	if request.method == 'GET':
		# aditional: the server name
		server = data.get('server')
		# get the user json
		data = controllers.get_user_data(user, server)
		# and return
		return jsonify({'answer': data})
	
	# put is to update data
	elif request.method == 'PUT':
		# aditional info to update
		# update = json.loads(data.get('data'))
		update = eval(data.get('data')) # this one supports ' and \"
		# update the user json
		data = controllers.update_user_data(user, update)
		# and return
		return jsonify({'answer': data})


# requests for server
# {
#	"id": "[id]",
#   *"server": "[name]" *only for GET requests
#	*"data": {data} *only for PUT requests
# }
@app.route('/servers', methods=['GET', 'PUT'])
async def servers():
	# get the json content
	data = request.json
	# extract the message from the request
	server_id = data.get('id')
	
	if dev:
		print(f"{request.method} -> /servers -> {server_id}")

	# get is to read data
	if request.method == 'GET':
		# aditional: the server name
		server_name = data.get('name')
		# get the server json
		data = controllers.get_server_data(server_id, server_name)
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


# requests for images
# {
#	"id": "[image hash]",
#   "url": "[public url]",
#   "prompt": "[image prompt]"
# }
@app.route('/images', methods=['POST'])
async def images():
	# get the json content
	data = request.json
	
	if dev:
		print(f"{request.method} -> /images")

	# post is to create data	
	if request.method == 'POST':
		# get the image data
		image_hash = data.get('id')
		image_url = data.get('url')
		image_prompt = data.get('prompt')
		# use the controller
		ans = controllers.post_image(image_hash, image_url, image_prompt)
		# and return
		return jsonify({'answer': ans})


# put, delete and patch have special cases
@app.route('/verbs', methods=['GET','POST','DELETE','PATCH'])
async def verbs():
	# get the json content
	data = request.json

	# reads verb data, mostly used by Lambda's brain
	# {
	# 	"verb": "[verb]"
	# }
	if request.method == 'GET':
		# get the verb from the request
		verb = data.get('verb')
		# use the controller
		ans = controllers.get_verb_data(verb)
		# and return
		return jsonify({'answer': ans})

	# writes or overwrites verb data based on the create or elimination
	# elimination of lambda skills
	# {
	#	"skill": "[name of the skill]",
	#	"words": [words...],
	#	"verbs": [verbs...],
	#   "lock": "[literally something]"
	# }
	elif request.method == 'POST':
		# get the skill name
		skill = data.get('skill')
		# and the word and verb lists
		word_list = eval(data.get('words'))
		verbs = eval(data.get('verbs'))
		# extra parameter, makes able to create new verbs
		newverb_lock = True if data.get('lock') else False
		# use the controller
		ans = controllers.post_verb_data(skill, word_list, verbs, newverb_lock)
		# and return
		return jsonify({'answer': ans})

	# removes all the information related to a lambda skill
	# {
	# 	"skill": "[name of the skill]"
	# }
	elif request.method == 'DELETE':
		# get the extra data
		skill = data.get('skill')
		# use the controller
		ans = controllers.delete_verb_data(skill)
		# and return
		return jsonify({'answer': ans})
	
	# PATCH is a special function that has searching uses:
	# * see what verbs has a word or a function [word, function]
	# {
	#	"search": "[word|function]",
	#	"value": "[that word or function]"
	# }
	# * see with what words and verbs is asociated a function [skill]
	# {
	#	"search": "skill",
	#	"value": "[skill name]"
	# }
	elif request.method == 'PATCH':
		# catch the params
		search = data.get("search")
		value = data.get("value")
		# use the controller
		ans = controllers.patch_verb_data(search, value)
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
	
	if dev:
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
	# data = json.loads(data.get('data'))
	data = eval(data.get('data'))
	
	if dev:
		print(f"{request.method} -> /errors -> {data['member']}")

	# post to add info
	if request.method == 'POST':
		# use the controller
		ans, error_hash = controllers.add_to_errors(data)
		# use telegram bot to notify
		# removed due to security problems
		# telegram_message(f"Error on: {data['call']}")
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
		userlist = eval(request.json.get('userlist'))
		# use the controller
		ans = controllers.patch_users(userlist)
		# and return the answer
		return jsonify({"answer": 'ok'})


# it only receives a {"content": "..."} 
# exceptional API to send alerts of errors on DB
# used in daily script that restores the usages
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


# run the app, on localhost only
app.run(port=31417, host="127.0.0.1", debug=dev)