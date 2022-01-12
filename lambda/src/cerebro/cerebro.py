from models.models import word_recocgnizer as recognizer
from models.memory import Memory

# instanse memory obj
memory = Memory('./memory.txt')

class Model:
  def __init__ (self, memory):
    self.memory = memory
    self.verb_position_limit = 3
    self.probability_threshold = .9
  
  def search_verb(self, sentence):
    verbs = memory['verbs'] # look for the registered verbs
    # try to find the verb on the first  words
    for word in sentence.split(' ')[:self.verb_position_limit]:
      idx, prob = recognizer(word, verbs)
      if prob > self.probability_threshold: # if there was a good coincidence
        break # stop trying more words
    # if there was no strong coincidence
    if prob < self.probability_threshold:
      raise ValueError("there's no verb detected")
    # there was a good coincidence
    else:
      return idx
    

  def __split_sentence(self,sentence):
    action_sentence, obj_sentence = 

  def __detect_obj(self, sentence):
    pass

  def __detect_act(self, sentence, obj):
    pass

  def __call__(self, sentence):
    print(sentence)
    # detect the object from the sentence
    # obj = self.__detect_obj(sentence)
    # detect the action to do to the object
    # act = self.__detect_act(sentence, obj)
    # then make the action on the object
    

model = Model(memory)
model('Ya no tenemos arroz')