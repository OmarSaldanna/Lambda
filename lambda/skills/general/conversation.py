from core.modules import OpenAI


# lambda dime algo sobre ...
# lambda dime algo acerca ...
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module
	openai = OpenAI(member, server)
	# try to make the answer shorter as possible
	message += ". Que tu respuesta sea breve y concisa."
	# now call gpt
	return openai.gpt(message)


# info about the skill
info = """
Conversation
Esta función es la que ocupa lambda para las conversaciones, también es implementada en el comando de "Lambda, ...". Permite tener conversaciones con gpt 3.5-turbo.
Comando 1:Lambda [dime] algo [sobre|acerca] [algún tema]
Comando 2:Lambda, [preguntas o conversación]
Ejemplo:lambda dime algo sobre los agujeros negros
Ejemplo:lambda, cuál es la capital de Perú?
"""