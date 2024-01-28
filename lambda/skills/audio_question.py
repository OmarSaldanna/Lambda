import os
from core.modules import OpenAI


# since the os.popen excecutes commands in system
# there's risk of injection attack
def security_check(audio_id: str):
	# wrong id length
	if len(audio_id) != 16: ######################## actual size of hashes ###########
		raise ValueError("unknown hash")
	# the hash do not contain that characters
	for c in ' \\/$%&*:;.,][()!\"\'<>':
		if c in audio_id:
			raise ValueError("unknown hash")


# 0   1  2     3 4
# lee el texto y ...
# transcribe el audio y ...
# extrae el texto y ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# split the message
	splited_message = message.split(' ')
	# catch the image id
	audio_id = openai.user_data['file']
	# cath the text prompt
	text_prompt = ' '.join(splited_message[4:])
	# pass the id through the security check
	security_check(audio_id)
	# get the extension of the file
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id} | head -n 1").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	# use OpenAI whisper
	audio_text = openai.speech_to_text(audio_path)
	# extract the text from the answer
	text = audio_text[0]['content']
	# then ask gpt-3 without context
	return openai.gpt(text_prompt, context=False, system=f"Eres una IA, responde a la pregunta BASADO EN LA SIGUIENTE INFORMACIÓN proveniente de un audio: {text}", model="gpt-3.5-turbo-16k")


# info about the skill
info = """
Pregunta a Audio
Esta función permite a Lambda transcribir el texto de audios para después hacer preguntas espeíficas sobre la información del audio. Sólo sube o graba el audio y después puedes preguntar.
Comando:Lambda [lee|analiza|oye|escucha] el [audio] y [preguntas]
Ejemplo:Lambda analiza el audio y dame un resumen breve
Ejemplo:Lambda oye el audio y extrae las palabras clave del audio
"""