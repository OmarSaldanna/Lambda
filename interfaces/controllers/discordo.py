# modules
from controllers.memory import refresh_users
# libraries
import requests
import os

lambdrive_path = 'lambdrive/'

def call_lambda(message: str, author: str):
	# call lambda api
	answer = requests.get(
		'http://127.0.0.1:8080/lambda', 
		headers={
			"message": message,
			"author": author
		}
	)
	return answer.json()['content']

# split a text in pieces of n length
# this was implemented cause of there's messages with len
# greater than 2K characters that discord don't acept. So
# send multiple messages if the msg is too large
# msg is the text, and message is the discord instance
def split_text(text, n=2000):
    return [text[i:i+n] for i in range(0, len(text), n)]


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
			res = "Tu comando todo no jaló mano"

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


def get_admin_manual():
	return split_text("""
            **Manual de Admin**

            ** Lambda CLI **
            > **Uso:** $ comando
            > **Ejemlos:**
            *$ ls*
            *$ cat ram/log.txt*
            *$ ls servies/lambdrive*
            > **Descripción:** es `básicamente una terminal al server de Lambda` integrada en el chat. Es importante recalcar que esta terminal `no es precisamente una terminal completamente operativa, pueden trabarla los comandos que ocupan la terminal, como ping, ssh, vi ...`
           	
           	** Adminisrador de miembros **
           	> **Uso:** member [add|see|del] miembro
           	> **Ejemlos:**
            *member see*
            *member add Lambda#6213*
            *member del Lambda#6213*
            > **Descripción:** permite hacer `gestión de los miembros que cuentan con accceso a Lambda`. Las acciones son `agregar, eliminar y ver los miembros actuales.`

            ** Manual de Admin **
            > **Uso:** aman
            > **Ejemplo**
            *aman*
            > **Descripción:** es en escencia el mensaje que despliega el manual del adninistrador, que `explica a detalle las funciones propias del administrador de lambda.`

            ** Manual de Admin **
            > **Uso:** aman
            > **Ejemplo**
            *aman*
            > **Descripción:** es en escencia el mensaje que despliega el manual del adninistrador, que `explica a detalle las funciones propias del administrador de lambda.`

            ** Lambdrive CLI **
            > **Uso:** lambdrive [ls|rm|mv|cp] argumentos
            > **Ejemlos:**
            *lambdrive ls*
            *lambdrive rm borrame.txt*
            *lambdrive mv nombre1.txt nombre2.txt*
            *lambdrive cp archivo.txt copia.txt*
            > **Descripción:** es un gestor rápido para los archivos almacenados en el servicio de lambdrive. Permite listar los archivos con **ls**, eliminar archivos con **rm**, renombrar archivos con **mv** y copiar archivos con **cp**.
        	""", 2000)


# simplificar a controllers las funciones de members
def add_member(message, members, info, admin):
	# user will be the third argument
	user = message.content.split(' ')[2]
	# but as a tagged user, the id will be like
	# <@1024056505789587486>
	user = user[2:-1]
	# if the user is already in members
	if user in members:
		log = f'[DISCORDO] -> Admin <@{admin}> tried to add <@{user}>'
		return f"> <@{user}> ya es parte de Lambda", log
	# if the user is not in members yet
	else:
		log = f'[DISCORDO] -> Admin <@{admin}> added <@{user}>'
		# append the user
		info['members'].append(user)
		# write changes
		info.write()
		# and refresh
		refresh_users(members)
		# send confirmation
		return f"> <@{user}> se bienvenido a Lambda", log


def delete_member(message, members, info, admin):
	# user will be the third argument
	user = message.content.split(' ')[2]
	# but as a tagged user, the id will be like
	# <@1024056505789587486>
	user = user[2:-1]
	# try to delete the user
	try:
		# find the idx
		idx = members.index(user)
		# delete it from members
		info['members'].pop(idx)
		# save changes
		info.write()
		# and refresh
		refresh_users(members)
		msg = f"> <@{user}> eliminado de Lambda"
		log = f'[DISCORDO] -> Admin <@{admin}> deleted <@{user}> from members'
	# if there's no user in members
	except:
		log = f'[DISCORDO] -> Admin <@{admin}> tried to delete <@{user}> from members'
		msg = f"> <@{user}> actualimente no es parte de Lambda"
		# finally send the mesage
	return msg, log


def lambdrive_cli(message, command):
	# list files
	if command == 'ls':
		res = os.popen(f"ls {lambdrive_path}").read()
		return split_text(res,2000)
	# remove a file
	elif command == 'rm':
		file = message.content[13:]
		os.popen(f"rm {lambdrive_path}{file}")
		return [f"> {lambdrive_path}{file} deleted"]
	# move or rename a file
	elif command == 'mv':
		text = message.content[13:]
		# since there are two arguments
		args = text.split(' ')
		os.popen(f"mv {lambdrive_path}{args[0]} {lambdrive_path}{args[1]}")
		return [f"> {args[0]} moved to {args[1]}"]
	# move or rename a file
	elif command == 'cp':
		text = message.content[13:]
		# since there are two arguments
		args = text.split(' ')
		os.popen(f"cp {lambdrive_path}{args[0]} {lambdrive_path}{args[1]}")
		return [f"> {args[0]} copied to {args[1]}"]
	
	# if the command is unknown
	else:
		return ["> No entendí tu comando. Los comandos disponibles son", "lambdrive [ls|rm|mv|cp]"]