# modules
import os
import json
import requests
# open ai
import openai
# and tokenizer
import tiktoken
# cloduinary
import cloudinary
import cloudinary.uploader
# image processing
from io import BytesIO
from PIL import Image


##########################################################################
############################### Functions ################################
##########################################################################

# download images, linux only
def download_image(img_link: str, name: str, extension='.png', where="lambdrive/images/", dalle_type= ""):
	# Create the wget command
	wget_command = f'wget "{img_link}" -O "{where}{name}{extension}"'
	# Execute the wget command
	if os.getenv("dev") != "yes":
		# download the img
		os.system(wget_command)
		# and copy it to dalle
		os.system(f"cp {where}{name}{extension} lambdrive/dalle/{dalle_type}_{name}{extension}")
	# else, just print the variables
	else:
		print(img_link)
	# return the image path
	return f"{where}{name}{extension}"

# function to generate hashes, it must not be used to security operations
def generate_hash(data: str):
	# generate a numerical hash with python
    # convert it to hexadecimal
    return hex(hash(data) & 0xFFFFFFFFFFFFFFFF)[2:].zfill(16)

##########################################################################
################################# Modules ################################
##########################################################################

# this will be like a dict, but the keys are lists of 
# words, used on lambda V2. Now is a module extra that
# may can be used to create new functions
class list_dic:
	# keys is a list of lists, and values just a list
	def __init__ (self, keys: list, values: list):
		# handle errors
		if len(keys) != len(values):
			raise ValueError("Error on list_dic: len(keys) != len(values)")
		# asociates each word with a index, this index
		# may be repeated if the key has more than one
		# word in the list. This way the search will be
		# faster than going looking for words
		self.word_dic = {}
		self.all_keys = []
		# fill the word_dic
		for i,key in enumerate(keys):
			# if the key is a list
			if isinstance(key, list):
				# assing the i per word in key list
				for word in key:
					self.word_dic[word] = i
					self.all_keys.append(word)
			# is just a word
			else: 
				self.word_dic[key] = i
				self.all_keys.append(key)
		# and the other params
		self.values = values
		self.default = default
		self.keys = keys

	def __getitem__ (self, key):
		try:
			# look for the key in the word_dic
			idx = self.word_dic[key]
			# then return the idx value
			return self.values[idx]
		except:
			# return the default function
			raise ValueError(f'Error on key {key}')

	def get_all_keys(self):
		return self.all_keys

	def get_keys(self):
		return self.keys

	def get_values(self):
		return self.values


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


# cloudinary module
class Cloudinary:
	"""
	This is a module that uses cloudinary to upload
	files into cloudinary
	"""
	def __init__ (self):
		# get the cloudinary credentials
		# returns "https" URLs by setting secure=True  
		config = cloudinary.config(
			secure=True,
			cloud_name=os.getenv("cloud_name"),
			api_key=os.getenv("api_key"),
			api_secret=os.getenv("api_secret")
		)
		# instance a db to use it
		self.db = DB()

	# upload files
	def upload (self, img_path: str):
		# try to upload the image
		try:
			# upload process
			ans = cloudinary.uploader.upload(img_path)
			# if it worked, regist on log
			self.db.post("/logs", {
				"db": "clodinary",
				"data": f"[{self.user_id}] uploaded file {image_path} to {ans['secure_url']}"
			})
			return ans['secure_url']
		except:
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] error on uploading file {image_path}"
			})
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}>, ocurrió un error al subir el archivo"
				}]


# models:
# gpt-3.5-turbo
# gpt-3.5-turbo-16k
# gpt-4
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
		openai.api_key = os.getenv("OPENAI")
		# the instance of db
		self.db = DB()
		# the models, the order is by price - to +
		self.models = [
			"gpt-3.5-turbo",
			"gpt-3.5-turbo-16k",
			"gpt-4"
		]
		# get the user data
		self.user_data = self.db.get('/members', {
			"id": self.user_id,
			"db": "members",
			"server": server
		})['answer']


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

	########################### availability checking functions ###########################

	# checks if the current model has tokens yet to answer the question
	# IMPORTANT: AVERAGE ANSWER LEN
	def __model_availability (self, model: str, message: str, context: bool):
		# if the context is going to be counted use the actual len
		# else, just count the context as 8, "Eres alguien inteligente"
		context_len = self.user_data['context_len'] if context else 8
		# now tokenize the message
		message_len = self.token_counter(message)
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
	def token_counter (self, string: str):
		# set the tokenizer
		encoding = tiktoken.get_encoding("cl100k_base")
		# encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
		# count the tokens
		num_tokens = len(encoding.encode(string))
		return num_tokens

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
	def __token_recount (self, usage: dict, model: str, context: bool):
  		# so, assign the variables
  		tokens_in = usage['prompt_tokens']
  		tokens_out = usage['completion_tokens']
  		# calculate the adjusted based on the model
  		adjusted = int(tokens_out * 1.3) if model != "gpt-4" else int(tokens_out * 2)
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
				"content": f"Lo siento <@{self.user_id}> se te acabaron los tokens de conversación"
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
		res = openai.ChatCompletion.create(
			model=model,
			# here also, if the context is required, call gpt with the
			# prompt and context, else just use the prompt
			messages=self.user_data['context'] if context else prompt_call,
			temperature=temp
		)
		# make recount of the tokens used, in the response are the
		# tokens used, tokens in and tokens out, this function
		tokens_in, tokens_out, adjusted, total_tokens = self.__token_recount(res['usage'], model, context)
		# regist on the logs the answer
		self.db.post("/logs", {
			"db": "chat",
			"data": f"[{self.user_id}] Q: {prompt}... A: {res['choices'][0]['message']['content']}"
		})
		self.db.post("/logs", {
			"db": "tokens",
			"data": f"[{self.user_id}] in: {tokens_in} out: {tokens_out} adjusted: {adjusted} total: {total_tokens}"
		})
		# handle context but for answer
		# this function just appends the answer to the context (if context),
		#  and saves changes on the database (context, usage and context len)
		self.__handle_context(
			res['choices'][0]['message']['content'], context
		)
		# form the answer in the format
		answer = [
			{
				"type": "text",
				"content": res['choices'][0]['message']['content']
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
	def __update_dalle_usage (self, n: int):
		# update the local instance
		self.user_data['usage']['dalle'] -= n
		# now update in the db
		self.__set_user_data({
			"usage": self.user_data['usage']
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
	def create_image (self, prompt:str, n=1):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# generate the images
			response = openai.Image.create(
				prompt=prompt,
				n=n,
				size="1024x1024"
			)
			# regist on the logs
			self.db.post("/logs", {
				"db": "images",
				"data": f"[{self.user_id}] {prompt}"
			})
			# get the urls
			urls = []
			for i in range(n):
				urls.append(response['data'][i]['url'])
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

	# DALL-E function to edit images
	def edit_image (self, image_path: str, prompt:str, n=1):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# pre process
			pre = self.__preprocess_image(image_path)
			# generate the images
			response = openai.Image.create_edit(
				image=pre,
				mask=open("full_mask.png"),
			  	prompt=prompt,
			  	n=n,
			  	size="1024x1024"
			)
			# regist on the logs
			self.db.post("/logs", {
				"db": "images",
				"data": f"[{self.user_id}] edited: {image_path}, {prompt}"
			})
			# get the urls
			urls = []
			for i in range(n):
				urls.append(response['data'][i]['url'])
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
			response = openai.Image.create_variation(
				image=open(image_path, "rb"),
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
				urls.append(response['data'][i]['url'])
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