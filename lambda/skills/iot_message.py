import requests
import time
import os


# Lambda manda el valor del [device] a [value]
# Lambda manda el estado del [device] a [value]
# Lambda manda el mensaje del [device] a [value]
# Lambda manda el brillo del [device] a [value]
# same for verbs: cambia, envia, ajusta
def main(params: tuple):
	# catch params
	message, author, server = params
	# first split device, value
	alias_container, value = message.split(' a ')
	# get the device alias
	alias = alias_container.split(' ')[5:]
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
		"alias": alias, "value": value
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
### Lambda IoT Turn On
Esta Skill permite a lambda encender dispositivos conectados a la red de dispositivos de IoT de Lambda. Para más información consulta [este tutorial](https://github.com/OmarSaldanna/lambda-iot-client).
> **Comando: Lambda [enciende, activa, prende] el [device alias]
> **Ejemplo: Lambda enciende el luz rojo
> **Ejemplo: lambda activa la bomba de agua
> **Ejemplo: lambda prende la luz del estudio
> **Verbos:** enciende, activa, prende.
"""