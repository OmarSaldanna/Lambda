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
### Error Tester
This function is for development purposes. Directly throws an error with a message.
> **Comando:** Lambda dame un error de ...
> **Ejemplo:** lambda dame un error de caramón camarelo

"""