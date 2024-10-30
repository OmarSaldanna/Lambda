import subprocess
import secrets
import os


# Simple module to use the .auth file. It's used inside Lambda to check
# if the requests have a valid API KEY.

class Auth:

	def __init__ (self, file=os.environ["AUTH_PATH"]):
		self.file = file
		# length of the generated api keys
		self.api_key_length_generate = int(os.environ["API_KEY_LENGTH_GENERATE"])
		self.api_key_length_check = int(os.environ["API_KEY_LENGTH_CHECK"])
		# and user id
		self.user_id_length = int(os.environ["USER_ID_LENGTH"])

	# function used to run the bash: cat .auth | grep $pattern and also a wc -l
	# and returns only the number
	def __grep (self, pattern: str, wc=False):
		 # create the process
		process = subprocess.Popen(f"cat {self.file} | grep '{pattern}' {'| wc -l' if wc else ''}", shell=True, stdout=subprocess.PIPE)
		# get the output
		output = process.stdout.read().decode('utf-8')
		# and the number
		return int(output[7]) if wc else output

	# used to prevent code injection in all the incomming params
	def __verification (self, value: str, standard_len: int):
		# if one of them is false, then return a forbindden access
		checks = [
			# has not the specified length
			len(value) == standard_len,
			# has no spaces
			' ' not in value
		]
		# finally make the check
		return False if False in checks else True

	# main function to create api keys and store them with their respective user_id
	# saved as 'user_id Api_key'. Mostly used where users create them api keys.
	def new_api_key (self, user_id: str, server_api_key: str):
		# run the verification for the incomming value
		if not self.__verification(user_id, self.user_id_length):
			return False
		# also for the server_api_key
		if not self.__verification(server_api_key, self.api_key_length_check):
			return False
		# finally verify if the request comes with the lambda server_api_key
		if server_api_key != os.environ["LAMBDA_API_KEY"]:
			return False
		# if the value was passed as ok
		# create a key that starts with la-
		key = 'la-' + secrets.token_urlsafe(self.api_key_length_generate)
		# check that the user doesn't exist on db
		appears = self.__grep(user_id, wc=True)
		if appears >= 1: # >= because there may be rare errors
			# then remove the user from the file before creating
			# the new api key
			with open(self.file, "r") as f:
				# also make a secondary file
				with open("auth.tmp", "a") as tmp:
					# read the lines
					lines = f.readlines()
					# iterate the lines
					for l in lines:
	    				# write all the lines except for the user_id one
						if l[:self.user_id_length] != user_id:
							tmp.write(l)
	            	# finally save the user with its api key
					tmp.write(f"{user_id} {key}\n")
					# move the tmp file to the original
					os.system(f"mv auth.tmp {self.file}")
		# if the user is new
		else:
        	# just append the new line
			with open(self.file, "a") as f:
				# save the user with its api key
				f.write(f"{user_id} {key}\n")
        # finally return the api key
		return key

    # main function used to check if an api key
	def look_for (self, api_key: str):
		# run the verification for the incomming api_key
		if not self.__verification(api_key, self.api_key_length_check):
			return False
		# look for the api_key in the file
		appears = self.__grep(api_key, wc=True)
		# if there were no matches or more than one
		if appears != 1:
			return False
		# a correct match, but may be the user id
		else:
			# then get the api_key, -1 to remove the \n
			db_api_key = self.__grep(api_key)[self.user_id_length+1:-1]
			# verify that they are the same, it can be an user_id
			if db_api_key == api_key:
				# finally return the user id
				return self.__grep(api_key)[:self.user_id_length]

	# extra function to detect null params
	def has_nulls (self, params: list):
		return True in [p in [None, ""] for p in params]

	# other extra function to prevent file saving on other locations
	def secure_filename (self, filename: str):
		return False if ".." in filename or "/" in filename else True;