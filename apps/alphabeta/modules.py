import json
import openai
import requests
from elevenlabs import set_api_key

# set elevenlabs api key
set_api_key(os.environ("ELEVENLABS"))

# voices:
voices = {
	'emidraw': 'r6uwdk8KbFRUhkvaThgv'
}

# general function to use lambda, is the same used in discord
def call_lambda(message: str, author: str, server: str, mode=""):
	# default lambda url for calls
	lambda_url = 'http://127.0.0.1:8080/lambda'
	# if it was a conversation request
	if mode == "chat":
		lambda_url = 'http://127.0.0.1:8080/lambda/chat'
	elif mode == "fast":
		lambda_url = 'http://127.0.0.1:8080/lambda/fast'

	# call lambda api
	answer = requests.get(
		lambda_url,
		json={
			"message": message,
			"author": author,
			"server": server
		}
	)
	return answer.json()


# convert the answer into a voice
def text_to_audio(text, voice_id='r6uwdk8KbFRUhkvaThgv'):
	CHUNK_SIZE = 1024
	url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

	headers = {
	  "Accept": "audio/mpeg",
	  "Content-Type": "application/json",
	  "xi-api-key": info['elevenlabs']
	}

	data = {
	  "text": text,
	  "model_id": "eleven_multilingual_v1",
	  "voice_settings": {
	    "stability": 0.4,
	    "similarity_boost": 1.0
	  }
	}

	file_name = f'lambdrive/audios/{hash(text)}.mp3'

	response = requests.post(url, json=data, headers=headers)
	with open(file_name, 'wb') as f:
	    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
	        if chunk:
	        	f.write(chunk)

	return file_name


def talk(message: str):
	# call lambda on conversation
	answer = call_lambda(message, "alphabeta", "0", mode="chat")["answer"][0]['content']
	# convert the answer to audio
	audio_file = text_to_audio(answer[0])
	# return the audio file
	return audio_file