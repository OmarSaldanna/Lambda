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


# 0   1  2     3  4   5 6
# lee el texto de ... y ...
# transcribe el audio de ...
# extrae el texto de ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# split the message
	splited_message = message.split(' ')
	# catch the image id
	audio_id = splited_message[4][1:]
	# cath the text prompt
	text_prompt = ' '.join(splited_message[6:])
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
	return openai.gpt(text_prompt, context=False, system=f"Eres una IA, responde a la pregunta BASADO EN LA SIGUIENTE INFORMACIÓN proveniente de un audio: {text}")


# info about the skill
info = """
### Audio Questions
Esta función permite a Lambda transcribir el texto de audios para después **hacer preguntas espeíficas sobre la información del audio**.
* 1. Sube el audio a discord como un archivo, puedes mandarlo al chat de @Lambda.
* 2. Usa el comando para transcribir el texto del audio. Es el siguiente:
> **Comando: Lambda [analiza, oye o escucha] el [audio] de [la id del audio] y [pregunta]
> **Ejemplo: Lambda analiza el audio de $db8194cf7daf4efe y dame un resumen breve
> **Ejemplo: Lambda oye el audio de $db8194cf7daf4efe y extrae las palabras clave del audio
> **Ejemplo: lambda escucha el audio de $db8194cf7daf4efe y dame las ideas principales
> **Verbos:** analiza, oye o escucha
> **Sustantivos:** audio
"""