# a script to test lambda app
import requests
import time
import json

# Record the start time
start_time = time.time()

headers={
	#"message": "crea una imagen de photo of slim asian girl, 20yo, close-up, high detail, studio, smoke, sharp, pink violet light, studio, 85mm sigma art lens",
	#"message": "crea un qr de www.google.com",
	#"message": "crea una imagen de photo of a christmas cat",
	"message": "cual es la capital de Perú",
	"server": "11",
	"author": "11"
}

try:
	ans = requests.get(
		'http://127.0.0.1:8080/lambda/chat',
		headers=headers
	)
	print('\n',ans.json(),'\n')
except:
	print("error")

# Record the end time
end_time = time.time()

# Calculate the time taken
time_taken = end_time - start_time
print(f"Time taken: {time_taken:.6f} seconds")