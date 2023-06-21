# here are located all the lambda funcions, what he can do
# the objective here is to generate a dict wirh the functions
# to be passed to to the brain, used by the lmm model.

# there will be a specific function asociated with each verb
# and question. 

# libraries
import os
import qrcode

# functions from files
from core.models.openai import GPT, DALLE
from core.extensions import *
from core.memory import *

# instances for memory, GPT and DALLE
info = get_memory('info')
openai_token = info['openai']
# the openai models
gpt = GPT(openai_token)
dalle = DALLE(openai_token)
# lambdrive path
lambdrive_path = 'lambdrive/'

##############################################################
################# Verbal Funcions ############################
##############################################################

# crea|genera un qr de|con www.google.com
def generate_qr(content: str, user: str):
	# create QR code instance
	qr = qrcode.QRCode(version=1, box_size=10, border=5)
	# select the qr content
	data = content.split(' ')[-1]
	# add data to QR code
	qr.add_data(data)
	qr.make(fit=True)
	# create image from QR code
	img = qr.make_image(fill_color="black", back_color="white")
	# create a hash to save the file
	h = hash(data)
	# save image on lambdrive/qrs
	img.save(f"{lambdrive_path}qrs/{h}.png")
	# upload to cloudinary
	url = upload_image(f"{lambdrive_path}qrs/{h}.png")
	# app to log
	app_to_log(f'[BODY] -> <@{user}> created a QR: {data}')
	# and return the messages
	return [url]

# crea|genera una imagen de algo
def call_dalle(content: str, user: str):
	# everything after the fourth word 
	prompt = content.split(' ')[4:]
	prompt = ' '.join(prompt)
	# second word is the number of images
	second_word = content.split(' ')[1]
	
	quantity = 1
	# una was skipped
	if second_word == 'dos':
		quantity = 2
	if second_word == 'tres':
		quantity = 3

	# start writing the answer
	answer = []
	# create the images with dalle
	images = dalle(prompt, quantity)
	# download the images
	for link in images:
		# save as the hashed link
		download_image(link, lambdrive_path + 'dalle/ ' + str(hash(link)))
		# append to answer the links
		answer.append(link)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> called dalle for {quantity} images: {prompt}')
	return answer

# lambda dime cuando fue la revolucion francesa
# fast questions, and more precise questions
def call_gpt(content: str, user: str):
	# load the user personality
	personality = get_personality(user)
	# create the structure
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": content}
	]
	answer = gpt(messages)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> called gpt: {content}')
	return [answer]

##############################################################
################# Question Funcions ##########################
##############################################################

# Lambda como estás?
def look_on_state(content: str, user: str):
	# load personality for questions
	personality = get_personality(user)
	# get the stats
	ram = os.popen('free -h').read()
	log_tail = os.popen(f'tail {log_file}').read()
	# define the message
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": f"{content}. Responde de manera rápida, no más de un párrafo. Responde de manera cómica basándote en los datos de tu cpu y en tus registros: \n{ram}\n{log_tail}"}
	]
	answer = gpt(messages, temp=.7)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda state: {content}')
	return [answer]

# Lambda quien eres
def look_on_person(content: str, user: str):
	# load personality for questions
	personality = get_personality(user)
	# define the message
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": f"{content}. Responde basado en tu personalidad, pero que sea una respuesta de no más de un párrafo."}
	]
	answer = gpt(messages, temp=.7)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda personality: {content}')
	return [answer]

# Lambda cuando fue la ultima vez que te actualizaste
def look_on_log(content: str, user:str):
	# load personality for questions
	personality = get_personality(user)
	# load the log
	log = read_log()
	# define the message
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": f"{content}. Responde de manera científica, no más de un párrafo, básate en la siguiente información. En los registros, lo primero es la fecha y luego de -> lo que pasó \n{log}"}
	]
	answer = gpt(messages, temp=.7)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda logs: {content}')
	return [answer]


##############################################################
################# Default Funcion ############################
##############################################################

def default(content: str, user: str):
	return [f"> Lo siento, la verdad no entendí que querías decir con:",f"> *{content}*"]

##############################################################
################# The Funcion Dict ###########################
##############################################################
# important, the keys and functions must be align based on the
# vocabulary file

# get the vocab structure
vocab = get_memory('vocabulary')

# for verbs
verb_dic = list_dic(
	vocab['verbos'],
	# dalle and qr are called with the same words
	# then the selection will be based on the third
	# dict than considers the thing
	[
		call_gpt,
		[call_dalle, generate_qr]
	],
	default
)

# and questions
quest_dic = list_dic(
	vocab['preguntas'],
	[
		look_on_state,
		look_on_person,
		look_on_log
	],
	default
)

# third dict that includes the functions that
# share activation words like DALLE and QR, then this
# dict will and the

thing_dic = list_dic(
	vocab['objetos'],
	[
		call_dalle,
		generate_qr
	],
	default
)

# this will be passed to the brain, where the words will be
# asociated to specific functions
function_dic = {
	"verb": verb_dic,
	"question": quest_dic,
	"thing": thing_dic
}