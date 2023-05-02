# Lambda's memory, yesterday it uses txt files
# Discordo version, it only has the log function
import json
import pytz
import datetime


log_file = './ram/log.txt'


# class for use lambda memory files
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


# read the memory files
def get_memory(mem):
  memory_files = {
    'memory': './lambda/modules/data/memory.json',
    'person': './lambda/modules/data/person.json',
    'social': './lambda/modules/data/social.json',
    'vocab': './lambda/modules/data/vocab.json',
    'code': './lambda/modules/data/code.json',
    'services': './ram/services.json',
    'info': './ram/info.json',

  }


  # returns a memory instance, this way the controlers
  # will read the brand new changes made for themselves
  return Memory(memory_files[mem])


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


# append smth to the log file
def app_to_log(msg, initial=False):
  # get the time
  time = get_time()
  # Open a file in append mode
  with open(log_file, 'a') as file:
    # initial is true if it's appending the first 
    if not initial:
      # Write a string to the file
      file.write(f'{time} {msg}')
    else:
      file.write(f'\n\n[LAMBDA] -> starting\n\n{time} {msg}')


# a specific function that helps refresh memory variables
def refresh_users(var):
  # read the memory
  mem = get_memory('info')
  # and return the variabes
  var = mem['VIPS']