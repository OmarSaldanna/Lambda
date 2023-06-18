# Lambda Mindful Messenger, lambda's name suggestion.
# this model recieves the functions dict. This model was
# developed for the cases when there are more than one
# function asociated to a key on the function dic.

class Lambda_Mindful_Messenger:

	def __init__ (self, thing_recognizer, function_dic:dict):
		self.thing_recognizer = thing_recognizer
		self.function_dic = function_dic

	# the verb or question has been detected
	def __call__ (self, message:str, tag:str, word:str):
		# in some cases the detected word may be is associated
		# to more than one function, this can be detected if
		# len(self.function_dic[tag][word]) > 1. So, first step
		# is select that
		instance = self.function_dic[tag][word]

		# if theres only one action, the instance will be a list
		# else, the instance is a list and has more than one function
		if not isinstance(instance, list):
			# then return that function
			return instance

		# if theres more than one action, for example in the
		# case of [genera|crea] un [QR|Imagen]. In this case
		# to determine the specific function the thing dic 
		# will be needed, it's on the function_dic, and was
		# defined in body.py, for more info.
		else:
			# in most of the cases the thing is the third word:
			# genera una [imagenes|imagen] de algo
			# genera un [qr] de algo
			# un this case, the thing_recognizer will be used
			# then select the third word
			third_word = message.split(' ')[2]
			# recognize or "correct" the word
			thing = self.thing_recognizer(third_word)
			# once detected select the function
			function = self.function_dic['thing'][thing]
			return function