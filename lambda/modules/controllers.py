import json
# the lambda modules: ai and memory
from modules.brain import AI
from modules.memory import Memory

# the memory files
data = Memory('./lambda/modules/data/data.json')
#memory = Memory('./lambda/modules/data/memory.json')
vocab = Memory('./lambda/modules/data/vocab.json')
game_db = Memory('./lambda/modules/data/game.json')

# and the ai
tokens = json.load(open('./info.json'))
ai = AI(tokens['OPENAI'])


# here the general commands come
# main function to process the messages
def discord_msg(msg):
	# determine the command type
	command_type, word = determine_command_type(msg)
	print(word)
	# if it's a question, let gpt3 answer
	if command_type == "question":
		# use gpt3
		print("using gpt3")
		return ai.gpt3(msg)
	else:
		# special funcions
		pass

# it can be an order or a question
def determine_command_type(msg):
	# the verb will be the word after lambda
	verb = msg.split(' ')[0]
	# then compare the verb with the known verbs
	word = ai.recognize_word(verb, vocab['verbos'])
	# there were no coincidence
	if not word:
		return "question", 0
	else: 
		return "order", word


# a verb was found, so the goal is to search the
# object of the sentence to use the action
def determine_service(sentence, verb):
	pass


###############################################
###############################################
#		Game functionality                    #
###############################################
###############################################

def append_player(player):
	#expected tuple (anme, id)
	name, _id = player
	# first verify if the player isn't repeat
	if _id not in game_db['ids']:
		# add the player
		game_db['jugadores'].append(name)
		game_db['ids'].append(_id)
		# save changes
		game_db.write()
		print(f"\n[MEMORY] -> Player {_id} registered")
		return True
	else:
		print(f"\n[MEMORY] -> Player {_id} repeated")
		return False