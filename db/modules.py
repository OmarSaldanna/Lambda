# Lambda's memory, yesterday it uses txt files
import json
import pytz
import datetime
import hashlib

memory_path = './db/data/'
log_path = './db/data/log/'

# class for use lambda memory files
class Memory:
  # open the json
  def __init__ (self, file_path: str):
    # open the dic
    try:
      # save the file path
      self.file_path = file_path
      # open the json file
      with open(self.file_path, "r") as f:
        # save the info
        self.dic = json.load(f)
    except:
      raise ValueError(f"[DB] -> bad json file {file_path}")

  # save changes
  def write (self):
    with open(self.file_path, "w") as write_file:
      json.dump(self.dic, write_file, indent=4, ensure_ascii=False)

  # update file
  def update (self, data: dict):
    # iterate the new dic with the changes
    for key, value in data.items():
      # make the changes
      self.dic[key] = value
    # and save them
    with open(self.file_path, "w") as write_file:
      json.dump(self.dic, write_file, indent=4, ensure_ascii=False)

  # select items
  def __getitem__ (self, key: str):
    try:
      return self.dic[key]
    except:
      raise KeyError(f"[MEMORY] -> KeyError: {key}")

  # set items
  def __setitem__ (self, key: str, value):
    try:
      self.dic[key] = value
    except:
      raise KeyError(f"[MEMORY] -> KeyError: {key}")

  # in case of print the memory
  def __str__ (self):
    return self.dic


# read the memory files
def get_memory(mem: str):
  # returns a memory instance
  return Memory(f'{memory_path}{mem}.json')

# read the memory files by id
def get_memory_by_id(database: str, _id: str):
  # returns a memory instance
  # print(f'{memory_path}{database}/{_id}.json')
  return Memory(f'{memory_path}{database}/{_id}.json')

# create a memory file, mostly used when memory
# files from users and servers are not found
def create_memory(path: str, content: dict):
  with open(memory_path+path, "w") as write_file:
    json.dump(content, write_file, indent=4, ensure_ascii=False)

# make a memory file for user, server or images
# based on the prototypes.json
def make_memory(_id: str, database: str):
  # select the db prototype
  prototype = get_memory('prototypes')[database]
  # create the memory file
  create_memory(
    # make the memory file with the id and in the
    # correct db folder
    f'{database}/{_id}.json',
    # and make it based on the prototype
    prototype
  )
  return get_memory(f'{database}/{_id}')


# function for time, for the log format
def get_time():
  # Get the current date and time in UTC
  utc_now = datetime.datetime.utcnow()
  # Create a timezone object for CDMX (UTC-5)
  cdmx_tz = pytz.timezone('America/Mexico_City')
  # Convert the UTC time to CDMX time
  cdmx_now = utc_now.replace(tzinfo=pytz.utc).astimezone(cdmx_tz)
  # Print the current date and time in CDMX time
  return str(cdmx_now.strftime('[%Y-%m-%d - %H:%M:%S]'))


# append smth to a log file
def app_to_log(file_name: str, msg: str):
  # get the time
  time = get_time()
  # Open a file in append mode
  with open(log_path + file_name + '.txt', 'a') as file:
    # append the line to the log file
    file.write(f'{msg} {time}\n')

# hash function
def generate_hash(string: str):
    # hash using SHA-256
    hash_object = hashlib.sha256()
    # convert the string to bytes
    string_bytes = string.encode('utf-8')
    # ceate the hash object
    hash_object.update(string_bytes)
    # get the hexadecimal hash
    hash_result = hash_object.hexdigest()
    # return
    return hash_result