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