import json
# the lambda modules: ai and memory
from modules.brain import AI
from modules.memory import Memory
from modules.telegram import Bot


# load the keys, ports and tokens
info = json.load(open('./info.json'))


# the memory files
def get_memory(mem):
	memory_files = {
		'data': './lambda/modules/data/data.json',
		'vocab': './lambda/modules/data/vocab.json',
		'memory': './lambda/modules/data/memory.json',
	}
	# returns a memory instance, this way the controlers
	# will read the brand new changes made for themselves
	return Memory(memory_files[mem])

# set the ai and telegram
ai = AI(info['OPENAI'])
telegram = Bot(info['TELEGRAM'],info['TELEGRAM_CHATS']['group'])


# here the general commands come
# main function to process the messages
def discord_msg(msg):
	# determine the command type
	command_type, word = determine_command_type(msg)
	print("")
	# if it's a question, let gpt3 answer
	if command_type == "question":
		# use gpt3
		print("[BRAIN] -> Using gpt3:")
		return ai.gpt3(msg)
	else:
		# special funcions
		print("using special function")
		pass

# it can be an order or a question
def determine_command_type(msg):
	# the verb will be the word after lambda
	# and the server recieves the words after lambda
	verb = msg.split(' ')[0]
	# read db
	vocab = get_memory('vocab')
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
