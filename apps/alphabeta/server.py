# libraries
from flask_cors import CORS
from flask import Flask, request, jsonify
# talk function
import modules

# instance the flask app
app = Flask(__name__)
CORS(app)

# lambda conversation
@app.route('/alphabeta', methods=['GET'])
def alphabeta():
	if request.method == 'GET':
		try:
			# extract the message from the request
			message = request.json.get('message')
			author = request.json.get('author')
			server = request.json.get('server')
			# use the fast conversation module
			if author == "alphabeta" and server == "0":
				# get the audio file
				file_path = modules.talk(message)
				# 
				return jsonify({'content': file_path})
		except Exception as e:
			print(e)
			return jsonify({'content': 'error'})

# run the app, on localhost only
app.run(port=8091, host="0.0.0.0", debug=True)