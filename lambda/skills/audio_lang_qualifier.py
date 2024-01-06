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


# 0        1  2             3  4
# califica mi pronunciación de ...
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
	audio_text = openai.speech_to_text(audio_path)
	# extract the text from the answer
	text = audio_text[0]['content']
	# then ask gpt-3 without context
	return openai.gpt(f"El siguiente mensaje lo que la IA capturó: {text}", model="gpt-3.5-turbo-16k", context=False, system="Eres parte de la enseñanza de lengua extranjera de un alumno, este grabó un audio y este mismo fue transcrito por una IA. BASADO EN EL IDIOMA EN QUE ESTE EL MENSAJE: Califica del 1 al 10 y brinda retroalimentación EN UNA LISTA DE PUNTOS, sobre gramática, vocabulario y demás.")


# info about the skill
info = """
### Audio Language Qualifier
Esta función te **permitirá evaluar tus audios en cualquier idioma, Lambda evaluará tu audio y te dará retroalimentación sobre tu diálogo, vocabulario, gramática y más**. Esta función es ideal para practicar tu aprendizaje de idioma. **No tienes que especificar el lenguaje, Lambda lo va a detectar automáticamente. Solo sigue los siguientes pasos:
* 1. Sube el audio a discord como un archivo, puedes mandarlo al chat de @Lambda.
* 2. Usa el comando para transcribir el texto del audio. Es el siguiente:
> **Comando:** Lambda [califica, evalúa, oye o escucha] mi [pronunciación o idioma] de [id del audio]
> **Ejemplo:** Lambda califica mi pronunciación de $db8194cf7daf4efe
> **Ejemplo:** Lambda escucha mi pronunciación de $db8194cf7daf4efe
> **Ejemplo:** lambda evalúa mi idioma de $db8194cf7daf4efe
> **Verbos:** califica, evalúa, oye o escucha
> **Sustantivos:** inglés
"""