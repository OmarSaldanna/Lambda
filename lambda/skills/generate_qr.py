import qrcode
from core.modules import generate_hash

# crea|genera un qr de|con www.google.com
def main(params: tuple):
	message, author, server = params
	# create QR code instance
	qr = qrcode.QRCode(version=1, box_size=10, border=5)
	# select the qr content
	data = message.split(' ')[-1]
	# add data to QR code
	qr.add_data(data)
	qr.make(fit=True)
	# create image from QR code
	img = qr.make_image(fill_color="black", back_color="white")
	# create a hash to save the file
	h = generate_hash(data)
	# save image on lambdrive/qrs
	img.save(f"lambdrive/qrs/{h}.png")
	# and return the messages
	return [{
		"type": "file",
		"content": f"lambdrive/qrs/{h}.png"
	}]