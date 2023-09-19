from core.modules import OpenAI


# edita una imagen de $imagen con $mascara y ...
# genera|crea|dame un edit de $imagen con $mascara y ...
def main(params: tuple):
	# catch params
	message, author, server = params
	words = message.split(' ')
	
	# second word is the number of images
	second_word = words[1]
	# count the number of images
	quantity = 1
	# una was skipped
	if second_word == 'dos':
		quantity = 2
	if second_word == 'tres':
		quantity = 3

	# catch the img id
	img_id = words[4][1:]
	# then get the image path
	img_path = f"lambdrive/images/{img_id}.png"

	# catch the mask
	mask_id = words[6][1:]
	# then get the image path
	mask_path = f"lambdrive/images/{mask_id}.png"
	
	# get the prompt
	prompt = ' '.join(words[8:])	

	# instance the openai object to use models
	openai = OpenAI(author, server)
	# use dalle to edit the image
	answer = openai.edit_image(img_path, mask_path, prompt, n=quantity)
	answer.append({'type': 'error', 'content': prompt})
	answer.append({'type': 'error', 'content': "img path: " + img_path})
	answer.append({'type': 'error', 'content': "mask path: " + mask_path})
	# return all the image links
	return answer


# info about the skill
info = """
### Image Edition
Esta imagen permite editar imágenes con inteligencia artificial. Para esto se le deben de proporcionar **dos imágenes**, la primera es la imagen original y la segunda debe de ser una "_máscara_" que es **una imagen recortada de donde quieres editar la imagen**. Además debes de dar una descripción de que es lo que deseas editar de la imagen. Puedes **agregar objetos, quitarlos, cambiar la forma de algo y más cosas**.
> **Comando 1:** Lambda edita una imagen de **$imagen** con **$mascara** y ...
> **Comando 2:** Lambda **[genera|crea|dame]** un **edit** de **$imagen** con **$mascara** y ...
> **Ejemplo:** lambda edita una imagen de $0a1029 con $0a1028 y a sunlit indoor lounge area with a pool containing a flamingo
> **Ejemplo:** Lambda dame dos edits de $0a1029 con $0a1028 y a sunlit indoor lounge area with a pool containing a flamingo
> **Notas:** para buenos resultados las imágenes **deben de ser cuadradas y de las mismas dimensiones**: 1024x1024. **Para recortar las imágenes puedes usar los siguientes links:**
* Para hacer las imágenes cuadradas: [iloveimg.com](https://www.iloveimg.com/crop-image/crop-png)
* Para recortar la zona para editar: [onlinepngtools.com](https://onlinepngtools.com/erase-part-of-png)

"""