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


# 0   1  2     3  4
# lee el texto de ...
# transcribe el audio de ...
# extrae el texto de ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# catch the audio id
	audio_id = message.split(' ')[4][1:]
	# pass the id through the security check
	security_check(audio_id)
	# get the extension of the file
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id}").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	return [{"type": "text", "content": audio_path}]
	# use OpenAI whisper
	return openai.speech_to_text(audio_path)


# info about the skill
info = """
### Audio Transcriber
Esta función permite a Lambda transcribir el texto de audios, **audios que pueden ser en casi cualquier idioma**. Solamente sigue estos pasos:
* Sube el audio a discord como un archivo, puedes mandarlo al chat de @Lambda.
* Y usa el comando para transcribir el texto del audio.
> **Comando: Lambda [lee, extrae o transcribe] el [audio o texto] de [la id del audio]
> **Ejemplo: Lambda transcribe el audio de $db8194cf7daf4efe
> **Ejemplo: Lambda extrae el texto de $db8194cf7daf4efe
> **Ejemplo: lambda lee el texto de $db8194cf7daf4efe
> **Verbos:** lee, extrae o transcribe
> **Sustantivos:** audio o texto
"""