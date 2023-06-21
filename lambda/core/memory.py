# Lambda's memory, yesterday it uses txt files
import json
import pytz
import datetime

memory_path = './memory/'
log_file = memory_path + 'log.txt'


# class for use lambda memory files
class Memory:

  # open the json
  def __init__ (self, file_path: str):
    # open the dic
    try:
      self.file_path = file_path
      self.dic = json.load(open(file_path))
    except:
      raise ValueError(f"bad json file {file_path}")

  # save changes
  def write (self):
    with open(self.file_path, "w") as write_file:
      json.dump(self.dic, write_file, indent=4)

  def __getitem__ (self, key):
    try:
      return self.dic[key]
    except:
      raise KeyError(f"[MEMORY] -> KeyError: {key}")


# read the memory files
def get_memory(mem: str):
  # returns a memory instance
  return Memory(f'{memory_path}{mem}.json')


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
def app_to_log(msg: str):
  # get the time
  time = get_time()
  # Open a file in append mode
  with open(log_file, 'a') as file:
    # append the line to the log file
    file.write(f'{msg} at {time}\n')