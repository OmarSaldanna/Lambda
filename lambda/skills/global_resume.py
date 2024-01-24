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
	system_text = """Eres un asistente de IA. Basado en un manual de "comandos" proporcionado sobre el uso de una IA mediante un chat, quiero que respondas como el soporte técnico de una empresa de tecnología. TE HARÁN PREGUNTAS COMO:

		1) cómo hacer ciertas cosas o cómo usar una función: RESPONDE EN TRES PÁRRAFOS CORTOS. En el primero escribe LO QUE HACE LA FUNCIÓN. En el segundo escribe EJEMPLOS DE COMO USAR LA FUNCIÓN, remarca las palabras importantes con NEGRITAS EN MARKDOWN. fianalmente en el tercero escribe el COMANDO DE LA FUNCIÓN y también remarca las palabras importantes con NEGRITAS EN MARKDOWN.
		2) que sabes hacer o cuales son tus funciones: RESPONDE EN FORMA DE LISTA MARKDOWN, lista en la que hables BREVEMENTE, pero NO ESCRIBAS NADA SOBRE LOS COMANDOS O EJEMPLOS de las funciones del manual: la visión inteligente, las de PDFs, todas las que usen Audios, la de preguntas a youtube y las que te MÁS TENGAN QUE VER CON LA PREGUNTA. En general QUE ESTA RESPUESTA SEA EXTENSA, REMARCA LAS KEYWORDS EN NEGRITAS.
	"""
	# define the user message
	message += '. RECUERDA REMARCAR EN NEGRITAS LAS KEYWORDS. El manual de funciones es el siguiente:\n\n' + read_file(global_resume)
	# passs the message and the system_text
	return openai.gpt(message, model="gpt-3.5-turbo-16k", context=False, system=system_text)

# theres no info, this is the function that uses all the info
info = """
"""