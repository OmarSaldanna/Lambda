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
	# load the context
	context, _ = load_context(user)
	# append the content to get the answer
	context.append({"role": "user", "content": content})
	# call gpt with the context and the content
	answer = gpt(context)
	# handle the result and the context
	handle_gpt_context(user, [
		{"role": "user", "content": content},
		{"role": "system", "content": answer}
	])
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
		{"role": "user", "content": f"Lambda {content}. Responde de manera breve, no más de 3 líneas. Responde de manera cómica basándote en los datos de tu cpu y en tus registros: \n{ram}\n{log_tail}"}
	]
	answer = gpt(messages, temp=.6)
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
		{"role": "user", "content": f"Lambda {content}. Responde basado en tu personalidad, pero que sea una respuesta de no más de un párrafo."}
	]
	answer = gpt(messages, temp=.6)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda personality: {content}')
	return [answer]


# Lambda cuando fue la ultima vez que te actualizaste, for example
def look_on_log(content: str, user:str):
	# load personality for questions
	personality = get_personality(user)
	# load the log
	log = read_log()
	# define the message
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": f"Lambda {content}. Responde de manera científica, no más de un tres líneas, básate los siguientes registros:\n{log}"}
	]
	answer = gpt(messages, temp=.6)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda logs: {content}')
	return [answer]


# Lambda que sabes hacer ?
# Lambda que puedes hacer ?
# this message is the manual
def look_on_usage(content: str, user:str):
	# load personality for questions
	personality = get_personality(user)
	# define the message
	messages = [
		{"role": "system", "content": personality},
		{"role": "user", "content": f"Lambda, te acaban de preguntar que qué sabes y puedes hacer, responde tomando en cuenta que Lambda sabe responder a preguntas como:\n Cómo estas?, cuándo fue tu ultimo reinicio?, quién eres?. Además eres capaz de generar imágenes si lo piden como por ejemplo 'lambda crea una imagen de algo', además eres capaz de responder preguntas si se te llama con los prompts de lambda dime ... y lambda, ..."}
	]
	answer = gpt(messages, temp=.6)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> questioned lambda usage: {content}')
	return [answer]

##############################################################
################# Conversation Funcion #######################
##############################################################
# this is special, since it does not call to lambda ia, it 
# just calls a function to answer, and it is called with the
# "Lambda, ...", also will be for the real conversations
def conversation(content: str, user: str):
	# load the context
	context, _ = load_context(user)
	# append the content to get the answer
	context.append({"role": "user", "content": f"{content}\nQue tu respuesta solo contenga párrafos, no listas, pues será leído por una máquina. Que tus respuestas sean detalladas pero no más extensas que DOS párrafos."})
	# call gpt with the context and the content
	answer = gpt(context)
	# handle the result and the context
	handle_gpt_context(user, [
		{"role": "user", "content": content},
		{"role": "system", "content": answer}
	], on_conversation=True)
	# add to log
	app_to_log(f'[BODY] -> <@{user}> called gpt: {content}')
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
		look_on_log,
		look_on_usage
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