from core.modules import OpenAI


# Lambda dime mi uso
# Lambda dame mis recursos
# Lambda muestra mi disponibilidad
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module, here we have the usage in user_data
	openai = OpenAI(member, server)
	# now, user data is located in openai.user_data
	# then read the usage
	usage = openai.user_data['usage']
	# format the answer
	ans = [{
		"type": "error",
		"content": f"**Estos son tus recursos disponibles:**"
	}]
	for resource in usage.keys():
		ans.append({
			"type": "text",
			"content": f"* {resource}: **{usage[resource]}**"
		})
	# and send the answer
	return ans

# info about the skill
info = """
### Show Usage
Esta función sirve para **mostrar cuantos recursos de Lambda te quedan por usar: imágenes, tokens de conversación, archivos en la nube, audios** y lo demás que lambda cuente como uso. Esta te ayudará a que vayas midiendo tu uso de Lambda.
> **Comando:** Lambda **[verbo]** mi **[sustantivo]** ...
> **Ejemplo:** Lambda dime mi uso
> **Ejemplo:** Lambda dame mis recursos
> **Ejemplo:** Lambda dame mi uso
> **Ejemplo:** Lambda muestra mi disponibilidad
> **Verbos:** _dime, dame, muestra_
> **Sustantivos** _uso, disponibilidad, recursos_
"""