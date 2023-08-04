from core.modules import OpenAI


# crea|genera una imagen de ...
def main(params: tuple):
	# catch params
	message, author, server = params
	# everything after the fourth word
	prompt = message.split(' ')[4:]
	prompt = ' '.join(prompt)
	# second word is the number of images
	second_word = message.split(' ')[1]
	# count the number of images
	quantity = 1
	# una was skipped
	if second_word == 'dos':
		quantity = 2
	if second_word == 'tres':
		quantity = 3
	# start writing the answer
	answer = []
	# instance the openai object to use models
	openai = OpenAI(author)
	# create the images with dalle
	#urls = 'ok'
	answer = openai.create_image(prompt, quantity)
	# return all the image links
	return answer