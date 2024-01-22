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


# 0   1  2      3 4   5 6
# Lee la imagen y ...
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
	image_id = openai.user_data['file']
	# cath the text prompt
	text_prompt = ' '.join(splited_message[4:])
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
Visión Inteligente
Esta función permitirá que Lambda analice imágenes y puedas preguntar sobre ellas, desde diagramas, plantas, animales, paises, ecuaciones, arte y mucho más. Solo sube el tu imagen al chat, y luego de que lambda te diga que "tu archivo está disponible" haz tus preguntas. Se aceptan formatos .jpg .jpeg .heic .png. 
Comando: Lambda [lee|analiza|ve|mira|observa] la [imagen|foto|diagrama|cuadro] y [tus preguntas]
Ejemplo: Lambda mira la imagen y dime que puedes ver
Ejemplo: Lambda analiza el cuadro y dime de que artista piensas que sea
Ejemplo: lambda lee el diagrama de $db8194cf7daf4efe y dame una breve explicación de lo que habla el diagrama
"""