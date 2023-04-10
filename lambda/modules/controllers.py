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



# here is where the gpt call comes
def discord_gpt(msg):
	print("[BRAIN] -> Using gpt3:")
	# return the answer from gpt3
	return ai.gpt3(msg)

def discord_comm(msg):
	print("jaja")