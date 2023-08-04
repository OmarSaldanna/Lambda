from dotenv import load_dotenv
import openai
import os

# models:
# gpt-3.5-turbo
# gpt-3.5-turbo-16k
# gpt-4

class OpenAI:

	# this function just sets the OpenAI token
	def __init__ (self, token=""):
		# set the token
		if token == "":
			# load the .env file
			load_dotenv(dotenv_path)
			# load the key
			openai.api_key = os.getenv("OPENAI")
		# set the given token
		else:
			openai.api_key = token


	# gpt genereal usage, it requires the messages structure
	def gpt(self, messages: list, temp=0.5, model="gpt-3.5-turbo"):
		res = openai.ChatCompletion.create(
			model=model,
			messages=messages,
			#[{"role": "system", "content": system},
			#{"role": "user", "content": prompt}]
			temperature=temp
			)
		return res['choices'][0]['message']['content']


	# simple gpt usage, it don't require the messages structure
	def fast_gpt(self, prompt: str, system: str, temp=0.5, model="gpt-3.5-turbo"):
		res = openai.ChatCompletion.create(
			model=model,
			temperature=temp,
			messages=[
				{"role": "system", "content": system},
				{"role": "user", "content": prompt}
			]
			)
		return res['choices'][0]['message']['content']

	# DALL-E function to generate images
	def dalle(self, prompt:str, n=1):
		response = openai.Image.create(
			prompt=prompt,
			n=n,
			size="1024x1024"
		)
		# return all urls
		urls = []
		for i in range(n):
			urls.append(response['data'][i]['url'])
		return urls

	# DALL-E function to generate variations of given images
	def variate(self, image_path: str, n=1):
		response = openai.Image.create_variation(
			image=open(image_path, "rb"),
			n=n,
			size="1024x1024"
		)
		# return all urls
		urls = []
		for i in range(n):
			urls.append(response['data'][i]['url'])
		return urls