# to handle the db
from modules.db import DB

# Lambda cambia mi personalidad a ...
# Lambda resetea mi personalidad a ...
# Lambda cambia mi personalidad a ...
# Lambda edita tu personalidad a ...
def main(params: tuple):
	# extract the params
	message, member, server = params
	# get the personality from the message
	words = message.split(' ')[4:]
	new_personality = ' '.join(words)
	# instance the db
	db = DB()
	# save the changes
	db.put('/members', {
		"id": member,
		"data": {
			# clear the context and only keep the new personality
			"context": [{"text": new_personality}],
			# and the context size
			"context_size": 0
		}
	})
	# and send an advice
	return [{
		"type": "advice",
		"content": f"Nueva Personalidad Guardada"
	}]


# info about the skill
info = """
Ajuste de Personalidad 
Permite ajustar la "personalidad" con la que Lambda responde, podrás pedir que Lambda responda como algún célebre científico, como un poeta o literario, o que responda con sarcasmo o entusiasmo. Además podrías pedir respuestas más breves, conceptos remarcados, y más. 
Comando:Lambda **[cambia|ajusta|resetea|edita] tu [personalidad] a [descripción]
Ejemplo:Lambda cambia tu personalidad a Eres un poeta renacentista y quiero que a todas mis preguntas respondas con un refinado uso del lenguaje y con el contexto humanista y antropocentrista destacado del renacimiento
Ejemplo:lambda ajusta la personalidad a Simula la personalidad de Stephen Hawking, a todas las preguntas y temas de conversación responde con su elocuencia, humor y ocupa el refinado lenguaje de un científico. Da respuestas profundas y detalladas
"""