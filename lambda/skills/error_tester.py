# a simple function that throws error, this is
# to test the error module

# lambda dame un error de ...
def main(params: tuple):
	# extract the discord params
	message, member, server = params
	# get the message
	error_msg = message.split(' ')[4:]
	error_msg = " ".join(error_msg).strip()
	# raise error with the message
	raise ValueError(error_msg)

# info about the skill
info = """
Error Tester 
De las primeras funciones incorporadas en Lambda para prpobar su estabildad, usarla generará un error, que será notificado al Admin por mensaje, el contenido de dicho será el texto del error.
Comando:Lambda [dame] un [error] de [texto del error]
Ejemplo:lambda dame un error de caramón camarelo
"""