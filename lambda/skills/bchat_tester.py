import requests
import json
import os
# in case of use openai module
# from core.modules import OpenAI

# Lambda prueba el bchat ...
# Lambda testea el bchat ...

# Lambda envia a bchat ...
# Lambda manda a bchat ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# get the message
	content_list = message.split(' ')[3:]
	content = ' '.join(content_list)
	# send it to the lambda bchat api
	requests.post('http://127.0.0.1:8092/bchat', json=json.loads(content))
	# read the logs
	receipt = os.popen("tail -n 1 db/data/log/bchat-receipts.txt").read()
  	# or return something
	return [{
		"type": "text",
		"content": "Mensaje Enviado:"
	}, {
		"type": "text",
		"content": str(content)
	}, {
		"type": "text",
		"content": receipt
	}]


# info about the skill
info = """
### title
description
> **Comando: command
> **Ejemplo: example
> **Verbos:** verbs
"""