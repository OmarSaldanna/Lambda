from core.modules import OpenAI


# 0     1      2        3  4   5   6
# varia [tres] imágenes de $id con ...
# 0                1    2           3  4   5   6
# dame|crea|genera tres variaciones de $id con ...

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
	
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# use dalle to edith the image
	answer = openai.variate_image(img_path, quantity)
	# return all the image links
	return answer