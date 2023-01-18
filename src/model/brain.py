# here will be a more simplified function or class to use
# the word recognizer, and don't depending on the type of
# model used. This module will be used for recognize and
# correcta words fo1r each lambda command available.

# from models import lambda_word_recognizer as recognizer
from model.models.lwr import Lambda_Word_Recognizer

# the purpose of this subclass is to give the model an
# eassier use and then use the model for correct almost
# every word it can. At this moment it is only for known
# words saved on the memory of lambda.

# the funcionality of this module will be reciving words
# and the sentence or command where the word is, for then
# return the full command or sentence corrected. This way
# lambda will be smart and will probably 

class Use:
  def __init__(self, probability_threshold=.85, missing_char_number=-10):
    self.probability_threshold = probability_threshold
    self.recognizer = Lambda_Word_Recognizer(missing_char_number=missing_char_number)

  # this is the general purpose function
  def __call__(self, word, word_list, sentence):
    # predict with the model
    print(word, word_list)
    probs = self.recognizer(word, word_list)
    # if the coincidence was not too strong
    if max(probs) < self.probability_threshold:
      return "Error, no pude reconocer el mensaje"
    # else: continue
    idx = probs.index(max(probs))
    correct_word = word_list[idx]
    corrected_sentence = sentence.replace(word, correct_word)
    return corrected_sentence
  
  # this will be for the "lambda commands", returns the sentence,
  # the object and the action
  def special(self, sentence):
    pass

# sample use()

print('#my brain has been activated...')