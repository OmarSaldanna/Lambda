# This is the lambda main module, here is where the
# funcions are linked to words based on the incoming
# messages.
# AI class, when is called it recies a message and
# returns an answer. As easy as that. 

# import all the models
# from core.models import lmm, lwr

from core.models.lmm import Lambda_Mindful_Messenger
from core.models.lwr import Lambda_Word_Recognizer

# import the functions dic, and inside are the verbs
# and questions list, used on lambda word recognizer
# from body import function_dic

# this will module will be useful to determine easily
# if a word is a verb or a question
from core.extensions import list_dic


class AI:
  # instance all the models and the function dic
  def __init__ (self, function_dic: dict):
    self.function_dic = function_dic
    # get the all the known words in lists
    question_dic = function_dic['question']
    thing_dic = function_dic['thing']
    verb_dic = function_dic['verb']
    # create a list of all the known words for orders
    known_words = question_dic.get_all_keys() + verb_dic.get_all_keys()

    # lambda word recognizer for all the known words
    self.word_recognizer = Lambda_Word_Recognizer()
    # train the model with the knwon words
    self.word_recognizer.train(known_words)

    # the LMM will need a new instance of LWR trained with the 
    # thing_list since some words are associated to more than
    # one function, and things are the differences on the function
    # calling. This has a better explanation in vocab file and LMM
    thing_recognizer = Lambda_Word_Recognizer()
    thing_recognizer.train(thing_dic.get_all_keys())

    # and instance the lmm model with the trained word recognizer
    self.lmm = Lambda_Mindful_Messenger(thing_recognizer, function_dic)

    # form a list_dic with the questions and the verbs, to
    # help determining wether is a verb or a question. Thus
    # the keys will be the questions and verbs and the values
    # "question" or "verb"
    self.verb_or_question = list_dic(
      question_dic.get_all_keys() + verb_dic.get_all_keys(),
      ["question" for _ in range(len(question_dic.get_all_keys()))] + \
      ["verb" for _ in range(len(verb_dic.get_all_keys()))],
      "Error"
    )

  def __call__ (self, message: str, author: str):
    # select the first word of the message
    first_word = message.split(' ')[0]
    # correct the first word
    corrected_first_word = self.word_recognizer(first_word)
    # see if it's a verb or a question
    tag = self.verb_or_question[corrected_first_word]
    # now let the Lambda Mindful Messager associate the command
    # with the lambda function
    function = self.lmm(message, tag, corrected_first_word)
    # then call the function. All the functions only receive 2
    # parameters from the message, the message and the author.
    # All that functions return answers.
    answer = function(message, author)
    # just return the anser
    return answer

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