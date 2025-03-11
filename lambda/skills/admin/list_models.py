# to handle the db
from core.ai import AI

# Lambda lista los modelos, ias, llms
# Lambda muestra los modelos
# Lambda dame los modelos
# lambda dime los modelos disponibles
def main(params: tuple):
	# extract the params
	message, member, server = params
	# get the models, so instance AI
	ai = AI(member, server)
	# leer los modelos
	models = list(ai.models_info["models"].keys())
	# and send the available models
	return [{
		"type": "info",
		"content": "Modelos Disponibles:\n" + "\n> ".join(models)
	}]