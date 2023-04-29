# memory, yesterday it uses txt files
import json


class Memory:

  # open the json
  def __init__ (self, file_path):
    # open the dic
    self.file_path = file_path
    self.dic = json.load(open(file_path))

  # save changes
  def write (self):
    with open(self.file_path, "w") as write_file:
      json.dump(self.dic, write_file, indent=4)

  def __getitem__ (self, key):
    try:
      return self.dic[key]
    except:
      raise KeyError(f"[MEMORY] x-> KeyError: {key}")

# the memory files
def get_memory(mem):
  memory_files = {
    'memory': './lambda/modules/data/memory.json',
    'person': './lambda/modules/data/person.json',
    'social': './lambda/modules/data/social.json',
    'vocab': './lambda/modules/data/vocab.json',
    'code': './lambda/modules/data/code.json'
  }
  # returns a memory instance, this way the controlers
  # will read the brand new changes made for themselves
  return Memory(memory_files[mem])

print("[MEMORY] -> Memory Working")