from core.modules import OpenAI

# simple function to
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module
	openai = OpenAI(member)
	# try to make the answer shorter as possible
	message += ". Que tu respuesta sea breve y concisa."
	# now call gpt
	return openai.gpt(message)