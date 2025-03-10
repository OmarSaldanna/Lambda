# Lambda's memory, yesterday it uses txt files
import os
import json
import pytz
import telebot
import hashlib
import datetime

# memory route params
memory_path = os.environ["MEMORY_PATH"]
log_path = os.environ["LOG_PATH"]


#########################################################################################
################################# Memory Files' Handlers ################################
#########################################################################################

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
      json.dump(self.dic, write_file, indent=int(os.environ["INDENT"]), ensure_ascii=False)

  # update file
  def update (self, data: dict):
    # iterate the new dic with the changes
    for key, value in data.items():
      # make the changes
      self.dic[key] = value
    # and save them
    with open(self.file_path, "w") as write_file:
      json.dump(self.dic, write_file, indent=int(os.environ["INDENT"]), ensure_ascii=False)

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
  return Memory(f'{memory_path}{database}/{_id}.json')

# create a memory file, mostly used when memory
# files from users and servers are not found
def create_memory(path: str, content: dict):
  with open(memory_path+path, "w") as write_file:
    json.dump(content, write_file, indent=int(os.environ["INDENT"]), ensure_ascii=False)

# make a memory file for user, server or images
# based on the prototypes.json
def make_memory(_id: str, database: str):
  # load the prototypes
  mem = Memory(os.environ["PROTOTYPES_PATH"])
  # select the db prototype
  prototype = mem[database]
  # create the memory file
  create_memory(
    # make the memory file with the id and in the
    # correct db folder
    f'{database}/{_id}.json',
    # and make it based on the prototype
    prototype
  )
  return get_memory(f'{database}/{_id}')

#########################################################################################
################################# Special Functions #####################################
#########################################################################################

# function for time, for the log format
def get_time():
  # Get the current date and time in UTC
  utc_now = datetime.datetime.utcnow()
  # Create a timezone object for CDMX (UTC-5)
  cdmx_tz = pytz.timezone(os.environ["TIMEZONE"])
  # Convert the UTC time to CDMX time
  cdmx_now = utc_now.replace(tzinfo=pytz.utc).astimezone(cdmx_tz)
  # Print the current date and time in CDMX time
  return str(cdmx_now.strftime(os.environ["TIMEFORMAT"]))

# append smth to a log file
def app_to_log(file_name: str, msg: str):
  # get the time
  time = get_time()
  # Open a file in append mode
  with open(log_path + file_name + os.environ["LOGS_EXT"], 'a') as file:
    # append the line to the log file
    file.write(f'{msg} {time}\n')

# hash function
def generate_hash(string: str):
  # hash using SHA-256
  hash_object = hashlib.sha256()
  # convert the string to bytes
  string_bytes = string.encode(os.environ["ENCODE"])
  # ceate the hash object
  hash_object.update(string_bytes)
  # get the hexadecimal hash
  hash_result = hash_object.hexdigest()
  # return
  return hash_result

# controller to send alerts to telegram
def telegram_alert(content: str):
  # send telegram messages to the chat using system
  command = f"""curl -X POST "https://api.telegram.org/bot$TELEGRAM/sendMessage" -d "chat_id=$alert_chat&text={content}" """
  # print(command)
  os.system(command)
  # save a log
  app_to_log('telegram', f"[DB] {content}")
  # and return
  return 'ok'

# controller to list files in directories
# used mainly for json files
def list_file_names (folder: str, removed_letters=5):
  return [f[:-5] for f in os.listdir(folder) if f.endswith(".json")]