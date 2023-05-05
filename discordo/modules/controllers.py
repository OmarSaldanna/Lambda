import os
import qrcode
import requests
from modules.memory import *

lambdrive_path = "services/lambdrive/"

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
		return ['reiniciando windows']

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

            ** Lambdrive CLI **
            > **Uso:** lambdrive [ls|rm|mv|cp] argumentos
            > **Ejemlos:**
            > *lambdrive ls*
            > *lambdrive rm borrame.txt*
            > *lambdrive mv nombre1.txt nombre2.txt*
            > *lambdrive cp archivo.txt copia.txt*
            > **Descripción:** es un gestor rápido para los archivos almacenados en el servicio de lambdrive. Permite listar los archivos con **ls**, eliminar archivos con **rm**, renombrar archivos con **mv** y copiar archivos con **cp**.
        	""", 2000)


# simplificar a controllers las funciones de members
def add_member(message, vips, info):
	# user will be the third argument
	user = message.content.split(' ')[2]
	# if the user is already in vips
	if user in vips:
		log = f'[DISCORD] -> Admin on members -> tried to add {user}\n'
		return f"> {user} ya está con dios", log
	# if the user is not in vips yet
	else:
		log = f'[DISCORD] -> Admin on members -> added {user}\n'
		# append the user
		info['VIPS'].append(user)
		# write changes
		info.write()
		# and refresh
		refresh_users(vips)
		# send confirmation
		return f"> Bienvenido {user} a la buena vida pa", log


def delete_member(message, vips, info):
	# user will be the third argument
	user = message.content.split(' ')[2]
	# try to delete the user
	try:
		# find the idx
		idx = vips.index(user)
		# delete it from vips
		info['VIPS'].pop(idx)
		# save changes
		info.write()
		# and refresh
		refresh_users(vips)
		msg = f"> {user} exitosamente bajado del cielo"
		log = f'[DISCORD] -> Admin on members -> deleted {user}\n'
	# if there's no user in vips
	except:
		log = f'[DISCORD] -> Admin on members -> tried to delete {user}\n'
		msg = "> No apareció el wey"
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
		return ["> Escribe bien wey [ls|rm|mv|cp]"]

##########################################################################################
#################################### VIP Functions #######################################
##########################################################################################


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
	return split_text("""
                **Manual de Usuario**

                ** Chat GPT **
                > **Uso:** [Lambda|lambda] pregunta
                > **Ejemlos:**
                *Lambda cúal es la capital de Rusia?*
                *Lambda como hago un hello world en javascript?*
                > **Descripción:** es `básicamente un chat gpt integrado en discord`. De momento no guarda contexto como el chat gpt, además usa el modelo de `gpt3.5-turbo. En el futuro se prevee que si guarde contexto además de ajustes de "personalidad" propios de los usuarios que les ayuden a estos mismos a obtener mejores resultados.`

                ** Guardar Cosas **
                > **Uso:** [Sostenme|sostenme] texto
                > **Ejemplos:**
                *Sostenme http://endless.horse/*
                *sostenme 1234567890abcd1029*
                > **Descripción:** guarda en memoria algo como una string. Por ejemplo, `le puedes pedir que almacene un link importante para que después te lo regrese`.

                ** Buscar Cosas **
                > **Uso:** [Dame|dame] texto
                > **Ejemplos:**
                *Dame*
                *dame*
                > **Descripción:** muestra el `guardado de memoria del usuario`, si se da el caso que el usuario no tiene nada guardado, simplemente lambda dirá que no encontró nada.

                ** Manual de Usuario **
                > **Uso:** [Manual|manual|man]
                > **Ejemplos:**
                *Manual*
                *manual*
                *man*
                > **Descripción:** muestra el manual de usuario de Lambda, este `incluye sus funcionalidades y ejemplos de como hacer uso de dichas.`

                ** Señales de vida **
                > **Uso:** [Tas?|Tas|tas]
                > **Ejemplos:**
                *Tas?*
                *Tas*
                *tas*
                > **Descripción:** `Básicamente es un mensaje que informa si lambda se encuentra activo y operando correctamente` Responderá de la manera más rápida posible.

                ** Generador de QRs **
                > **Uso:** [QR|qr] link
                > **Ejemplos:**
                *QR www.google.com*
                *qr http://endless.horse/* 
                > **Descripción:** Es un generador de códigos QR a partir de un link o mensaje, así es, los QR pueden simplemente contener un "hola". Podrías comprobarlo si le pidieras un `qr hola` y lo escanearas con el celular.
                """, 2000)

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

# function for time
def get_time_for_file():
	# Get the current date and time in UTC
	utc_now = datetime.datetime.utcnow()
	# Create a timezone object for CDMX (UTC-5)
	cdmx_tz = pytz.timezone('America/Mexico_City')
	# Convert the UTC time to CDMX time
	cdmx_now = utc_now.replace(tzinfo=pytz.utc).astimezone(cdmx_tz)
	# Print the current date and time in CDMX time
	return str(cdmx_now.strftime('[%Y-%m-%d--%H:%M:%S]'))

def generate_qr(message):
	# in case there's not enough content for QR
	if len(message.content) <= 3:
		raise ValueError("Error: not enough content for QR")
	# QR object
	qr = qrcode.QRCode(version=1, box_size=10, border=5)
	# recieve the data for the qr
	data = message.content[3:]
	qr.add_data(data)
	qr.make(fit=True)
	# create QR
	img = qr.make_image(fill_color="black", back_color="white")
	# generate the filename with user and time
	file_name = f"qr-{str(message.author)}-{get_time_for_file()}"
	file_path = f"services/lambdrive/qr/{file_name}.png"
	# save the qr image
	img.save(file_path)
	return file_path
