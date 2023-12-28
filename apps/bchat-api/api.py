import json
import socket
import asyncio
import os
from flask_cors import CORS
from flask import Flask, request, jsonify


# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the bchat-server
client_socket.connect(("127.0.0.1", 31416))
# once connected, send the name
# the format is ~name
client_socket.send('+lambda'.encode())

# now the flask app
app = Flask(__name__)
CORS(app)

# function to struct the message, returns a string
# message= id~data
def struct_message(data: dict):
    # the message will start with the user id
    message = '-' + data['from'] + '-' + data['to'] + '-' + json.dumps(data)
    return message

# function to encrypt the message, returns a string
def encrypt_message(message: str):
    return message

# data: {
#   type: input or output
#   alias: device alias,
#   value: info,
# }
# sample {"from": "lambda", "to": "717071120175595631", "type": "output", "alias": "led rojo", "value": "255"}
@app.route('/bchat', methods=['POST'])
async def bchat():
    # get the json content
    data = request.json
    # post to add info
    if request.method == 'POST':
        # then struct the message
        message = struct_message(data)
        # encrypt the message
        message = encrypt_message(message)
        # send it
        client_socket.send(message.encode())
        # and return something
        return jsonify({'answer': 'ok'})


# detect dev mode
dev = True if os.getenv("dev") == 'yes' else False
# run the app, on localhost only
app.run(port=8092, host="127.0.0.1", debug=dev)