# libraries
import os
import json
import asyncio
# flask stuff
from flask_cors import CORS
from flask import Flask, request, jsonify
# the lambda brain
from core.brain import Brain
from modules.ai import AI
# the file functions
from modules import files
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


# simple function used to parse errors
def err (error_env):
	return { "type": "error", "content": os.environ[error_env]}


# Lambda requests: special functions
# {
# 	"server": "web | api",
# 	"message": {
# 		"text": "promt to process"
# 		"files": [filenames to use or empty]
# 	}
# }
@app.route('/', methods=['GET'])
async def lambda_special ():
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
			return jsonify(err("MISSING_PARAMS_ERROR"))

		# look for the user api_key and the user id
		found_user_id = secure.look_for(api_key)
		if found_user_id:
			# process the message
			answer = brain(message, found_user_id, server)
			# and send the anser
			return jsonify(answer)
		# there were an error in the api key
		else:
			return jsonify(err("BAD_API_KEY_ERROR"))


# Lambda requests: for chat, also admits images
# {
# 	"prompt": {"text": "promt text"},
# 	"server": "web | api"
# }
########################################################
# {
# 	"prompt": {"image": ["image encoded in base64", "prompt"]},
# 	"server": "web | api"
# }
@app.route('/chat', methods=['GET'])
async def lambda_simple ():
	# get the json content of the request
	data = request.json
	# the headers for the auth
	try:
		server_api_key = request.headers["x-api-key"]
	except:
		return jsonify(err("BAD_REQUEST_ERROR"))

	if request.method == 'GET':
		# extract the message from the request
		message = data.get('prompt')
		server = data.get('server')
		# check null params
		if secure.has_nulls([server_api_key, message, server]):
			return jsonify(err("MISSING_PARAMS_ERROR"))

		# look for the user api_key and the user id
		found_user_id = secure.look_for(server_api_key)
		if found_user_id:
			# instance the AI
			ai = AI(found_user_id, server)
			# use the chat on the default mode
			try:
				answer = ai(message, "chat")
			except:
				return jsonify(err("CHAT_PROCESSING_ERROR"))
			# and send the answer
			return jsonify(answer)
		# there were an error in the api key
		else:
			return jsonify(err("BAD_API_KEY_ERROR"))


# Security requests: token actions
# NOTE: THESE ONE RECEIVES THE LAMBDA SERVER API KEY
@app.route('/auth', methods=['POST','PUT'])
async def lambda_security ():
	# get the json content of the request
	data = request.json
	# the headers for the auth
	try:
		server_api_key = request.headers["x-api-key"]
	except:
		return jsonify(err("BAD_REQUEST_ERROR"))

	user_id = data.get('id')
	# check for null params
	if secure.has_nulls([server_api_key, user_id]):
		return jsonify(err("MISSING_PARAMS_ERROR"))

	# POST is for generating tokens for users
	elif request.method == 'POST':
		# use the secure module to generate the new key
		answer = secure.new_api_key(user_id, server_api_key)
		# finally return the false or the api key
		# the client will handle the key or show the error
		# in case of an error
		if not answer:
			answer = err("BAD_API_KEY_ERROR")
		# format the answer
		else:
			answer = { "type": "info", "content": answer}
		return jsonify(answer)

	# PUT is for reload the users' usage credits
	# {
	# 	"credits": number of paid credits
	# }
	elif request.method == 'PUT':
		# extract the data from the request
		credits = data.get('credits')
		# also check the credits to not be null
		if secure.has_nulls([credits]):
			return jsonify(err("MISSING_PARAMS_ERROR"))

		# verify the server_api_key
		if server_api_key == os.environ["LAMBDA_API_KEY"]:
			# convert credits to int
			credits = int(credits)
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
			return jsonify({'content': True, "type": "info"})
		# bad api key
		else:
			return jsonify(err("BAD_API_KEY_ERROR"))


# Starting requests: get user data
@app.route('/start', methods=['GET'])
async def lambda_start ():
	# the headers for the auth
	try:
		server_api_key = request.headers["x-api-key"]
	except:
		return jsonify(err("BAD_REQUEST_ERROR"))

	if request.method == 'GET':
		# check null params
		if secure.has_nulls([api_key]):
			return jsonify(err("BAD_REQUEST_ERROR"))

		# look for the user api_key and the user id
		found_user_id = secure.look_for(api_key)
		if found_user_id:
			# instance the AI
			ai = AI(found_user_id, "chat")
			# and return the user data
			return jsonify({"content": ai.user_data, "type": "info"})
		# in case of a bad api key
		else:
			return jsonify(err("BAD_API_KEY_ERROR"))


