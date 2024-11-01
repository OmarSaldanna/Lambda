# Lambda's OpenAI module
from core.modules import OpenAI
# file that contains the "info" of all the modules
global_resume = "lambda/skills/skill_commands.txt"


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

# lambda como puedo ...
# lambda dime que función ...
# lambda dime con que ...
# dame mas detalles ...
# same for ejemplo, info, informacion
# same for verb dime
def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# define a message for system
	system_text = """Eres un asistente de IA. Basado en un manual de "comandos" proporcionado sobre el uso de una IA mediante un chat, quiero que respondas como el soporte técnico de una empresa de tecnología. Responde en formato Markdown."""
	# define the user message
	message += '. Responde con el formato Markdown. El manual de funciones es el siguiente:\n\n' + read_file(global_resume)
	# passs the message and the system_text
	return openai.gpt(message, model="gpt-3.5-turbo-16k", context=False, system=system_text)

# theres no info, this is the function that uses all the info
info = """
"""