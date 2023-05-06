# the lambda modules: ai, memory and telegram interface
from modules.brain import AI
from modules.telegram import Bot
from modules.memory import get_memory, app_to_log


# load the keys, ports and tokens
info = get_memory('info')

# set the ai and telegram
ai = AI(info['OPENAI'])
# telegram = Bot(info['TELEGRAM'],info['TELEGRAM_CHATS']['group'])


# here is where the gpt call comes
def discord_gpt(msg):
	# return the answer from gpt3
	return ai.gpt3(msg)

# generate images with DALL-E
def discord_dalle(msg):
	# return the link for the generated image
	return ai.dalle(msg)

def discord_comm(msg):
	print("jaja")