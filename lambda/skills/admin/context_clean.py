# to handle the db
from modules.db import DB

# Lambda limpia mi contexto
# Lambda borra mi contexto
# Lambda resetea mi contexto
# Lambda vacia mi contexto
# ---------------------------
# Lambda cambia la conversación
# Lambda cambia la plática
# Lambda cambia el tema
# asunto
def main (params: tuple):
	# extract the params
	message, member, server = params
	# instance the db
	db = DB()
	# get the user data
	user_data = db.get('/members', {
			"id": member,
			"server": server
	})['answer']
	# clear the context: only keep personality
	new_context = user_data["context"][0]
	# save the changes
	db.put('/members', {
		"id": member,
		"data": {
			# update the context
			"context": new_context,
			# and the context size
			"context_size": 0
		}
	})
	# and send an advice
	return [{
		"type": "advice",
		"content": f"Conversación Eliminada"
	}]


# info about the skill
info = """
Limpiar Conversación
Esta función borra el contexto almacenado, es decir, Lambda borra tu conversación. Esta función es recomendable para cuando quieres hablar con lambda sobre un tema diferente, pues te permite empezar una nueva conversación.
Comando:** Lambda [limpia|borra|resetea|vacía] mi [contexto|conversación|chat|charla|plática]
Ejemplo:** Lambda limpia mi contexto
Ejemplo:** lambda borra el chat
Ejemplo:** lambda vacía nuestra plática
"""