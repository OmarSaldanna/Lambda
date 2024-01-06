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


# 0       1  2     3  4
# traduce el audio de $id
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# catch the image id
	audio_id = message.split(' ')[4][1:]
	# pass the id through the security check
	security_check(audio_id)
	# get the extension of the file
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id} | head -n 1").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	# use OpenAI whisper
	audio_text = openai.speech_to_text(audio_path, "translation")
	# extract the text from the answer
	text = audio_text[0]['content']
	# then ask gpt-3 without context
	return openai.gpt(text, model="gpt-3.5-turbo-16k", context=False, system="Eres una IA para realizar traducciones RESPONDE ÚNICAMENTE CON LA TRADUCCIÓN EN ESPAÑOL DEL TEXTO PROPORCIONADO")


# info about the skill
info = """
### Spanish Audio Translator
Esta función hará que **Lambda traduzca a texto en español un audio en cualquier idioma**. Ideal para traducir fragmentos de videos, o diálogos con extranjeros. Para usar esta función sigue estos pasos:
* 1. Sube el audio a discord como un archivo, puedes mandarlo al chat de @Lambda.
* 2. Usa el comando para transcribir el texto del audio. Es el siguiente:
> **Comando:** Lambda traduce el audio de [la id del audio]
> **Ejemplo:** Lambda traduce el audio de $db8194cf7daf4efe
> **Ejemplo:** lambda traduce el audio de $db8194cf7daf4efe
> **Verbos:** traduce
> **Sustantivos:** audio
"""