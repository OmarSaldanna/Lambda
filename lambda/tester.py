# a script to test lambda app
import requests


user = input("your user: ")


while True:
	msg = input("message: ")
	if msg == ';':
		break
	else:
		ans = requests.get(
			'http://127.0.0.1:8080/lambda', 
			headers={
				"message": msg,
				"author": user
			}
		)
		print('\n',ans.json(),'\n')
