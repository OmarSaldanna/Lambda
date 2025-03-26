# modules
from core.lwr import Lambda_Word_Recognizer as LWR
# and libraries
import requests
import time
import os


# Lambda prende el ...
# Lambda activa el ...
# Lambda enciende el ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# get the device alias
	alias = message.split(' ')[2:]
	alias = ' '.join(alias)

	# recognize the alias among all the registered devices
	# first read the user data
	user_devices = requests.get("http://127.0.0.1:8081/members", json={
		"id": author,
		"db": "members"
	}).json()["answer"]["devices"]
	# train a lwr with the devices
	dev_recognizer = LWR()
	dev_recognizer.train(list(user_devices.keys()))
	# and recognize the alias
	alias = dev_recognizer(alias)

	# set the message content
	message_content = {
		"from": "lambda", "to": author, "type": "output",
		"alias": alias, "value": "255"
	}

	# send it to the lambda bchat api
	requests.post(
		'http://127.0.0.1:8092/bchat',
		json=message_content
	)
	# wait some time
	time.sleep(3)
	# set the initial answer
	answer = "Ups, algo salió mal"
	# read the last five receipts
	receipts = os.popen("tail -n 5 db/data/log/bchat-receipts.txt").read().split('\n')
	# delete the last one, since its a ''
	receipts.pop()
	# find the one that belongs to the user
	for receipt in receipts[::-1]: # starting from the last one
		# get the content info
		owner, _, message, _,_,_,_ = receipt.split('-')
		# and check the owner
		if owner == author:
			# save the answer
			answer = message
			# and break
			break

  	# send the answer
	return [{
		"type": "text",
		"content": answer
	}]


# info about the skill
info = """
Lambda IoT: Encender
Permite a Lambda encender dispositivos conectados a la red de dispositivos de IoT de Lambda. Manda un valor de 255. Para más información técnica consulta https://github.com/OmarSaldanna/lambda-iot-client
Comando:Lambda [enciende|activa|prende] el [alias del dispositivo]
Ejemplo:Lambda enciende el led rojo
Ejemplo:lambda activa la bomba de agua
"""