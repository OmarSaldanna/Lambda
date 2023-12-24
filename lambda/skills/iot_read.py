# in case of use openai module
# from core.modules import OpenAI

def main(params: tuple):
	# catch params
	message, author, server = params
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# use gpt 
  	# return openai.gpt(message, system="Eres una IA capaz de hacer cálculos")
  	# or return something
	return [{
		"type": "text",
		"content": "ok"
	}]


# info about the skill
info = """
### title
description
> **Comando: command
> **Ejemplo: example
> **Verbos:** verbs
"""