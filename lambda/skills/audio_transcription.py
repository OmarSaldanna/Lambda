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


# 0   1  2
# lee el texto
# transcribe el audio
# extrae el texto
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# catch the audio id
	audio_id = openai.user_data['file']
	# pass the id through the security check
	security_check(audio_id)
	# get the extension of the file
	audio_file = os.popen(f"ls lambdrive/audios | grep {audio_id} | head -n 1").read()[:-1]
	# create the file path
	audio_path = f"lambdrive/audios/{audio_file}"
	# use OpenAI whisper
	return openai.speech_to_text(audio_path)


# info about the skill
info = """
Transcriptor de Audio
Esta función permite a Lambda transcribir el texto de audios, dichos pueden ser en casi cualquier idioma. Solamente sube tu archivo o graba un audio desde Discord y ocupa la función
Comando Lambda [lee|extrae|transcribe] el [audio|texto]
Ejemplo Lambda transcribe el audio
Ejemplo Lambda extrae el texto
Ejemplo lambda lee el texto
"""