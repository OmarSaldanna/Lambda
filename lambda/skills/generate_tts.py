from core.modules import OpenAI

# crea un audio con ...
# the same for genera, dame
def main(params: tuple):
	# catch params
	message, author, server = params
	# everything after the fourth word
	prompt = message.split(' ')[4:]
	prompt = ' '.join(prompt)
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# use the TTS model function
	return openai.text_to_speech(prompt)


# info about the skill
info = """
### Text To Speech
Esta función te permitirá **generar audios a partir de un texto**, todo por inteligencia artificial. Solo manda el texto y Lambda generará el audio al instante. El modelo puede generar audio en múltiples idiomas, por ejemplo: Inglés, Alemán, Francés y muchos más. **No tienes que específicar el idioma, simplemente escribe el texto** en el idioma que quieras, si quieres copia y pega de una traducción.
> **Comando:** Lambda [crea, genera o dame] una [audio] de ...
> **Ejemplo:** lambda crea un audio de Ich haiße Lambda, Ich bin gut, un Dir?
> **Ejemplo:** Lambda dame un audio de Bonjour bonne journée comment vas-tu?
> **Ejemplo:** Lambda dame un audio de Hello good morning, how are you??
"""