# File requests: process files and append them to context
# Images: png, jpeg, jpg, webp
# Documents: pdf, docx, pptx, txt
# Audios: mp3, ogg, wav
# Code files: js, sh, py, html, php, c, ino, json
# Data files: csv, xlsx, data (like a txt)

# File flow ###################
# 1 - Endoded and upload in a post request (frontend):
# {
#	"name": name of the file
#	"ext": extension of the file
#	"type": image, document, audio, code, data
#	"content": endoced file data in base64
# }
# 
# 2 - Received and stored in lambdrive/{type}/{some hash}.{ext}
# 
# 3 - Saved in the user file db
#
# GET: returns the list of available files
# POST: upload files and returns the new list
# DELETE: delete files
@app.route('/drive', methods=['GET','POST','DELETE'])
async def lambda_drive ():
	# the headers for the auth
	try:
		server_api_key = request.headers["x-api-key"]
	except:
		return jsonify(err("BAD_REQUEST_ERROR"))

	# check null params
	if secure.has_nulls([api_key]):
		return jsonify({'answer': err("BAD_REQUEST_ERROR")})
	# look for the user api_key and the user id
	found_user_id = secure.look_for(api_key)
	# if the id was not found
	if not found_user_id:
		return jsonify({'answer': err("BAD_API_KEY_ERROR")})

	############################ Process the request #################
	
	# retrieve the user file list
	if request.method == 'GET':
		# retrieve all the files from the db
		# instance ai and use the db module
		ai = AI(found_user_id, "files") # this mode is symbolic
		# use the db
		found_files = ai.db.get("/files", {
			"id": found_user_id
		})["answer"]
		# return the found files
		return jsonify({"content": found_files, "type": "info"})

	# save a new file
	# {
	# 	"type": "folder to save the file",
	#   "name": "name of the file",
	# 	"content": "base64 file"
	# }
	elif request.method == 'POST':
		# get the json content of the request
		data = request.json 
		# get the data
		file_type = data.get('type')
		file_name = data.get('name')
		file_content = data.get('content')
		# check nulls
		if secure.has_nulls([file_type, file_name, file_content]):
			return jsonify(err("MISSING_PARAMS_ERROR"))
		# check the filename
		if not secure.secure_filename(file_name):
			return jsonify(err("BAD_FILE_ERROR"))

		# if no nulls, then save the file
		try:
		# save the new file on db
			ai = AI(found_user_id, "files") # this mode is symbolic
			# use the db
			found_files = ai.db.post("/files", {
				"id": found_user_id,
				"filename": f"lambdrive/{found_user_id}/{file_type}/{file_name}"
			})["answer"]
			# save it on storage
			files.base64_to_file(file_content, f"lambdrive/{found_user_id}/{file_type}/{file_name}")
			# return the found files
			return jsonify({"type": "info", "content": found_files})
		# if there was an error
		except:
			return jsonify(err("FILE_SAVING_ERROR"))

	# delete a file
	# NOTE: FOR SECURITY AND LAMBDA INTEGRITY REASONS, THE FILES ARE GOING
	# TO BE DELETED ONLY IN DB LIST
	# 
	# {
	#   "name": "name of the file"
	# }
	elif request.method == 'DELETE':
		# get the json content of the request
		data = request.json
		# get the data
		file_name = data.get('name')
		# check nulls
		if secure.has_nulls([file_name]):
			return jsonify(err("MISSING_PARAMS_ERROR"))
		# check the filename
		if not secure.secure_filename(file_name):
			return jsonify(err("BAD_FILE_ERROR"))

		# delete the file from db
		ai = AI(found_user_id, "files") # this mode is symbolic
		# use the db
		found_files = ai.db.delete("/files", {
			"id": found_user_id,
			# note: delete requests only requires 
			"filename": f"{file_name}"
		})["answer"]
		# return the found files
		return jsonify({"type": "info", "content": found_files})


# run the app, on localhost only
app.run(port=int(os.environ["LAMBDA_PORT"]), host=os.environ["LAMBDA_HOST"], debug=dev)