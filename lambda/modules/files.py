import base64

# function to save an encoded to a file
def base64_to_file (base64_str, file_name):
	# decode the data
	decoded_data = base64.b64decode(base64_str)
	# and write the file
	with open(file_name, 'wb') as file:
		file.write(decoded_data)