from core.modules import OpenAI


# Lambda limpia mi contexto
# Lambda borra mi contexto
# Lambda resetea mi contexto
# Lambda vacia mi contexto
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module, to use it to handle the db
	# in an pretty easy way
	openai = OpenAI(member, server)
	# now, user data is located in openai.user_data
	# so, clear the context and just leave the personality
	# as simple as that, since the new users are created like that
	openai.user_data['context'] = [{
		"role": "system", "content": openai.user_data['personality']
	}]
	# also set the context size to 0
	openai.user_data['context_len'] = 0
	# finally save changes
	openai.set_user_data({
		"context_len": openai.user_data['context_len'],
		"context": openai.user_data['context'],
	})
	# and send an advice
	return [{
		"type": "error",
		"content": f"Listo <@{member}>"
	}]


# info about the skill
info = """
Limpiar Conversación
Esta función borra el contexto almacenado, es decir, Lambda borra tu historial de conversación (manualmente). Esta función es recomendable para cuando quieres hablar con lambda sobre un tema diferente, pues te permite empezar una nueva conversación.
Comando:** Lambda [limpia|borra|resetea|vacía] mi [contexto|conversación|chat|charla|plática]
Ejemplo:** Lambda limpia mi contexto
Ejemplo:** lambda borra el chat
Ejemplo:** lambda vacía nuestra plática
"""