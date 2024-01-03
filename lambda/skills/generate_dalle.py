from core.modules import OpenAI
from core.models.lwr import Lambda_Word_Recognizer as LWR

# crea|genera una imagen [horizontal|vertical|cuadrada] de ...                    
def main(params: tuple):
	# catch params
	message, author, server = params
	# everything after the fourth word
	prompt = message.split(' ')[5:]
	prompt = ' '.join(prompt)
	# select the image type with LWR
	mode = message.split(' ')[3]
	recognizer = LWR()
	# train the LWR
	recognizer.train(["horizontal", "vertical", "cuadrada"])
	# and recognize
	sizes = {
		"horizontal": "1792x1024",
		"vertical": "1024x1792",
		"cuadrada": "1024x1024"
	}
	size = sizes[recognizer(mode)]
	# instance the answer
	answer = []
	# instance the openai object to use models
	openai = OpenAI(author, server)
	# create the images with dalle
	#urls = 'ok'
	answer = openai.create_image(prompt, size=size)
	# return all the image links
	return answer


# info about the skill
info = """
### Image Generator
Esta función es la que crea imágenes con DALL-E 3. Preferentemente las descripciones de las imágenes deben de ser en inglés, esto hará que el resultado sea más preciso. **El modelo actual solamente permite crear una imagen a la vez**. Además ahora podrás crear imagenes en formatos vertical, horizontal y cuadrado.
> **Comando:** Lambda [crea, genera o dame] una imagen [horizontal, vertical o cuadrada] de ...
> **Ejemplo:** lambda crea una imagen horizontal de Porsche Origami
> **Ejemplo:** Lambda genera una imagen cuadrada de gato en la sala, al lado de la chimenea al atardecer, nevando, casa de madera, foto casera en navidad

"""