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
### Conversation
Esta función es la que ocupa lambda para las conversaciones, también es implementada en el comando de "_Lambda, ..._". Permite tener conversaciones con _gpt3.5-turbo_.
> **Comando:** Lambda dime algo [sobre o acerca] ...
> **Ejemplo:** lambda dime algo sobre los agujeros negros

"""