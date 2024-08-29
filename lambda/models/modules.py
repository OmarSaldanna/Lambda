# moduless
import os
import json
import requests
# open ai
from openai import OpenAI as OAI
# and tokenizer
import tiktoken

# image processing
from io import BytesIO
from PIL import Image


##########################################################################
################################# Modules ################################
##########################################################################


# models:
# gpt-3.5-turbo
# gpt-3.5-turbo-16k
# gpt-4-turbo-preview
class OpenAI:
	"""
	Module used to interact with OpenAI models
	like DALL-E, GPT3.5 and GPT4. Also it handles
	the users' context and personalities loaded.

	There are some rules in the GPT usage, these
	are to rule the way GPT models are used.

	FUNCTIONALITY BETWEEN MODELS
	* The messages will be answered based on the
	selected model
	* If the selected model has no tokens left, then
	change to other model that has tokens, notify
	the user this has happened
	* If all the models are out of tokens, then notify
	the user that he's out of tokens

	USER COMMANDS FOR MODELS
	* The current model and the usage will can be 
	shown with a command, also will show the remaining
	tokens of all the models
	* The current model will can be changed with a
	command
	"""
	# receives the user id only
	def __init__ (self, user_id: str, server: str):
		# set the user_id
		self.user_id = user_id
		# set the key
		# openai.api_key = os.getenv("OPENAI")
		# the instance of db
		self.db = DB()
		# the models, the order is by price - to +
		self.models = [
			"gpt-3.5-turbo",
			"gpt-3.5-turbo-16k",
			"gpt-4-turbo-preview"
		]
		self.metrics = {
			"gpt-3.5-turbo": "conversación",
			"gpt-3.5-turbo-16k": "documentos, videos o audios",
			"gpt-4-turbo-preview": "gpt-4 o visión de imágenes"
		}
		# get the user data
		self.user_data = self.db.get('/members', {
			"id": self.user_id,
			"db": "members",
			"server": server
		})['answer']
		# instance openAI
		self.client = OAI()


	########################### database functions ###########################

	# set new info into a user
	def __set_user_data (self, update: dict):
		# call the db
		ans = self.db.put('/members', {
			"id": self.user_id,
			"db": "members",
			"data": update
		})['answer']
		return ans

	# new function to publicly allow set user data
	def set_user_data (self, update: dict):
		return self.__set_user_data(update)

	########################### availability checking functions ###########################

	# checks if the current model has tokens yet to answer the question
	# IMPORTANT: AVERAGE ANSWER LEN
	def __model_availability (self, model: str, message: str, context: bool, image=False):
		# if the context is going to be counted use the actual len
		# else, just count the context as 8, "Eres alguien inteligente"
		context_len = self.user_data['context_len'] if context else 8
		# now tokenize the message
		message_len = self.token_counter(message, image)
		# if model has more tokens than the context + message + avg answer len
		if self.user_data['usage'][model] >= context_len + message_len + 200:
			# the model has enough tokens yet
			return True
		# if not
		else:
			# the model has not enough tokens
			return False

	########################### context handling functions ###########################

	# get the actual tokens of a string
	def token_counter (self, string: str, image=False):
		# added to tokenize images
		added_for_image = 0
		if image:
			added_for_image = int(765/3)
		# set the tokenizer
		encoding = tiktoken.get_encoding("cl100k_base")
		# encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
		# count the tokens
		num_tokens = len(encoding.encode(string))
		return num_tokens + added_for_image

	# determines the context limit based on the model, here's
	# the limit of the context's size, once the context reaches
	# IMPORTANT: LIMIT OF THE TOKENS TO RESET THE CONTEXT
	def __get_token_limit (self, model: str):
		if model == "gpt-3.5-turbo-16k":
			return 16000
		else:
			# this will be lower, since to keep the
			# conversations cheap, may be change in the future
			return 1000

	# create a context for a user once the context has gone full
	# only called in cases, BEFORE THE ANSWER
	def __recreate_context (self):
		# set the new context starting with personality
		new_context = [{
			"role": "system",
			"content": self.user_data['personality']
		}]
		# add the actual context's tail, the last two messages
		# these are the last question an the last answer
		new_context += self.user_data['context'][-2:]
		# save the new context
		self.user_data['context'] = new_context
		# and restart the context_len counter
		self.user_data['context_len'] = 0

	# VERY IMPORTANT!
	# used to count the tokens on th
	def __token_recount (self, usage, model: str, context: bool):
  		# so, assign the variables
  		tokens_in = usage.prompt_tokens
  		tokens_out = usage.completion_tokens
  		# calculate the adjusted based on the model
  		adjusted = int(tokens_out * 2) if model != "gpt-4-turbo-preview" else int(tokens_out * 3)
  		# calculate the total = tokens_in + adjusted
  		total_tokens = tokens_in + adjusted
  		# update the user data
  		self.user_data['usage'][model] -= total_tokens
  		# ubdate the context len based on the usage
  		# ONLY IF THE CONTEXT IS ENABLED
  		if context:
  			self.user_data['context_len'] = tokens_in + tokens_out
  		# else, just wait to the next call that uses context
  		# return the count to save on the logs
  		return tokens_in, tokens_out, adjusted, total_tokens


	# This functin is called in every response of GPT, but
	# its function is just to add to context, and save on db
	def __handle_context (self, answer: str, context: bool): 
		# if the context was enabled
		if context:
			# add the answer to the context
			self.user_data['context'].append({
				"role": "system",
				"content": answer
			})
		# then make the update
		self.__set_user_data({
			"usage": self.user_data['usage'],
			"context_len": self.user_data['context_len'],
			"context": self.user_data['context'],
		})


	# this function prepares context to call the function
	# tokens will be counted after the answer
	def __append_to_context(self, text: str, model: str):
		# before the answer
		# here is the part of recreate context, only here
		# so, count the tokens on the message
		text_len = self.token_counter(text)
		# if the question + the context is larger than the limit: recreate the context
		if text_len + self.user_data['context_len'] > self.__get_token_limit(model):
			# recreate the context only if it surpasses the limit 
			self.__recreate_context()
		# finally add the incoming message to the context
		self.user_data['context'] += [{'role': 'user', 'content': text}]


	########################### GPT usage function ###########################

	# gpt genereal usage, you can select the model to use and also
	# you can manage wether save the conversation context or not
	def gpt (self, prompt: str, model="gpt-3.5-turbo", temp=0.5, context=True, system="Eres alguien inteligente"):
		# check tokens availability for the selected model
		# also based on the len of the context
		availability = self.__model_availability(model, prompt, context)
		# if the model is out of tokens
		if not availability:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more tokens left for {model}"
			})
			# then return a message, in the correct 
			# format: a list of dicts per message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}> se te acabaron las palabras para {self.metrics[model]}."
			}]
		# at this point the user has tokens to use yet. Then add the
		# incoming message to the context only if the context is enabled
		if context:
			# this function just add the prompt to the context
			self.__append_to_context(prompt, model)
		# if not, format the prompt to call gpt
		else:
			prompt_call = [
				# this content is found in the __model_availability function
				# counted as the 8 tokens added
				{"role": "system", "content": system},
				{"role": "user", "content": prompt}
			]
		# so use gpt with the available model
		res = self.client.chat.completions.create(
			model=model,
			# here also, if the context is required, call gpt with the
			# prompt and context, else just use the prompt
			messages=self.user_data['context'] if context else prompt_call,
			temperature=temp
		)
		# make recount of the tokens used, in the response are the
		# tokens used, tokens in and tokens out, this function
		tokens_in, tokens_out, adjusted, total_tokens = self.__token_recount(res.usage, model, context)
		# regist on the logs the answer
		self.db.post("/logs", {
			"db": "chat",
			"data": f"[{self.user_id}] {model} Q: {prompt[:10]}... A: {res.choices[0].message.content[:10]}"
		})
		self.db.post("/logs", {
			"db": "tokens",
			"data": f"[{self.user_id}] {model} in: {tokens_in} out: {tokens_out} adjusted: {adjusted} total: {total_tokens}"
		})
		# handle context but for answer
		# this function just appends the answer to the context (if context),
		#  and saves changes on the database (context, usage and context len)
		self.__handle_context(
			res.choices[0].message.content, context
		)
		# form the answer in the format
		answer = [
			{
				"type": "text",
				"content": res.choices[0].message.content
			}
		]
		# finally return the answer
		return answer

	########################### DALL-E sub functions ###########################

	# function to save the images in lambdrive
	# receives the urls and returns hashes, names
	# where the images are, now on lambdrive. Image
	# type is the db key: images, edtis or variations
	def __download_images (self, urls: list, image_type: str):
		hashes = []
		images_paths = []
		# per image url
		for url in urls:
			name = str(generate_hash(url))
			# download the image and save the path
			images_paths.append(download_image(url, name, dalle_type=image_type))
			# save the name
			hashes.append(name)
		# get the actual images
		images_data = self.db.get('/members', {
			"id": self.user_id,
			"db": "images"
		})['answer']
		# append the new images
		# update the db
		self.db.put('/members', {
			"id": self.user_id,
			"db": "images",
			"data": {
				image_type: images_data[image_type] + hashes
			}
		})
		# return the image paths
		return images_paths, hashes

	# same function but for images, this one also
	# recieves the number of images that wants to be 
	# generated
	def __dalle_availability (self, n: int):
		# get the remaining images
		remaining_images = self.user_data['usage']['dalle']
		# now check if the remaining images are less
		# than the generated
		if remaining_images < n:
			# the operation can be done
			# return also the remaining images
			return False, remaining_images
		# if there are images available
		else:
			return True, remaining_images - n

	# function to update usage, after generating the images
	# also saves the images hash
	def __update_dalle_usage (self, n: int, last_hash: str):
		# update the local instance
		self.user_data['usage']['dalle'] -= n
		# now update in the db
		self.__set_user_data({
			"usage": self.user_data['usage'],
			"file": last_hash
		})

	# function to pre process images to use dalle edit and variation
	def __preprocess_image (self, image_path: str):
		# Read the image file from disk and resize it
		image = Image.open(image_path)
		image = image.resize((1024, 1024))
		# convert to RGBA format to solve an error
		image = image.convert('RGBA')

		# Convert the image to a BytesIO object
		byte_stream = BytesIO()
		image.save(byte_stream, format='PNG')
		byte_array = byte_stream.getvalue()
		return byte_array

	########################### DALL-E functions ###########################

	# DALL-E function to create images
	def create_image (self, prompt:str, n=1, size="1024x1024"):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# generate the images
			response = self.client.images.generate(
				model="dall-e-3",
				prompt=prompt,
				n=n,
				size=size,
				quality="hd"
			)
			# regist on the logs
			self.db.post("/logs", {
				"db": "images",
				"data": f"[{self.user_id}] {prompt}"
			})
			# get the urls
			urls = []
			for i in range(n):
				urls.append(response.data[i].url)
			# download the images
			paths, hashes = self.__download_images(urls, 'images')
			# update the usage
			self.__update_dalle_usage(n, hashes[0])
			# finally return the paths in the correct format
			answer = []
			for p,h in zip(paths, hashes):
				answer.append({'type':'file', 'content':p})
				answer.append({'type':'text', 'content':"Listo, tu imagen está disponible"})
			# and append a message with the remaining images
			answer.append({
				"type": "text",
				"content": f"> <@{self.user_id}>, te quedan {remaining} imágenes"
			})
			return answer

		# if there are no available images
		else:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more images left"
			})
			# return a message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, ya no te quedan más imágenes."
			}]

	# DALL-E function to edit images
	def edit_image (self, image_path: str, mask_path:str, prompt:str, n=1, ):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# generate the images
			response = self.client.images.edit(
				image=self.__preprocess_image(image_path),
				mask=self.__preprocess_image(mask_path),
			  	prompt=prompt,
			  	n=n
			)
			# regist on the logs
			self.db.post("/logs", {
				"db": "images",
				"data": f"[{self.user_id}] edited: {image_path}, {prompt}"
			})
			# get the urls
			urls = []
			for i in range(n):
				urls.append(response.data[i].url)
			# download the images
			paths, hashes = self.__download_images(urls, 'images')
			# update the usage
			self.__update_dalle_usage(n)
			# finally return the paths in the correct format
			answer = []
			for p,h in zip(paths, hashes):
				answer.append({'type':'file', 'content':p})
				answer.append({'type':'text', 'content':f"Imagen disponible como ${h}"})
			# and append a message with the remaining images
			answer.append({
				"type": "text",
				"content": f"> <@{self.user_id}>, te quedan {remaining} imágenes"
			})
			return answer

		# if there are no available images
		else:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more images left"
			})
			# return a message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, ya no te quedan más imágenes."
			}]

	# DALL-E function to generate variations of a given image
	def variate_image (self, image_path: str, n=1):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# generate the images
			response = self.client.images.create_variation(
				image=self.__preprocess_image(image_path),
			  	n=n,
			  	size="1024x1024"
			)
			# regist on the logs
			self.db.post("/logs", {
				"db": "images",
				"data": f"[{self.user_id}] variated: {image_path}"
			})
			# get the urls
			urls = []
			for i in range(n):
				urls.append(response.data[i].url)
			# download the images
			paths, hashes = self.__download_images(urls, 'images')
			# update the usage
			self.__update_dalle_usage(n)
			# finally return the paths in the correct format
			answer = []
			for p,h in zip(paths, hashes):
				answer.append({'type':'file', 'content':p})
				answer.append({'type':'text', 'content':f"Imagen disponible como ${h}"})
			# and append a message with the remaining images
			answer.append({
				"type": "text",
				"content": f"> <@{self.user_id}>, te quedan {remaining} imágenes"
			})
			return answer

		# if there are no available images
		else:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more images left"
			})
			# return a message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, ya no te quedan más imágenes."
			}]
	
	
	########################### Audio functions ###########################

	# used to create text to speech audios
	def text_to_speech (self, text: str, voice="echo", model="tts-1-hd"):
		# first count the characters in the text
		chars = len(text)
		# then check the availability
		# if there's not enough tokens
		if self.user_data['usage']['tts'] < chars:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more tts chars left"
			})
			# send a message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, solo te quedan {self.user_data['usage']['tts']} caracteres para audios, tu mensaje tiene {chars}."
			}]
		# then there's enough chars
		# create a file path to save the audio
		audio_hash = generate_hash(text)
		audio_path = f"lambdrive/audios/{audio_hash}.mp3"
		# os.system(f"touch {audio_path}")
		# so create the audio
		response = self.client.audio.speech.create(
		  model=model,
		  voice=voice,
		  input=text
		)
		# then save the audio in a file
		response.stream_to_file(audio_path)
		# regist on the logs
		self.db.post("/logs", {
			"db": "audios",
			"data": f"[{self.user_id}] generated: {audio_hash}.mp3"
		})
		# discount the chars to the user_data
		self.user_data['usage']['tts'] -= chars
		# and save changes
		self.__set_user_data({
			"usage": self.user_data['usage'], 
			"file": audio_hash
		})
		# finally send the answer
		return [
			{"type": "file", "content": audio_path},
			{"type": "text", "content": f"Listo, tu audio está disponible para usarse."},
			{"type": "text", "content": f"Te quedan {self.user_data['usage']['tts']} caracteres para audios"}
		]

	# function to use whisper model, type can be "translation" or "transcription"
	def speech_to_text (self, audio_path: str, model_type="transcription"):
		# read the audio minutes
		minutes = audio_minutes(audio_path)
		# check availability
		if self.user_data['usage']['whisper'] < minutes:
			# if the user has not enough minutes left
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more whisper left"
			})
			# send a message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, solo te quedan {self.user_data['usage']['whisper']} minutos de audio, tu audio tiene {minutes} minutos."
			}]
		# then the user has enough minutes
		# so, read the user
		audio_file = open(audio_path, "rb")
		# create the transcript or translation
		if model_type == "transcription":	
			transcript = self.client.audio.transcriptions.create(
				model="whisper-1",
				file=audio_file
			)
		elif model_type == "translation":	
			transcript = self.client.audio.translations.create(
				model="whisper-1",
				file=audio_file
			)
		else:
			raise ValueError(f"Value Error: {model_type}")
		# regist on the logs
		self.db.post("/logs", {
			"db": "audios",
			"data": f"[{self.user_id}] transcripted: {audio_path}.mp3"
		})
		# make the discount of the minutes
		self.user_data['usage']['whisper'] -= minutes
		# save the changes
		self.__set_user_data({
			"usage": self.user_data['usage']
		})
		# finally send the answer
		return [
			{"type": "text", "content": transcript.text}
		]

	########################### Vision functions ###########################

	# gpt genereal usage, you can select the model to use and also
	# you can manage wether save the conversation context or not
	def gpt_vision (self, image_prompt: str, text_prompt: str, model="gpt-4-vision-preview", context=True):
		# first check if there's images for the user
		if self.user_data['usage']['vision'] <= 0:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more images left for {model}"
			})
			# then return a message, in the correct 
			# format: a list of dicts per message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}> se te acabaron las imágenes para la Vision Inteligente."
			}]
		# also check tokens availability for the selected model
		# also based on the len of the context
		availability = self.__model_availability("gpt-4-turbo-preview", text_prompt, context, image=True)
		# if the model is out of tokens
		if not availability:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more tokens left for {model}"
			})
			# then return a message, in the correct 
			# format: a list of dicts per message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}> se te acabaron las imágenes para la Vision Inteligente."
			}]
		# so, upload the image
		cloud = Cloudinary(self.user_id)
		try:
			image_url = cloud.upload(image_prompt)
		except:
			raise OSError(f"Could not upload {image_prompt} to cloudinary")
		# at this point the user has tokens to use yet. Then add the
		# incoming message to the context only if the context is enabled
		if context:
			# this function just add the prompt to the context
			# then ONLY APPEND THE TEXT PROMPT 
			self.__append_to_context(text_prompt, model)
		# if not, format the prompt to call gpt

		# special format for the gpt vision calls
		messages = [
			{
	            "role": "user",
	            "content": [
	                {"type": "text", "text": text_prompt},
	                {
	                    "type": "image_url",
	                    "image_url": image_url,
	                },
	            ],
	        }
	    ]
		# so use gpt with the available model
		res = self.client.chat.completions.create(
			model=model,
			# here also, if the context is required, call gpt with the
			# prompt and context, else just use the prompt
			messages=messages,
			max_tokens=1024
		)
		# make recount of the tokens used, in the response are the
		# tokens used, tokens in and tokens out, this function
		tokens_in, tokens_out, adjusted, total_tokens = self.__token_recount(res.usage, "gpt-4-turbo-preview", context)
		# regist on the logs the answer
		self.db.post("/logs", {
			"db": "chat",
			"data": f"[{self.user_id}] {model} Q: {text_prompt[:10]}... A: {res.choices[0].message.content[:10]}"
		})
		self.db.post("/logs", {
			"db": "tokens",
			"data": f"[{self.user_id}] {model} in: {tokens_in} out: {tokens_out} adjusted: {adjusted} total: {total_tokens}"
		})
		# handle context but for answer
		# this function just appends the answer to the context (if context),
		#  and saves changes on the database (context, usage and context len)
		self.__handle_context(
			res.choices[0].message.content, context
		)
		# discount tokens from vision
		self.user_data['usage']['vision'] -= 1
		# save the changes
		self.__set_user_data({
			"usage": self.user_data['usage']
		})
		# form the answer in the format
		answer = [
			{
				"type": "text",
				"content": res.choices[0].message.content
			}
		]
		# finally return the answer
		return answer