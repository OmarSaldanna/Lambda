# the lambda modules: ai, memory and telegram interface
from modules.brain import AI
from modules.memory import get_memory, app_to_log
from modules.telegram import Bot


# load the keys, ports and tokens
info = get_memory('info')

# set the ai and telegram
ai = AI(info['OPENAI'])
# telegram = Bot(info['TELEGRAM'],info['TELEGRAM_CHATS']['group'])


# here is where the gpt call comes
def discord_gpt(msg):
	log = "[BRAIN] -> Using gpt3:"
	# return the answer from gpt3
	return ai.gpt3(msg), log

def discord_comm(msg):
	print("jaja")