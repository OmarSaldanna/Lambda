# helper functions for the body functions

# modules
from core.memory import get_memory, log_file

import os

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


# read the log file
def read_log():
	with open(log_file, "r") as file:
	    file_contents = file.read()
	return file_contents

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