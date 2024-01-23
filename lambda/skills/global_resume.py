# Lambda's OpenAI module
from core.modules import OpenAI
# file that contains the "info" of all the modules
global_resume = "lambda/skills/global_resume.txt"


def read_file(path):
    try:
    	# opens the file
        with open(path, 'r') as archivo:
        	# reads the content
            contenido = archivo.read()
            # and returns it
            return contenido
    # in case of errors
    except FileNotFoundError:
        return f"archivo no encontrado: {path}"
    except PermissionError:
        return f"No se tienen permisos para acceder al archivo: {path}"

# general type for que and como
# lambda que puedes ...
# lambda como puedo ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# define a message for system
	system_text = """Eres un asistente de IA. Te voy a presentar un manual de comandos con ejemplos y descripciones de las funciones. Responde a las preguntas badado en la estructura y ejemplos de los comandos de las funciones. Usa lenguaje markdown para remarcar las partes importantes del comando de la función. Si te preguntan como pueden hacer algo, responde con ejemplos de como usar el comando de la función. Además brinda detalles de la función. Si te preguntan que puedes hacer, da una lista breve de las funciones más interesantes de la lista y lo que estas pueden hacer. El manual de las funciones es el siguiente:

		Primero que nada, si quieres usar archivos en tus funciones: como PDFs, audios o imágenes, primero sube tu archivo al chat de discord, y luego manda el mensaje para usar la función, automáticamente se detectará el ultimo archivo que hayas subido. Los formatos aceptados son .pdf .jpeg .jpg .png .heic .mp3 .wav .ogg\n\n""" + read_file(global_resume)
	# passs the message and the system_text
	return openai.gpt(message, model="gpt-3.5-turbo-16k", context=False, system=system_text)

# theres no info, this is the function that uses all the info
info = """
"""