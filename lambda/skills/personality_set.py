from core.modules import OpenAI


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
	# instance openai module, to use it to handle the db
	# in an pretty easy way
	openai = OpenAI(member, server)
	# now, user data is located in openai.user_data
	# set the new personality
	openai.user_data['personality'] = new_personality
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
		"personality": openai.user_data['personality'],
	})
	# and send an advice
	return [{
		"type": "error",
		"content": f"Listo <@{member}>"
	}]


# info about the skill
info = """
Ajuste de Personalidad 
Permite ajustar la "personalidad" con la que Lambda responde, podrás pedir que Lambda responda como algún célebre científico, como un poeta o literario, o que responda con sarcasmo o entusiasmo. Además podrías pedirle que escriba en manera de lista, remarque conceptos, etc. Esta función elimina la conversación y esta vuelve a empezar desde cero.
Comando:Lambda **[cambia|ajusta|resetea|edita] tu [personalidad] a [descripción]
Ejemplo:Lambda cambia tu personalidad a Eres un poeta renacentista y quiero que a todas mis preguntas respondas con un refinado uso del lenguaje y con el contexto humanista y antropocentrista destacado del renacimiento
Ejemplo:lambda ajusta la personalidad a Simula la personalidad de Stephen Hawking, a todas las preguntas y temas de conversación responde con su elocuencia, humor y ocupa el refinado lenguaje de un científico. Da respuestas profundas y detalladas
"""