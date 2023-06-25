# modules
from controllers.memory import get_memory
# libraries
import requests
import os

lambdrive_path = 'lambdrive/'

############################################################
###################### General Functions ###################
############################################################

def call_lambda(message: str, author: str, on_conversation=False):
	# default lambda url for calls
	lambda_url = 'http://127.0.0.1:8080/lambda'
	# if it was a conversation request
	if on_conversation:
		lambda_url = 'http://127.0.0.1:8080/lambda/conversation'
		print(lambda_url)
	# call lambda api
	answer = requests.get(
		lambda_url,
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

def get_public_manual():
	return split_text("""
# Manual de Usuario
_Cualquier duda y para mejor explicación preguntar a_ **@Reagan**.
            
> **Lo Nuevo en Lambda**
Actualmente lambda se encuentra en su versión 2, la cual hace de lambda algo más que una simple herramienta o bot de discord, **Lambda ha incluido nuevos ajustes que permiten una interacción muy personalizada para los usuarios:**

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
			res = "Tu comando todo no jaló mano"

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


def get_admin_manual():
	return split_text("""
            # Manual de Admin

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

            ** Función de Echo **
            > **Uso:** echo mensaje...
            > **Ejemplo**
            *echo @Lambda*
            > **Descripción:** imprime en cuestón, lo que está después de echo, pero sin ser procesado. Esta función es utilizada principalmente para desarrollo y para demostraciones del chat de discord.

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
def add_member(message):
	# read the memory
	memory_file = get_memory('info')	
	# user will be the third argument
	user = message.content.split(' ')[2]
	# but as a tagged user, the id will be like
	# <@1024056505789587486>
	user = user[2:-1]
	# if the user is already in members
	if user in memory_file['members']:
		log = f'[DISCORDO] -> Admin <@{message.author.id}> tried to add <@{user}>'
		return f"> <@{user}> ya es parte de Lambda", log
	# if the user is not in members yet
	else:
		log = f'[DISCORDO] -> Admin <@{message.author.id}> added <@{user}>'
		# append the user
		memory_file['members'].append(user)
		# write changes
		memory_file.write()
		# send confirmation
		return f"> <@{user}> se bienvenido a Lambda", log


def delete_member(message):
	# user will be the third argument
	user = message.content.split(' ')[2]
	# but as a tagged user, the id will be like
	# <@1024056505789587486>
	user = user[2:-1]

	# try to delete the user
	try:
		# read the memory
		memory_file = get_memory('info')
		# find the idx
		idx = memory_file['members'].index(user)
		# delete it from members
		memory_file['members'].pop(idx)
		# save changes
		memory_file.write()
		# return the messages
		msg = f"> <@{user}> eliminado de Lambda"
		log = f'[DISCORDO] -> Admin <@{message.author.id}> deleted <@{user}> from members'
		return msg, log
	# if there's no user in members
	except:
		log = f'[DISCORDO] -> Admin <@{message.author.id}> tried to delete <@{user}> from members'
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