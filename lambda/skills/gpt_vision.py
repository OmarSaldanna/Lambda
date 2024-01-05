import os
from core.modules import OpenAI


# since the os.popen excecutes commands in system
# there's risk of injection attack
def security_check(file_id: str):
	# wrong id length
	if len(file_id) != 16: ######################## actual size of hashes ###########
		raise ValueError(f"unknown hash: {file_id}")
	# the hash do not contain that characters
	for c in ' \\/$%&*:;.,][()!\"\'<>':
		if c in file_id:
			raise ValueError(f"unknown hash: {file_id}")


# 0   1  2      3  4   5 6
# Lee la imagen de $id y ...
# same for analiza, ve, mira, observa
# also for foto, diagrama, cuadro
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# split the message
	splited_message = message.split(' ')
	# catch the image id
	image_id = splited_message[4][1:]
	# cath the text prompt
	text_prompt = ' '.join(splited_message[6:])
	# pass the id through the security check
	security_check(image_id)
	# get the extension of the file
	image_file = os.popen(f"ls lambdrive/images | grep {image_id} | head -n 1").read()[:-1]
	# create the file path
	image_prompt = f"lambdrive/images/{image_file}"
	# use OpenAI module vision
	return openai.gpt_vision(image_prompt, text_prompt)


# info about the skill
info = """
### AI Vision (by OpenAI's GPT)
Esta función permitirá que **Lambda analice imágenes y puedas preguntar sobre las imágenes**, desde diagramas, plantas, animales, paises, ecuaciones, arte y mucho más. Solo sigue estos pasos:
* 1. Sube la imagen a discord, puedes mandarla al chat de @Lambda.
* 2. Usa el comando para transcribir el texto del audio. Es el siguiente:
> **Comando: Lambda [lee, analiza, ve, mira u observa] el [imagen, foto, diagrama o cuadro] de [la id de la imagen] y [tus preguntas]
> **Ejemplo: Lambda mira la imagen de $db8194cf7daf4efe y dime que puedes ver
> **Ejemplo: Lambda analiza el cuadro de $db8194cf7daf4efe y dime de que artista piensas que sea
> **Ejemplo: lambda observa la imagen de $db8194cf7daf4efe y dime que planta es, y si es muy complicada y cara de cuidar
> **Ejemplo: lambda lee el diagrama de $db8194cf7daf4efe y dame una breve explicación de lo que habla el diagrama
> **Verbos:** lee, analiza, ve, mira u observa
> **Sustantivos:** imagen, foto, cuadro o diagrama
"""