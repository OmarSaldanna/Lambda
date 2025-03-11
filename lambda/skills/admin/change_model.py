# import the ai, that has info of models and also db module
from core.ai import AI


# Lambda usa {modelo} para {modo} (GENERAL)
def main(params: tuple):
	# extract the params
	message, member, server = params
	# get the model and the mode from the message
	model = message.split(' ')[1]
	mode = message.split(' ')[3]
	# instance ai
	ai = AI(member, server)
	# check mode and model in system options
	if model not in ai.models_info["models"].keys():
		return {
			"type": "error",
			"content": f"Modelo {model} no encontrado"
		}
	if mode not in ai.user_data["models"].keys():
		return {
			"type": "error",
			"content": f"Modo {mode} no encontrado"
		}
	# set changes
	ai.user_data["models"][mode] = model
	# save the changes
	ai.db.put('/members', {
		"id": member,
		"data": {
			# set the models
			"models": ai.user_data["models"]
		}
	})
	# and send an advice
	return [{
		"type": "advice",
		"content": f"Usando {model} para {mode}"
	}]