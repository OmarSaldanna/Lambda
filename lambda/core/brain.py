# This is the lambda main module, here is where the
# funcions are linked to words based on the incoming
# messages.
# AI class, when is called it recieves a message and
# returns an answer. As easy as that. 

# import all the models
from core.models.lwr import Lambda_Word_Recognizer

# import needed modules
from core.modules import OpenAI, DB
# and libraries
import os
import importlib
import telebot
from dotenv import load_dotenv

# load the .env variables
load_dotenv()


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
    # get the telegram variables: token, chat id
    self.telegram_chat = os.getenv("alert_chat")
    # instance the telebram bot
    self.tbot = telebot.TeleBot(os.getenv("TELEGRAM"))

  # function used to report errors on lambda skills, it will be saved on
  # the db on errors and also a report will be sent to the admin via telegram.
  # The error will be reported as well as the user, server and the message
  def __error_report (self, error_str: str, params: tuple):
    message, member, server = params
    # send the report to telegram
    try:
      # send the messages to the chat
      self.tbot.send_message(self.telegram_chat, f"Error on: {message}\n\n{error_str}")
    except:
      print("Error sending message for telegram")
    # now save it in the error db
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
    openai = OpenAI(author, server)
    # try to make the answer shorter as possible
    message += ". Que tu respuesta sea breve y concisa."
    # now call gpt
    return openai.gpt(message)
