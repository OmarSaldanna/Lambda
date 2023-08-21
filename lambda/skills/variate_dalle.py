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


# info about the skill
info = """
### Image Variation
Esta función sirve para generar variaciones (NO EDICIONES) de imágenes, por inteligencia artificial. Básicamente hace pequeños cambios en las imágenes. La imagen para variar debe ser proporcionada con una ID, incluyendo el símbolo de "_$_".
> **Comando 1:** Lambda [crea, genera, dame] [una. dos o tres] [variación o variaciones] de $ID
> **Comando 2:** Lambda varía [una. dos o tres] [imagen o imágenes] de $ID
> **Ejemplo:** lambda crea dos variaciones de $000000
> **Ejemplo:** Lambda varía una imagen de $000000

"""