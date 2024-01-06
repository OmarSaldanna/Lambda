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
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id} | head -n 1").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	# use OpenAI whisper
	return openai.speech_to_text(audio_path, "translation")


# info about the skill
info = """
### Audio Translator (English)
Esta función permite a Lambda traducir el texto de audios, **audios que pueden ser en casi cualquier idioma** al idioma **inglés**. Podrías grabar un audio en español desde Discord y pedirle a Lambda que te lo traduzca a inglés (en texto). **Ya después si lo deseas podrías usar la función de generar audios para crear audios en inglés**. Para usar este función solamente sigue estos pasos:
* 1. Sube el audio a discord como un archivo, puedes mandarlo al chat de @Lambda.
* 2. Usa el comando para transcribir el texto del audio. Es el siguiente:
> **Comando:** Lambda [traduce, transcribe] a [inglés] de [la id del audio]
> **Ejemplo:** Lambda transcribe a inglés de $db8194cf7daf4efe
> **Ejemplo:** Lambda traduce a ingles de $db8194cf7daf4efe
> **Verbos:** traduce, transcribe
> **Sustantivos:** inglés
"""