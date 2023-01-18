# internal lambda model for recognize words. Compares a given word
# with other words given in a list, this list of known words will
# be on the memory
import numpy as np

class Lambda_Word_Recognizer:
  def __init__(self, missing_char_number):
    self.missing_char_number = missing_char_number

  def __dot_product(self, vects):
    sum = 0
    for v1,v2 in zip(vects[0], vects[1]):
      sum += v1*v2
    return sum

  def __norm(self, vect):
    # convert to np array
    v = np.array(vect)**2
    return np.sqrt(sum(v))

  def generate_vectors(self, word1, word2):
    words = [word1, word2]
    # select the size of the largest word
    size = (len(word1) if len(word1) > len(word2) else len(word2))
    # create the numerical vectors
    vects = [[], []]
    # iterate the letters number
    for i in range(size):
      # iterate the words
      for j in range(2):
        try:
          # add the ascii code if there's a letter
          vects[j].append(ord(words[j][i]) -96) # normalize according ascii
        except:
          # there is no word
          vects[j].append(self.missing_char_number)
    return vects

  # cosine of the angle between two vectors as word similarity
  def __proximity(self, vects):
    # apply the formula
    v1, v2 = vects
    return self.__dot_product(vects) / (self.__norm(v1) * self.__norm(v2))

  def __call__(self, given_word, word_list, alert=False):
    proximity_list = []
    for word in word_list:
      # convert lower and then to vectors
      vects = self.generate_vectors(given_word.lower(), word.lower())
      # then calculate and register the probability
      proximity_list.append(self.__proximity(vects))
    if alert:
      print(f'==> model ==> comparing word [{given_word}] with word_list')
    # return all the probabilities
    return proximity_list