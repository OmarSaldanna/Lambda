# a script to test lambda app
import requests
import json
import os

# os.system('clear')

# general function to make requests
def request(type_: str, api: str, headers: dict):
	api = f'http://127.0.0.1{api}'
	# prepare the dic
	for key in headers.keys():
		# if there's a dic in headers
		if type(headers[key]) == dict:
			# json dump
			headers[key] = json.dumps(headers[key])
	# make the request based on type
	if type_ == 'GET':
		return requests.get(api, headers=headers).json()
	elif type_ == 'POST':
		return requests.post(api, headers=headers).json()
	elif type_ == 'PUT':
		return requests.put(api, headers=headers).json()
	else:
		raise ValueError('Type of request unknown')

api = ':8081/verbs'
headers = {
	#"data": "lambda reboot",
	'verb': 'dime',
	#'db': 'bin',
	'data': {
		# FOR MEMBERS DB
		#'role': 'member',
		#"usage": {
	    #    "images": 0,
	    #    "context": 0
	    #},
	    #"images": ['107071120175595.png'],
	    #"variations": ['107071120175595.png', '107071120175595.png']
	    ##############################
	    # FOR SERVERS DB
	    #"lockdown_channel": "animesito",
  		#"lockdown_members": ["1", "0"]
	    ##############################
	    # FOR FUNCTIONS
	    'type': 'general',
	    'function': 'conversation',
	    #'anagrana': 'generate_anagrama',
	    ##############################
	    # FOR ERRORS
	    #"call": "lambda crea que no se",
 		#"code": "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.",
 		#"member": "102910",
 		#"server": "multiusos"
	}
}

# member db working and images
# servers db working
# verbs db working
# logs db working
print(request('POST', api, headers)['answer'])