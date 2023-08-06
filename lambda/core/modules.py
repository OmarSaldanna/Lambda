# modules
import os
import json
import requests
from dotenv import load_dotenv
# to tokenize GPT scontext
import tiktoken
import openai
# cloduinary
import cloudinary
import cloudinary.uploader

# load the .env variables
load_dotenv()

##########################################################################
############################### Functions ################################
##########################################################################

# download images, linux only
def download_image(img_link: str, name: str, extension='.png', where="lambdrive/dalle/"):
	# Create the wget command
	wget_command = f'wget "{img_link}" -O "{where}{name}{extension}"'
	# Execute the wget command using os.popen
	if os.getenv("dev") != "yes":
		os.popen(wget_command)
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
		return requests.get(self.api + api, headers=headers).json()

	# post request
	def post (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.post(self.api + api, headers=headers).json()

	# put request
	def put (self, api: str, headers: dict):
		# preprocess the headers
		headers = self.__preprocess(headers)
		# send the request
		return requests.put(self.api + api, headers=headers).json()


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

	# checks if the current model has tokens yet,
	def __gpt_availability_check (self):
		# get the current model
		current_model = self.user_data['model']
		# check if it has available tokens
		if self.user_data['usage'][current_model] > 50:
			# the model has available tokens
			# then return the model to use it
			# the false is that the model is
			# the same as the current model
			return current_model, True
		# if not, check other models
		else:
			# check the models
			for model in self.models:
				# if one other has availability
				if self.user_data['usage'][model] > 50:
					# return the model, and a false
					# that indicates the model is 
					# another one from the current
					return model, False
			# else, the user has no tokens left
			# then just return False
			return False

	########################### context handling functions ###########################

	# get the actual tokens of a string
	def token_counter_str (self, string: str, encoding_name='gpt2'):
		# tokenize
		encoding = tiktoken.get_encoding(encoding_name)
		# count the tokens
		num_tokens = len(encoding.encode(string))
		return num_tokens

	# count the tokens in a message structure
	def __token_counter_list (self, messages: list, encoding_name='gpt2'):
		total = 0
		# iterate the messages
		for message in messages:
			# count the tokens in the message
			total += self.token_counter_str(message['content'])
		# return the total
		return total

	# determines the context limit based on the model, here's
	# the limit of the context's size, once the context reaches
	# IMPORTANT: LIMIT OF THE TOKENS TO RESET THE CONTEXT
	def __get_token_limit (self, model: str):
		if model == "gpt-3.5-turbo-16k":
			return 800
		else:
			return 800

	# create a context for a user once the context has gone full
	def __recreate_context(self, n: int):
		# set the new context starting with personality
		new_context = [{
			"role": "system",
			"content": self.user_data['personality']
		}]
		# add the actual context's tail, the last two messages
		new_context += self.user_data['context'][-n:]
		# return the new context
		return new_context

	# VERY IMPORTANT!
	# function used to update the context usage
	# if the prices change in the future this part must change
	def __count_gpt_usage (self, context_len: int, answer: str):
		# calculate the tokens of the answer
		answer_len = self.token_counter_str(answer)
		# make the cost
		tokens_in = context_len
		# since answer tokens costs 1.3 times context 
		# tokens, see openAI pricing
		tokens_out = int(answer_len * 1.3)
		# then count total tokens
		tokens_count = tokens_in + tokens_out
		# return the total tokens
		return tokens_count, answer_len

	# main context function, used to handle it,
	# is called before and after the GPT call
	def __handle_context (self, text: str, model: str, on_answer=False):
		# get the context len
		context_len = self.__token_counter_list(
			self.user_data["context"]
		)
		# in case the function was called after
		# gpt was called to answer. Here the thing
		# is to:
		# * count the tokens in and out
		# * once counted, add the answer to the context
		# * if the context is bigger than the limit
		# then recreate it and save it
		# * finally make the updates on DB
		if on_answer:
			# * count the tokens in and out
			token_count, answer_len = self.__count_gpt_usage(
				context_len, text
			)
			# * once counted, add the answer to the context
			self.user_data['context'].append({
				"role": "system",
				"content": text
			})
			# and update the context len
			context_len += answer_len
			# * if the context is bigger than the limit
			# then recreate it and save it
			if context_len > self.__get_token_limit(model):
				# recreate the context
				# the last messages are: user, system
				self.user_data['context'] = self.__recreate_context(2)
			# * finally make the updates on DB:
			# usage
			self.user_data['usage'][model] -= token_count
			# model, may be changed due to availability
			self.user_data['model'] = model
			# context was already changed
			# then make the update
			self.__set_user_data({
				"usage": self.user_data['usage'],
				"model": self.user_data['model'],
				"context": self.user_data['context'],
			})
			
		# in case the function was called before
		# then text is the user prompt. Here the
		# point is just ADD THE PROMPT TO THE
		# PAST CONTEXT and send it to the model
		else:
			# add the text to the context
			self.user_data['context'].append({
				"role": "user",
				"content": text
			})
			# may be the prompt makes the context
			# bigger than the limit, in that case,
			# recreate the context
			if context_len > self.__get_token_limit(model):
				# recreate the context
				# the last messages are: user, system
				self.user_data['context'] = self.__recreate_context(3)

	########################### GPT usage function ###########################

	# gpt genereal usage, it requires the messages structure
	def gpt(self, message: str, temp=0.5):
		# check tokens availability
		availability = self.__gpt_availability_check()
		# if the user is out of tokens
		if not availability:
			# regist on the logs
			self.db.post("/logs", {
				"db": "errors",
				"data": f"[{self.user_id}] no more tokens left"
			})
			# then return a message, in the correct 
			# format: a list of dicts per message
			return [{
				"type": "error",
				"content": f"Lo siento <@{self.user_id}> se te acabaron los tokens de conversación"
				}]
		# then the user has tokens to use yet
		model, on_current_model = availability
		# handle context for the prompt
		self.__handle_context(
			message, model, on_answer=False
		)
		# so use gpt with the available model
		res = openai.ChatCompletion.create(
			model=model,
			messages=self.user_data['context'],
			temperature=temp
		)
		# regist on the logs also the answer
		self.db.post("/logs", {
			"db": "chat",
			"data": f"[{self.user_id}] Q: {message}... A: {res['choices'][0]['message']['content']}"
		})
		# handle context but for answer
		messages = self.__handle_context(
			res['choices'][0]['message']['content'],
			model, on_answer=True
		)
		# form the answer in the format
		answer = [
			{
				"type": "text",
				"content": res['choices'][0]['message']['content']
			}
		]
		# check if the model was changed for
		# avaulability reasons
		if not on_current_model:
			answer.append({
				"type": "error",
				"content": f"<@{self.user_id}> tu modelo de lenguaje en uso fue cambiado a _{model}"
			})
		# finally return the answer
		return answer

	########################### DALL-E sub functions ###########################

	# function to save the images in lambdrive
	# receives the urls and returns hashes, names
	# where the images are, now on lambdrive. Image
	# type is the db key: images, edtis or variations
	def __download_images(self, urls: list, image_type: str):
		hashes = []
		images_paths = []
		# per image url
		for url in urls:
			name = str(generate_hash(url))
			# download the image and save the path
			images_paths.append(download_image(url, name))
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
	def __update_dalle_usage(self, n: int):
		# update the local instance
		self.user_data['usage']['dalle'] -= n
		# now update in the db
		self.__set_user_data({
			"usage": self.user_data['usage']
		})

	########################### DALL-E functions ###########################

	# DALL-E function to create images
	def create_image(self, prompt:str, n=1):
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
			print(urls)
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
	def edit_image(self, image_path: str, prompt:str, n=1):
		# first check availability for the requested images
		available, remaining = self.__dalle_availability(n)
		# if there are images available
		if available:
			# generate the images
			response = openai.Image.create_edit(
				image=open(image_path, "rb"),
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
	def variate_image(self, image_path: str, n=1):
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