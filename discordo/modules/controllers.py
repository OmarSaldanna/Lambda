import os
import requests
from modules.memory import get_memory

# split a text in pieces of n length
# this was implemented cause of there's messages with len
# greater than 2K characters that discord don't acept. So
# send multiple messages if the msg is too large
# msg is the text, and message is the discord instance
def split_text(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]


def lambda_cli(message):
	commands = message.content[2:]
    # if the admin run an update
	if commands == 'lambda rupdate':
    	# the command will be executed in the discord app.py
		command = 'tmux new-session -d -s rupdate "cd $HOME/Lambda && lambda rupdate && tmux kill-session -t rupdate"'
      	# record for the log file
		log = f'[DISCORD] -> running lambda rupdate'
      	# doesn't return nothing
		os.popen(command).read()
      	# lambda will be restarted...
		return ['0']

    # if it was a simple command      
	else:
		log = f'[DISCORD] -> access lambda-cli {commands}'
		# then send the comands to the terminal
		res = os.popen(commands).read()
		# if the command is not correct, res will be ''
		if res == '':
			# and discord throws error sending empty messages
			res = "Tu comando todo ñengo no jaló mano"

		# if the result it's larger than discord's limit
		if len(res) > 2000:
			# split the text in pieces
			pieces = split_text(res, 2000)
			# add the final message
			pieces.append("**Mames, it's so fucking big**")
			# return pieces
			return pieces
		else:
			return [res]


def chat_gpt(message, lambda_api):
    # then consult to lambda
	# print(f'[DISCORD] -> Using GPT3 -> {message.content}')
    # select the message content after the "lambda "
	msg = str(message.content)[7:]
    # consult to lambda
	ans = requests.get(lambda_api + '/gpt', headers={'msg':msg}).json()
	# print(ans['answer'])
    # if the result it's larger than discord's limit
	if len(ans['answer']) > 2000:
		# split the text in pieces
		pieces = split_text(ans['answer'], 2000)
		# add the final message
		pieces.append("**Mames, it's so fucking big**")
		# and return
		return pieces
	# if the message is inside the limit
	else:
		return [ans['answer']]


def get_manual():
	return """
                > **Funciones Disponibles**

                **Chat GPT**
                > **Uso:** [Lambda|lambda] pregunta
                > **Ejemlos:**
                *Lambda cúal es la capital de Rusia?*
                *Lambda como hago un hello world en javascript?*
                > **Detalles:** no guarda contexto como el chat gpt, además usa el modelo de gpt3.5-turbo

                ** Guardar Cosas **
                > **Uso:** [Sostenme|sostenme] texto
                > **Ejemplos:**
                *Sostenme http://endless.horse/*
                *sostenme 1234567890abcd1029*
                > **Detalles:** guarda en memoria algo una string.

                ** Buscar Cosas **
                > **Uso:** [Dame|dame] texto
                > **Ejemplos:**
                *Dame*
                *dame*
                > **Detalles:** muestra el guardado den memoria del usuario, si se da el caso que el usuario no tiene nada guardado, simplemente lambda dirá que no encontró nada.

                """

def save_stuff(message):
    # get the memory
    mem = get_memory('memory')
    # and save the stuff
    mem['stuff'][str(message.author)] = str(message.content[9:])
    mem.write()


def get_stuff(message):
	# get the memory
    mem = get_memory('memory')
    # try to read the memory
    try:
        stuff = mem['stuff'][str(message.author)]
    except:
        stuff = "Lo siento no encontré nada"
    return stuff