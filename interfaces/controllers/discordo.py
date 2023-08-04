# libraries
import requests
import json
import os

############################################################
###################### General Functions ###################
############################################################

# general function to make requests to db
def db_request(type_: str, api: str, headers: dict):
	api = f'http://127.0.0.1:8081{api}'
	# prepare the dic
	for key in headers.keys():
		# if there's a dic in headers
		if type(headers[key]) == dict:
			# json dump
			headers[key] = json.dumps(headers[key])
	# make the request based on type
	if type_ == 'GET':
		return requests.get(api, headers=headers).json()
	elif type_ == 'POST':
		return requests.post(api, headers=headers).json()
	elif type_ == 'PUT':
		return requests.put(api, headers=headers).json()
	else:
		raise ValueError('Type of request unknown')

# general functions to use lambda
def call_lambda(message: str, author: str, server: str,on_conversation=False):
	# default lambda url for calls
	lambda_url = 'http://127.0.0.1:8080/lambda'
	# if it was a conversation request
	if on_conversation:
		lambda_url = 'http://127.0.0.1:8080/lambda/conversation'
	# call lambda api
	answer = requests.get(
		lambda_url,
		headers={
			"message": message,
			"author": author,
			"server": server
		}
	)
	return answer.json()

# split a text in pieces of n length
# this was implemented cause of there's messages with len
# greater than 2K characters that discord don't acept. So
# send multiple messages if the msg is too large
# msg is the text, and message is the discord instance
def split_text(text, n=2000):
    return [text[i:i+n] for i in range(0, len(text), n)]

# manual for lambda
def get_public_manual():
	return split_text("""
# Manual de Usuario
_Cualquier duda y para mejor explicación preguntar a_ **@Reagan**.
            
> **Lo Nuevo en Lambda**
Actualmente lambda se encuentra en su versión 3, la cual hace de lambda algo más que una simple herramienta o bot de discord, **Lambda ha incluido nuevos ajustes que permiten una interacción muy personalizada para los usuarios:**

* **Adios Comandos**: Para los usuarios, lambda ya no cuenta con un alto repertorio de comandos, sino que ahora, para todo lo que necesites solo tendrás que usar la palabra **Lambda**, investigaciones, imágenes generadas con IA, conversaciones, QRs y mucho más al **alcance de una sola palabra**.
* **Ajuste de personalidad**: puedes pedirlque **que hable como alguna figura literaria** y sostener una contínua conversación con Lambda como si fuera ese mítico personaje. _Para cambiar ese ajuste contacta a @Reagan_.
* **Contexto**: ahora como el chatGPT lambda ya basa sus respuestas en tus preguntas y sus respuestas anteriores, de manera que puedes sostener conversaciones sin que lambda pierda el hilo de esta. de un mensaje a otro.
* **Conversaciones**: Lambda tiene dos ajustes para guardar contexto: si el contexto llega a llenarse con **preguntas, entonces el contexto será elminado para una nueva plática**. Por otro lado, si se llena en **una conversación, Lambda mantendrá el contexto de tu última pregunta y la última respuesta, de esa manera la conversación puede ser más extensa**.

# Interacción con Lambda

Como fue previamente mencionado, ahora la mayoría de funciones de Lambda puden ser usadas mediante su nombre. Aquí algunos ejemplos de Lo que lambda puede hacer:

> **Imágenes o QRs:**
* Lambda **[genera|crea]** un QR _de www.mipagina.com_
* Lambda **[genera|crea] [una|dos|tres]** imágenes _de a wonderful landscape on martian surface_

> **Preguntas generales:**
* Lambda **dime** _cuál es la cápital de Italia?_

> **Conversaciones contínuas:**
* Lambda, _en que nos quedamos?_

> Preguntas generales:
* Lambda quien eres?
* Lambda cómo estás?
* Lambda cuándo fue la última vez que te reiniciaste?
* Lambda qué sabes hacer?
* Lambda qué puedes hacer?

	""", 2000)

############################################################
###################### Admin Functions #####################
############################################################

def lambda_cli(message):
	commands = message.content[2:]
    # if the admin run an update
	if commands == 'lambda rupdate':
    	# the command will be executed in the discord app.py
		command = 'tmux new-session -d -s rupdate "cd $HOME/Lambda && lambda rupdate && tmux kill-session -t rupdate"'
      	# doesn't return nothing
		os.popen(command).read()
      	# lambda will be restarted...
		return ['reiniciando windows']

    # if it was a simple command      
	else:
		# then send the comands to the terminal
		res = os.popen(commands).read()
		# if the command is not correct, res will be ''
		if res == '':
			# and discord throws error sending empty messages
			res = "Tu comando jaló"

		# if the result it's larger than discord's limit
		if len(res) > 2000:
			# split the text in pieces
			pieces = split_text(res, 2000)
			# add the final message
			pieces.append("**" + '-'*100 + "**")
			# return pieces
			return pieces
		else:
			return [res]