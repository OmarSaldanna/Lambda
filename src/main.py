# access to lambda memory
from memory.memory import Memory
# lambda interfaces to communications
# Discord, Email, Whatsapp an API
from interfaces import Discord
# Lambda module od IA
from model.brain import Use
# other things
import json
import os


path = './src/'


# bot info to run all the interfaces
info = json.load(open(path + 'info.json'))

# memory for specific information such as
# memory = Memory(path + 'data/data/memory.txt') # names, dates, links
# memory for known words for talking, like
# vocab = Memory(path + 'data/data/vocab.txt') # verbs, nouns, idioms
# memory for storaged data like models or numerical stuff
# data = Memory(path + 'data/data/data.txt') # on development

# all lambda modules to language functions
# use = Use() # this one is to correct 
# ...