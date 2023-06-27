import json
import openai
import requests
from elevenlabs import set_api_key

info = {}

# read memory
with open("memory/info.json", "r") as json_file:
    # Load the JSON data from the file
    info = json.load(json_file)

# set the keys
openai.api_key = info['openai']
set_api_key(info['elevenlabs'])

# voices:
voices = {
	'emidraw': 'r6uwdk8KbFRUhkvaThgv'
}


# call lambda api
def call_lambda_conversation(message: str, usr="717071120175595631"):
	lambda_url = 'http://127.0.0.1:8080/lambda/conversation'
	# call lambda api
	answer = requests.get(
		lambda_url,
		headers={
			"message": message,
			"author": usr
		}
	)
	return answer.json()['content']

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
	answer = call_lambda_conversation(message)
	# convert the answer to audio
	audio_file = text_to_audio(answer[0])
	# return the audio file
	return audio_file