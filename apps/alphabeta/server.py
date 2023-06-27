# libraries
from flask_cors import CORS
from flask import Flask, request, jsonify
# talk function
import modules

# instance the flask app
alphabeta = Flask(__name__)
CORS(alphabeta)

# lambda conversation
@alphabeta.route('/lambda/alphabeta', methods=['GET'])
def lambda_conversation():
	if request.method == 'GET':
		try:
			# extract the message from the request
			message = request.headers.get('message')
			author = request.headers.get('author')
			# use the talk
			if author == "717071120175595631":
				# get the audio file
				file_path = modules.talk(message)
				# 
				return jsonify({'content': file_path})
		except:
			return jsonify({'content': 'error'})

# run the app, on localhost only
alphabeta.run(port=88, host="0.0.0.0", debug=True)