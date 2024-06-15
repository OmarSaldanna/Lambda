# Lambda Word Recognizer V3
# internal lambda model for recognize words. Compares a given word
# with other words given in a list, this list of known words will
# be on the memory.
# Now LWR includes numbers and doesn't throw error on symbols
import numpy as np
from unidecode import unidecode


class Lambda_Word_Recognizer:
  def __init__(self):
    # replace char
    self.ord_values = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '0': 26, '1': 27, '2': 28, '3': 29,
    '4': 30, '5': 31, '6': 32, '7': 33, '8': 34, '9': 35
  }

  def __pre_process_word(self, word):
    # unidecode
    word = unidecode(word)
    # and lower case
    word = word.lower()
    return word

  def __process_words(self, words):
    # first pre process
    words = [self.__pre_process_word(w) for w in words]
    # then turn the word into a vector
    vectors = []
    for word in words:
      word_vector = self.word_to_vector(word)
      vectors.append(word_vector)
    # return the vectors and the words
    return vectors, words

  def word_to_vector(self, word: str):
    # generate a zeros vector
    # each dimension is for each letter
    word_vector = np.zeros((len(self.ord_values.keys())))
    # and add the letters in the word
    for letter in word:
      # this try is in case of symbols
      try:
        # get the idx
        idx = self.ord_values[letter]
        # sum √(i+1) where the letter
        word_vector[idx] += np.sqrt(i+1)
      except:
        pass
    # return as a numpy array
    return word_vector

  def __distances(self, vector: np.array, vector_list: np.array):
    distances = []
    for v in vector_list:
      # calculate the distance from vector to all the vectors
      # in the vector list
      distance = np.linalg.norm(vector - v)
      distances.append(distance)
    return distances

  # convert the word_list to vectors and store that vectors
  # into the model to then make predictions
  def train(self, word_list: list):
    # get the vectors from all the words
    self.weights, self.labels = self.__process_words(word_list)


  def __call__(self, word: str):
    try:
      # pre process the word
      word = self.__pre_process_word(word)
      # get the vector of the word
      word_vector = self.word_to_vector(word)
      # calculate the distances between the word vector and weights
      distances = self.__distances(word_vector, self.weights)
      # get the closest distance
      closest = np.argmin(distances)
      # then return the label (word) predicted
      return self.labels[closest]
    except:
      raise ValueError(f"Error on prediction: {word}")
  

'''
# testing code
word_recognizer = Lambda_Word_Recognizer()
# testing params
given_word = "oromge"
word_list = ["apple", "orange", "banana", "grape", "mango", "strawberry", "watermelon"]
# train and predict
word_recognizer.train(word_list)
result = word_recognizer(given_word)
print(result)
'''