from core.modules import OpenAI


# Lambda dime mi uso
# Lambda dame mis recursos
# Lambda muestra mi disponibilidad
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module, here we have the usage in user_data
	openai = OpenAI(member, server)
	# for client names
	names = {
		"gpt-3.5-turbo": "Conversación",
		"gpt-3.5-turbo-16k": "Lectura de textos largos",
		"gpt-4-turbo-preview": "GPT-4 y visión(respuestas)",
		"tts": "Generación de audios",
		"dalle": "Creación de Imágenes(no QRs)",
		"vision": "Visión inteligente",
		"whisper": "Oído inteligente"
	}
	# units
	units = {
		"gpt-3.5-turbo": "palabras (aprox.)",
		"gpt-3.5-turbo-16k": "palabras (aprox.)",
		"gpt-4-turbo-preview": "palabras (aprox.)",
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
		# to calculate from tokens to words
		if resource.startswith('gpt'):
			text += f"* **{names[resource]}:** {usage[resource]*0.75} {units[resource]}\n"
		# to other models
		else:
			text += f"* **{names[resource]}:** {usage[resource]} {units[resource]}\n"
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