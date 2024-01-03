# modules
from core.models.lwr import Lambda_Word_Recognizer as LWR
# and librariesimport requests
import requests
import time
import os


# Lambda dime el valor de ...
# Lambda dime la humedad de ...
# Lambda dime la temperatura de ...
# Lambda dime la medida de ...
# the same commands but for "dame" and "lee" verbs
def main(params: tuple):
	# catch params
	message, author, server = params
	# get the device alias
	alias = message.split(' ')[5:]
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
		"from": "lambda", "to": author, "type": "intput",
		"alias": alias, "value": ""
	}

	# send it to the lambda bchat api
	requests.post(
		'http://127.0.0.1:8092/bchat',
		json=message_content
	)
	# wait some time
	time.sleep(2)
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
### Lambda IoT Reader
Esta skill permite que Lambda lea el valor de sensores o estados de dispositivos (cualquier variable) conectados a los Arduinos en la red de Arduinos de Lambda para IoT. Para más información consulta [este tutorial](https://github.com/OmarSaldanna/lambda-iot-client).
> **Comando: Lambda [dime, dame, lee] el [cosa] del [dispositivo]
> **Ejemplo: Lambda lee la medida del potenciometro
> **Ejemplo: lambda dime la temperatura del cuarto
> **Ejemplo: lambda dame la humedad del la cocina
> **Verbos:** lee, dime, dame.
> **Cosas:** valor, temperatura, humedad, medida.
"""