from data.memory import Memory
import numpy as np
#from interfaces import discord
from model.brain import Use

memory_routes = ('./data/data.txt', './data/memory.txt')

module = input('\ntesting-module-$ ')
inform = Memory(memory_routes[0]) # words saved
memory = Memory(memory_routes[1]) # words saved in lambda


if module == 'm':

  print('## Testing memory...\n')

  # equal numbers
  memory['int'] = 1
  print(memory['int'], type(memory['float']))
  memory['float'] = 3.1416
  print(memory['float'], type(memory['float']))
  # append numbers
  memory.append('int',2)
  # memory.append('int',3)
  memory.append('float',2.7219)
  # memory.append('float',3.7219)
  print(memory['int'], memory['float'])
  # create lists
  memory['intlist'] = [1,2,3,4]
  memory['strlist'] = ['a','b','c']
  # equal strs
  print(memory['intlist'], memory['strlist'])
  memory['intlist'] = [1,2,3,4]
  memory['strlist'] = ['a','b','c']
  memory.remove('intlist', '2')
  print(memory['intlist'], memory['strlist'])
  # delete all 
  # memory.delete('float')
  # memory.delete('int')

elif module == 'u':
  use = Use()
  sentence = "ponnme hicaru-nara"
  print(memory['musica'], 'memoey')
  res = use('hicaru-nara',memory['musica'],sentence)
  print(res)