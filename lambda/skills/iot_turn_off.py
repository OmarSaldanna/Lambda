import requests
import time
import os


# Lambda apaga el ...
# Lambda deactiva el ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# get the device alias
	alias = message.split(' ')[2:]
	alias = ' '.join(alias)
	# set the message content
	message_content = {
		"from": "lambda", "to": author, "type": "output",
		"alias": alias, "value": "0"
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
### Lambda IoT Turn Off
This skill makes Lambda able to communicate with the BChat and through it **turn on devices with Arduinos connected to internet all over the world**. This skill is **only to turning off devices**, there's other one that allows to turn on.
> **Comando: Lambda [apaga, desactiva] el [device alias]
> **Ejemplo: Lambda desactiva el led rojo
> **Ejemplo: lambda apaga la luz del estudio
> **Verbos:** apaga, desactiva.
"""