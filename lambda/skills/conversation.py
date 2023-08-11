from core.modules import OpenAI
# gpt (self, prompt: str, model="gpt-3.5-turbo", temp=0.5, context=True, system="Eres alguien inteligente")

# simple function to talk with lambda
def main(params: tuple):
	# extract the params
	message, member, server = params
	# instance openai module
	openai = OpenAI(member, server)
	# try to make the answer shorter as possible
	message += ". Que tu respuesta sea breve y concisa."
	# now call gpt
	return openai.gpt(message)