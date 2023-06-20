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


##############################################################
################# Verbal Funcions ############################
##############################################################

# Lambda crea|genera un qr de|con www.google.com
def generate_qr(content: str, user: str):
	# create QR code instance
	#qr = qrcode.QRCode(version=1, box_size=10, border=5)
	# add data to QR code
	#qr.add_data(content)
	#qr.make(fit=True)
	# create image from QR code
	#img = qr.make_image(fill_color="black", back_color="white")
	# create a hash to save the file
	#h = generate_hash(content)
	# save image to file
	#img.save(f"{h}.png")
	return f"tu QR está en algun_lado.png"

# lambda crea|genera una imagen de algo
def call_dalle(content: str, user: str):
	# url = dalle(content)
	# return url[0]
	return "calling dalle"

# lambda dime cuando fue la revolucion francesa
def call_gpt(content: str, user: str):
	messages = [
		{"role": "system", "content": "eres un asistente, es prioritario que des respuestas cortas, preferentemente de no más de un párrafo."},
		{"role": "user", "content": content}
	]
	# return gpt(messages)
	return "calling gpt"

##############################################################
################# Question Funcions ##########################
##############################################################

# Lambda como estás?
def look_on_state(content: str, user: str):
	return "estoy bien"

# Lambda quien eres
def look_on_person(content: str, user: str):
	return "Soy Lambda"

# Lambda cuando fue la ultima vez que te actualizaste
def look_on_log(content: str, user:str):
	return "fue de hecho ayer"

##############################################################
################# Default Funcion ##########################
##############################################################

def default(content: str, user: str):
	return f"> Lo siento, la verdad no entendí que querías decir con _{content}_"

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