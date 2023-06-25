# helper functions for the body functions

# modules
from core.memory import get_memory, log_file

import os

# to tokenize GPT scontext
import tiktoken

# cloduinary
import cloudinary
import cloudinary.uploader
# get the cloudinary credentials
info = get_memory('info')['cloudinary']
# returns "https" URLs by setting secure=True  
config = cloudinary.config(
	secure=True, cloud_name= info['cloud_name'],
	api_key=info['api_key'], api_secret=info['api_secret']
	)

##########################################################################
################## Helper Functions for body #############################
##########################################################################

# cloudinary function
def upload_image(img_path: str):
	ans = cloudinary.uploader.upload(img_path)
	return ans['secure_url']


# download images, linux only
def download_image(img_link: str, name: str, extension='.png'):
	# Create the wget command
	wget_command = f'wget "{img_link}" -O "{name}{extension}"'
	# Execute the wget command using os.popen
	os.popen(wget_command)


# get the last of the log file that sums ~3000 tokens
def read_log(token_limit=3000):
	token_counter = 0
	counter = 10
	log = ''
	while token_counter < 3000:
		# read the n last lines
		log = os.popen(f'tail -n {counter} {log_file}').read()
		# count the tokens
		token_counter = tokenize_counter(log)
		# 
		counter += 5
	return log



# read the personality
def get_personality(user: str):
	# try to find the user, if wasn't found, return the default
	person_file = get_memory('personality')
	personality = ''
	try:
		personality = person_file[user]
	except:
		print(f'[LAMBDA] -> Personality not found <@{user}>')
		personality = person_file['default']
	return personality

##########################################################################
################## GPT Context Processing ################################
##########################################################################

# 4,096 tokens is the max context. Then clear the context of the user
# once the user actual context has surpassed the limit size.
token_limit = 4000


# get the actual tokens of the context
def tokenize_counter(string: str, encoding_name='gpt2'):
	# tokenize
	encoding = tiktoken.get_encoding(encoding_name)
	# count the tokens
	num_tokens = len(encoding.encode(string))
	return num_tokens


# create a context register if the user does not has one.
# also if the context is new, append the personality as 
# the first message in context
def load_context(user: str):
	# read the memory
	memory_file = get_memory('memory')
	# get the personality
	personality = get_personality(user)

	# try to get the context of the user
	try:
		# the context exists
		user_context = memory_file['gpt_contexts'][user]
	# this is in case of new users
	except:
		# the context does not exists, then create the instance
		# with the personality as the firt item
		memory_file['gpt_contexts'][user] = [
			{"role": "system", "content": personality}
		]
		# save changes
		memory_file.write()
		# and return the context
		user_context = memory_file['gpt_contexts'][user]
	return user_context, memory_file


# counts the size in tokens of an user's gpt context
def get_context_len(user: str):
	# select the context
	context, memory_file = load_context(user)
	token_counter = 0
	# iterate the messages structure
	for msg in context:
		# and count the tokens
		token_counter += tokenize_counter(msg['content'])
	return token_counter, memory_file


# counts the tokens from a specific message structure
def get_message_len(message: list):
	token_counter = 0
	# iterate the messages structure
	for msg in message:
		# and count the tokens
		token_counter += tokenize_counter(msg['content'])
	return token_counter


# create a context for a user once the context has gone full
def recreate_context(user: str, message: list, memory_file, on_conversation):
	# if it was "Lambda dime ...", it's not conversation
	# if it was "Lambda, ...", it's a conversation
	# and conversations keep the context's tail to keep the thread
	# so, form the new context
	personality = get_personality(user)
	new_context = [
		{"role": "system", "content": personality}
	]
	# add the actual context's tail, if it's on conversation
	if not on_conversation:
		new_context += message
	# finally save the context
	memory_file['gpt_contexts'][user] = new_context
	memory_file.write()


# this function is called in every gpt call, it recieves the
# user and the message of the call. The function:
# if: the message and answer tokens + actual tokens > token_limit
# -> then send the answer and creates a new context
# else: the message and answer tokens + actual tokens <= token_limit
# -> then just append these new messages to the context
def handle_gpt_context(user: str, message: list, on_conversation=False):
	# get the actual len of the saved context
	context_size, memory_file = get_context_len(user)
	# get the len of the new context
	new_size = get_message_len(message)
	# once the context has gone full
	if context_size + new_size > token_limit:
		# create a new context
		recreate_context(user, message, memory_file, on_conversation)
	# since the context isn't full already
	else:
		# just aadd the message to the actual context
		memory_file['gpt_contexts'][user] += message
		# save changes
		memory_file.write()


##########################################################################
################## List Dic: words2functions #############################
##########################################################################

# this will be like a dict, but the keys are lists of words
class list_dic:
	# keys is a list of lists, and values just a list
	def __init__ (self, keys: list, values: list, default):
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
			return self.default

	def get_all_keys(self):
		return self.all_keys

	def get_keys(self):
		return self.keys

	def get_values(self):
		return self.values


'''
def hello():
	print('hello')

def product():
	print('2 * 2 = 4')

def default():
	print('default')

func_dic = list_dic(
	[['hello', 'hola'], 'product'],
	[hello, product],
	default
)

func_dic['hello']()
func_dic['hola']()
func_dic['product']()
'''
'''
answer = upload_image('lambdrive/first-anime.png')
print(answer)
'''