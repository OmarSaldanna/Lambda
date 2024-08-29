
# lambda dime mi id
# lambda dame mi id
# lambda muestra mi id
def main(params: tuple):
	# catch the params
	message, author, server = params
	# and return the messages
	return [{
		"type": "error",
		"content": f"<@{author}> tu id es:"
	},
	{
		"type": "text",
		"content": f"```{author}```"
	}]


# info about the skill
info = """
Obtener ID
Esta función permite al usuario mostrarle su ID de discord. Esta ID se utiliza para otras funciones de Lambda, como las conexiones de IoT para robótica. Además quizá te la pida un admin para registrarte.
Comando:Lambda [dame|dime|muestra] mi [id]
Ejemplo:lambda dame mi id
Ejemplo:lambda muestra mi id
"""