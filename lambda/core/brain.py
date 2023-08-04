# This is the lambda main module, here is where the
# funcions are linked to words based on the incoming
# messages.
# AI class, when is called it recies a message and
# returns an answer. As easy as that. 

# import all the models
from core.models.lwr import Lambda_Word_Recognizer

# import the functions dic, and inside are the verbs
# and questions list, used on lambda word recognizer
# from body import function_dic

# import all the modules
from core.modules import OpenAI, DB
# libraries
import os
import importlib


class AI:
  # instance all the models and the function dic
  def __init__ (self):
    # create a list of all the known verbs
    known_words = os.listdir("db/data/verbs")
    known_words = [file[:-5] for file in known_words if file.endswith('.json')]
    # lambda word recognizer for all the known words
    self.word_recognizer = Lambda_Word_Recognizer()
    # train the model with the knwon words
    self.word_recognizer.train(known_words)
    # instance the db
    self.db = DB()

  # function used to run lambda skills
  def __call_function(self, lib_name: str, params):
    #try:
    # import the function
    main_module = importlib.import_module(f"skills.{lib_name}")
    # and use it
    return main_module.main(params)
    #except:
      # throw a simple message
      # return [{
      #  "type": "error",
      #  "content": "Lo siento, ocurrió un error, comprueba que tu comando este bien escrito. \
      #  Este error será reportado para su solución."
      #}]


  # main function
  def __call__ (self, message: str, author: str, server: str):
    # select the first word of the message
    first_word = message.split(' ')[0]
    # correct the first word
    verb = self.word_recognizer(first_word)
    # now load the db from the verb
    verb_data = self.db.get('/verbs', {
      'verb': verb
    })['answer']
    # there are general functions, and multi functions
    if verb_data['type'] == 'multi': # multi function
      # then the objects are the keys of verb_data
      # and a LWR is needed to correct the word and
      # call the right function
      things = set(verb_data.keys()) - {'type'}
      thing_recognizer = Lambda_Word_Recognizer()
      # train the LWR with the things of the verb
      thing_recognizer.train(list(things))
      # then correct the word
      third_word = message.split(' ')[2]
      thing = thing_recognizer(third_word)
      # and select the function and run it
      return self.__call_function(
        # and pass the params
        verb_data[thing], (message, author, server)
      )
    # general function: only has one function
    elif verb_data['type'] == 'general':
      # since there's only one function then use it
      return self.__call_function(
        # and pass the params
        verb_data['function'], (message, author, server)
      )
    # error on function type
    else:
      # this is a clear error on db
      raise ValueError(f"Error on database, verb: {verb}, type unknown")
      

  # this is a fast function, independent. This is a simple
  # function for fast usage, like: Lambda, ...
  def chat(self, message: str, author: str, server: str):
    # instance openai module
    openai = OpenAI(author)
    # now call gpt
    return openai.gpt(message)


'''
ai = AI(function_dic)
# verbs
print(ai('dime cual es la capital de Mexico', 'kerr'))
print(ai('crea un QR con algo', 'kerr'))
print(ai('genera una imagen de algo', 'kerr'))
print(ai('genera dos imagenes de algo', 'kerr'))
# questions
print(ai('cómo estas?', 'kerr'))
print(ai('que sabes hacer', 'kerr'))
print(ai('Qué es lo que quieres ?', 'kerr'))
print(ai('Cuándo fue la ultima vez que te reiniciaste', 'kerr'))
'''