# Lambda's memory, yesterday it uses txt files
# Discordo version, it only has the log function
import pytz
import datetime

log_file = './ram/log.txt'

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