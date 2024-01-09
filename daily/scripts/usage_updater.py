import requests


# db class to interact
class DB:
	"""
	Module to interact with the lambda database: verbs,
	members, servers, images, errors or logs:
	
	{ /members
		"db": "members|images",
		"id": "[id]",
		*"data": {data}
	}

	{ /servers
		"id": "[id]"
		*"data": {data}
	}

	{ /verbs
		"verb": "[verb]"
		"data": {
	       "type": "general|multi"
	 		"object": "function name",
			*"function": "function name"
			...
	 	}
	}

	{ /logs
		"db": "bin|admins|errors|general"
		"data": "message to add"
	}

	{ /errors
		"data": {
			"call": lambda call that generated the error
	 		"code": error code
	 		"member": user id
	 		"server": server
	 	}
	}
	"""
	def __init__ (self, host='127.0.0.1', port='8081'):
		# define the api url
		self.api = f'http://{host}:{port}'

	# preprocess headers
	def __preprocess (self, headers: dict):
		for key in headers.keys():
			# if there's a dic in headers
			if type(headers[key]) == dict:
				# json dump
				headers[key] = json.dumps(headers[key])
		return headers

	# get request
	def get (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.get(self.api + api, json=headers).json()

	# post request
	def post (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.post(self.api + api, json=headers).json()

	# put request
	def put (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.put(self.api + api, json=headers).json()





# firts make the put of all users, this will discount a day
# in the days left counter