from core.modules import OpenAI


# Lambda dime mi uso
# Lambda dame mis recursos
# Lambda muestra mi disponibilidad
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module, here we have the usage in user_data
	openai = OpenAI(member, server)
	# units
	units = {
			"gpt-3.5-turbo": "tokens (aprox. 3 letras)",
			"gpt-3.5-turbo-16k": "tokens",
			"gpt-4": "tokens",
			"tts": "caracteres",
			"dalle": "imágenes",
			"vision": "imágenes",
			"whisper": "minutos"
	}
	# now, user data is located in openai.user_data
	# then read the usage
	usage = openai.user_data['usage']
	# format the answer
	ans = [{
		"type": "error",
		"content": f"**<@{member}> Estos son tus recursos disponibles:**"
	}]
	# send all in a text
	text = ""
	for resource in usage.keys():
		# add the resource lines to the text
		text += f"* {resource}: **{usage[resource]}** {units[resource]}\n"
	# add the text to the answer
	ans.append({"type": "text", "content": text})
	# and send the answer
	return ans

# info about the skill
info = """
Display de Recursos
Esta función sirve para mostrar cuantos recursos de Lambda te quedan por usar: imágenes, tokens de conversación, audios y lo demás que lambda cuente como uso. Esta te ayudará a que vayas midiendo tu uso de Lambda.
Comando:Lambda [dame|dime|muestra] mi [uso|disponibilidad|recursos]
Ejemplo:Lambda dime mi uso
Ejemplo:Lambda dame mis recursos
Ejemplo:Lambda dame mi uso
Ejemplo:Lambda muestra mi disponibilidad
"""