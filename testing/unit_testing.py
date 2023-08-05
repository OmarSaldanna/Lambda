# a script to test lambda app
import requests
import time
import json


def test(headers: dict, Id: str, api="/lambda"):
	# Record the start time
	start_time = time.time()
	# set the api url
	lambda_api = 'http://127.0.0.1:8080' + api
	# set the variable
	ans = []
	# try to call lambda
	try:
		ans = requests.get(
			lambda_api,
			headers=headers
		)
		ans = ans.json()
	except:
		print("error")
		return False

	# Record the end time
	end_time = time.time()
	# Calculate the time taken
	time_taken = end_time - start_time
	# return the answer and the time
	return Id, ans['answer'], time_taken