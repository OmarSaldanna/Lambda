from core.modules import OpenAI


# 0     1      2        3  4   5   6
# edita [tres] imágenes de $id con ...
# 0                1    2         3  4   5   6
# dame|crea|genera tres ediciones de $id con ...

def main(params: tuple):
	# catch params
	message, author, server = params

	# second word is the number of images
	second_word = message.split(' ')[1]
	# count the number of images
	quantity = 1
	# una was skipped
	if second_word == 'dos':
		quantity = 2
	if second_word == 'tres':
		quantity = 3

	# catch the img id
	img_id = message.split(' ')[4][1:]
	# then get the image path
	img_path = f"lambdrive/images/{img_id}.png"

	# now catch the prompt
	# everything after the sixth word
	prompt = message.split(' ')[6:]
	prompt = ' '.join(prompt)
	
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# use dalle to edith the image
	answer = openai.create_image(img_path, prompt, quantity)
	# return all the image links
	return answer