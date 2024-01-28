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
	audio_id = openai.user_data['file']
	# pass the id through the security check
	security_check(audio_id)
	# get the extension of the file
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id} | head -n 1").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	# use OpenAI whisper
	answer = openai.speech_to_text(audio_path, "translation")
	# extract the text from the answer
	audio_text = message + ':\n' + answer[0]['content']
	# then ask gpt-3 without context
	return openai.gpt(audio_text, model="gpt-3.5-turbo-16k", context=False, system="Eres una IA para realizar traducciones RESPONDE ÚNICAMENTE CON LA TRADUCCIÓN en el idioma especificado, si no se especifica, tradúcelo a español", model="gpt-3.5-turbo-16k")


# info about the skill
info = """
Traductor de Audios
Esta función hará que Lambda traduzca a texto en cualquier idioma (a español por default) un audio en cualquier idioma. Ideal para traducir fragmentos de videos, o diálogos con extranjeros. Sólo sube tu archivo o graba el audio y ocupa la función.
Comando:Lambda [traduce] el [audio] a [idioma del texto]
Ejemplo:Lambda traduce el audio
Ejemplo:Lambda traduce el audio a inglés
Ejemplo:Lambda traduce el audio a japonés
"""