import os
import json
import requests

# db class to interact
class DB:
	
	def __init__ (self, host=os.environ["DB_HOST"], port=os.environ["DB_PORT"]):
		# define the api url
		self.api = f'http://{host}:{port}'

	# preprocess headers
	def __preprocess (self, headers: dict):
		for key in headers.keys():
			# if there's a dic in headers
			if type(headers[key]) in [dict, list]:
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

	# delete request
	def delete (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.delete(self.api + api, json=headers).json()