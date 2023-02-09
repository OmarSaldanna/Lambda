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

