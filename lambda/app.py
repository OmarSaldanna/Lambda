# libraries
from flask_cors import CORS
from flask import Flask, request, jsonify
# functions from files
from core.memory import get_memory, app_to_log
# the lambda brain
from core.brain import AI
# the function dic to instance lambda AI
from core.body import function_dic

# load the port and the host
info = get_memory('info')
port = info['host']['lambda_port']
host = info['host']['lambda_ip']

# instance the flask app
app = Flask(__name__)
CORS(app)

# and the lambda AI
ai = AI(function_dic)

# lambda requests
@app.route('/lambda', methods=['GET'])
def discordo():
	if request.method == 'GET':
		# extract the message from the request
		message = request.headers.get('message')
		author = request.headers.get('author')
		# process the message
		answer = ai(message, author)
		# add a log
		app_to_log(f'[LAMBDA] -> request from: {author}')
		# and send the anser
		return jsonify({'content': [answer]})


# run the app, on localhost only
app.run(port=port, host=host, debug=True)