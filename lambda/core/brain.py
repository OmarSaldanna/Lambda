# This is the Lambda main module, here is where the
# funcions are linked to words based on the incoming
# messages.
# AI class, when is called it recieves a message and
# returns an answer. As easy as that. 

# import the Lambda Word Recognizer
from core.lwr import Lambda_Word_Recognizer
# import the DB handler
from modules.db import DB
# also libraries
import importlib
import os


class Brain:

  # instance DB handler, and a LWR to correct verbs
  def __init__ (self):
    # create a list of all the verbs
    known_words = os.listdir(os.environ["MEMORY_PATH"] + "verbs")
    # remove the "".json"
    known_words = [file[:-5] for file in known_words if file.endswith('.json')]
    # instance a lambda word recognizer for all the known words
    self.word_recognizer = Lambda_Word_Recognizer()
    # train the model with the knwon words
    self.word_recognizer.train(known_words)
    # instance the db
    self.db = DB()

  # function used to report errors on lambda skills, it will be saved on
  # the db on errors and also a report will be sent to the admin via telegram.
  # The error will be reported as well as the user, server and the message
  def __error_report (self, error_str: str, params: tuple):
    message, member, server = params
    # save it in the error db
    self.db.post("/errors", {
      "data": {
        "call": message,
        "code": error_str,
        "member": member,
        "server": server
      }
    })
    # and in logs
    self.db.post("/logs", {
      "db" : "errors",
      "data": f"[{member}] {message}"
    })

  # function used to run lambda skills
  def __call_function(self, lib_name: str, params):
    try:
      # import the function
      main_module = importlib.import_module(f"skills.{lib_name}")
      # and use it
      return main_module.main(params)
    # if the skill doesn't work, then use the error report
    except Exception as e:
      # if is on dev
      if os.getenv("dev") == "yes":
        # show the error code
        print(str(e))
      # use the report
      self.__error_report(str(e), params)
      # now throw a simple message
      return [{
        "type": "error",
        "content": "Lo siento, ocurrió un error, comprueba que tu comando este bien escrito. Este error será reportado para su solución."
      }]

  # main function
  def __call__ (self, message: str, author: str, server: str):
    # select the first word of the message
    first_word = message.split(' ')[0]
    # correct the first word
    verb = self.word_recognizer(first_word)
    # now load the verb data from the db
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