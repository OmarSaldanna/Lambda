import qrcode
from modules.utils import generate_hash

# 
# crea|genera un qr de|con www.google.com
def main(params: tuple):
	message, author, server = params
	# create QR code instance
	qr = qrcode.QRCode(version=1, box_size=10, border=5)
	# split the message
	splited_message = message.split(' ')
	# select the qr content
	data = ' '.join(splited_message[4:])
	# add data to QR code
	qr.add_data(data)
	qr.make(fit=True)
	# create image from QR code
	img = qr.make_image(fill_color="black", back_color="white")
	# create a hash to save the file
	h = generate_hash(data)
	# save image on lambdrive/qrs
	img.save(f"lambdrive/{author}/generated/{h}.png")
	# and return the messages
	return [{
		"type": "file",
		"content": f"lambdrive/{author}/generated/{h}.png"
	}]



# info about the skill
info = """
Generar QRs
Esta función se encarga de generar códigos QR de links o de textos. Solo proporciona el contenido del QR y Lambda lo creará.
Comando:Lambda [crea|genera|dame] un [QR|qr] de [contenido del QR]
Ejemplo:Lambda crea un qr de https://www.youtube.com/watch?v=J---aiyznGQ
Ejemplo:lambda crea un QR de mensaje para el qr
"""