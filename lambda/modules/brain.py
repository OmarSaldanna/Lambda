# here will be a more simplified function or class to use
# the word recognizer, and don't depending on the type of
# model used. This module will be used for recognize and
# correcta words fo1r each lambda command available.

from modules.models.lwr import Lambda_Word_Recognizer
from modules.models.gpt import GPT
from modules.models.dalle import DALLE

# the purpose of this class is to give the model an
# eassier use and then use the model for correct almost
# every word it can. At this moment it is only for known
# words saved on the memory of lambda.

# the funcionality of this module will be reciving words
# and the sentence or command where the word is, for then
# return the full command or sentence corrected. This way
# lambda will be smart and will probably recognize comands
# for IoT interaction

class AI:
  def __init__(self, openai_token, probability_threshold=.95, missing_char_number=-10):
    # lwr instance
    self.probability_threshold = probability_threshold
    self.lwr = Lambda_Word_Recognizer(missing_char_number=missing_char_number)

    # gpt-3 instance
    self.gpt = GPT(openai_token)
    self.dalle = DALLE(openai_token)

  # this is the general purpose function
  def check_sentence(self, word, word_list, sentence):
    # predict with the model
    probs = self.lwr(word, word_list)
    # if the coincidence was not too strong
    if max(probs) < self.probability_threshold:
      return "Error, no pude reconocer la palabra"
    # else: continue
    idx = probs.index(max(probs))
    correct_word = word_list[idx]
    corrected_sentence = sentence.replace(word, correct_word)
    return corrected_sentence

  # useful to detect if a word is in a word_list
  # will be use in a function dictionary and for recognized words
  # like animes, songs, functions, etc.
  def recognize_word(self, word, word_list):
    # predict with the model
    probs = self.lwr(word, word_list)
    # if the coincidence was not too strong
    if max(probs) < self.probability_threshold:
      return False
    # else, return the word with more relation
    else:
      # index of the max prob
      word_idx = probs.index(max(probs))
      # return the word
      return word_list[word_idx]
  
  # use chat gpt
  def gpt3(self, sentence):
    return self.gpt(sentence)

  # generate custom images
  def dalle(self, sentence):
    return self.dalle(sentence)
