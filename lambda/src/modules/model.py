import numpy as np

##################################### WORD RECOGNIZER

def dot_product(vects):
  sum = 0
  for v1,v2 in zip(vects[0], vects[1]):
    sum += v1*v2
  return sum

def norm(vect):
  # convert to np array
  v = np.array(vect)**2
  return np.sqrt(sum(v))

def generate_vectors(word1, word2):
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
        vects[j].append(0)
  return vects

# cosine of the angle between two vectors 
def proximity(vects):
  # apply the formula
  v1, v2 = vects
  return dot_product(vects) / (norm(v1) * norm(v2))

def word_recocgnizer(given_word, word_list, probs=False):
  proximity_list = []
  for word in word_list:
    # convert to lower
    vects = generate_vectors(given_word.lower(), word.lower())
    proximity_list.append(proximity(vects))
  # if the probs were requested
  if probs:
    return proximity_list
  # else return only the index
  return proximity_list.index(max(proximity_list))