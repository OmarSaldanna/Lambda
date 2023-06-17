# helper functions for the body functions
import hashlib


# used to save qr codes
def generate_hash(text: str):
	hash_object = hashlib.sha256(text.encode())
	return hash_object.hexdigest()


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
		self.keys = []
		# fill the word_dic
		for i,key in enumerate(keys):
			# if the key is a list
			if isinstance(key, list):
				# assing the i per word in key list
				for word in key:
					self.word_dic[word] = i
					self.keys.append(word)
			# is just a word
			else: 
				self.word_dic[key] = i
				self.keys.append(key)
		# and the other params
		self.values = values
		self.default = default

	def __getitem__ (self, key):
		try:
			# look for the key in the word_dic
			idx = self.word_dic[key]
			# then return the idx value
			return self.values[idx]
		except:
			# return the default function
			return self.default

	def get_keys(self):
		return self.keys

	def get_values(self):
		return self.keys


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