import json
# the lambda modules: ai and memory
from modules.brain import AI
from modules.memory import Memory

# the memory files
def get_memory(mem):
	memory_files = {
		'game': './lambda/modules/data/game.json',
		'data': './lambda/modules/data/data.json',
		'vocab': './lambda/modules/data/vocab.json',
		'memory': './lambda/modules/data/memory.json',
	}
	# returns a memory instance, this way the controlers
	# will read the brand new changes made for themselves
	return Memory(memory_files[mem])
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
#       Game functionality                    #
###############################################
###############################################

# determins the number of players that are going to
# recieve points for correct answers. The value will
# be set in base of the total of players, like 0.5.
first_ones = int(game_db['state']['first ones'])


def add_player(player):
	# expected tuple (anme, id)
	name, _id = player
	# search the existing players in the db
	players = game_db['players']
	# check that the player id does no exist
	exists = False
	for player in players:
		# if the id exists
		if player['id'] == _id:
			print(f"[MEMORY] -> repeated player {_id}")
			exists = True
			break
	# the id exists
	if exists:
		return "Player Already Exists"
	# the id don't exist
	else:
		# add the new player
		new_player = {'id': _id, 'name':name, 'points': '0'}
		game_db['players'].append(new_player)
		game_db.write()
		print(f"[MEMORY] -> added player {_id}")
		return "Player Added Successfully"


def check_answer(ctx):
	# expected tuple (_id, challenge, answer)
	_id, challenge, answer = ctx
	# get the actual state: in case the request was sent
	# with a unexistant challenge number.
	actual_challenge = game_db['state']['challenge']
	if challenge != actual_challenge:
		return "Error: challenge number isn't the current one"
	print(ctx)
	print(actual_challenge)
	# then the answer was sent for the correct challenge
	# so it's needed to chech that the challenge is still
	# recieving answers. corrects counter < first_ones
	corrects_counter = int(game_db['challenges'][int(challenge)]['corrects'])
	# if the challenge isn't acepting answers
	if corrects_counter > first_ones:
		return "Error: challenge isn't acepting answers any more"
	# so, here the answer comes in time and to the correct 
	# challenge number. Finally it's needed to check if the
	# plater isn't in the winners list yet
	if _id in game_db['challenges'][int(challenge)]['winners']:
		return "Error: player is in the winners list"

	# Here, it was a new winner: then
	# add the answer sent to the answers list
	game_db['challenges'][int(challenge)]['answers'].append(
		{'id': _id, 'answer': answer}
	)
	# get the correct answer
	correct_answer = game_db['challenges'][int(challenge)]['answer']
	# check the answer
	if answer == correct_answer:
		print(f"[MEMOR][GAME] -> Detected correct answer from {_id} to challenge {challenge}")
		# since the answer was correct, add the points
		player_idx = find_player_idx(_id)
		points = calculate_score(corrects_counter)
		actual_points = int(game_db['players'][player_idx]['points'])
		game_db['players'][player_idx]['points'] = str(actual_points+points)
		# and add 1 to the corrects counter
		game_db['challenges'][int(challenge)]['corrects'] = str(corrects_counter + 1)
		game_db
		# add the player id to the winners
		game_db['challenges'][int(challenge)]['winners'].append(_id)
		# save all the changes
		game_db.write()
		return "correct"
	else:
		print(f"[MEMOR][GAME] -> incorrect answer from {_id} to challenge {challenge}")
		# save all the changes
		game_db.write()
		return "incorrect"

# depends on the actual corrects counter 
def calculate_score(place):
	# the points are based on the game rules
	# place will be the actual counter, the last will be 19
	if place == 0: # the first place
		return 4
	elif place < 6:
		return 3
	elif place < 12:
		return 2
	elif place < 19:
		return 1

# returns the player id
def find_player_idx(_id):
	for i,player in enumerate(game_db['players']):
		if _id == player['id']:
			return i
	return False

# this is for the challenge web settings
def generate_settings():
	settings = {}
	settings['host'] = game_db['settings']['lambda api']
	# if the sets are going for the login	
	settings['title'] = game_db['settings']['title']
	# now the ch
	current_challenge = int(game_db['state']['challenge'])
	for i in range(4):
		display = 'block' if i<=current_challenge else 'none'
		settings[f'ch{i+1}'] = display
		# and the links for each challenge
		settings[f'link{i}'] = f"http://127.0.0.1:8000/game/challenge/{i}"
	return settings