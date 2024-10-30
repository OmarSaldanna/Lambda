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
Generador de Imágenes
Esta función es la que crea imágenes con DALL-E 3. Proporciona las descripciones de las imágenes en inglés. El modelo actual solamente permite crear solo una imagen a la vez. Además ahora podrás crear imagenes en formatos vertical, horizontal y cuadrado.
Comando:Lambda [crea|genera|dame] una [imagen] [horizontal|vertical|cuadrada] de [descripción de la imagen]
Ejemplo:Lambda crea una imagen vertical de a professional architectural photograph of an innovative building with brutalist design, with plants on some balconies, solar panels, and some mini wind turbines, clear weather, hyper-realistic photo, ultra high quality
Ejemplo:Lambda crea una imagen cuadrada de a Rover picture on mars showing two moons at the distance and two suns
"""