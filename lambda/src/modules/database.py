## GENERAL FUNCTIONS

db_route = "./modules/database.txt"
ans_start = '\n\t > '

# databaset "rules"
key_separator = ':>:'
val_separator = ':<:'
sub_separator = '::'

############################ GENERAL FUNCTIONS ########################

# database format: key:>:value\n
def find(key_to_find, lines, space, value=0):
  counter = -1
  for line in lines:
    key = line.split(space)[value]
    counter += 1
    if key == key_to_find:
      return counter
  return -1

def delete(key):
  save(key, '', delete=True)

def save(key, val, delete=False):
  file = open(db_route, 'r') # first read the file
  lines = file.read().split('\n') # read the file by lines
  file.close() # close
  idx = find(key, lines, key_separator) # look for the key to see if it exists
  # if it exists
  if idx >= 0:
    # delete the register
    if delete:
      lines.pop(idx) # delete the line
    # for update
    else:
      lines[idx] = f"{key}{key_separator}{val}" # write the new line
  else:
    if not delete:
      lines.append(f"{key}{key_separator}{val}") # add the new line
  file = open(db_route, 'w') # open for write
  file.write('\n'.join(lines)) # write the new data
  file.close()

def give(key):
  file = open(db_route) # open the file
  lines = file.read().split('\n') # read the file by lines
  file.close()
  idx = find(key, lines, key_separator) # look for the key
  if idx >= 0:
    res = lines[idx].split(key_separator)[1] # select the value
  else:
    res = ''
  return res

def save_list(key, list, space=val_separator):
  val = space.join(list)
  save(key, val)

def give_list(key, space=val_separator):
  return give(key).split(space)

def append_list(key, val, space=val_separator):
  if give(key) == '':
    save(key, val)
  else:
    prev = give(key)
    new = f'{prev}{space}{val}'
    save(key, new)

def format_answer(value):
  try:
    value = val_separator.join(value)
  except:
    pass
  return f'{ans_start}{value.replace(val_separator, ans_start)}'

############################ SPECIFIC FUNCTIONS ########################

def save_stuff(name, stuff):
  save_list(f'stuff_{name}', stuff)

def give_stuff(name):
  key = f'stuff_{name}'
  res = give_list(key)
  if res == '':
    return f"{name} pero no has dado nada"
  else:
    return f'Aquí tienes {name} {format_answer(res)}'

def get_animes():
  animes = {}
  try:
    for i in give_list('animes'):
      link, name = i.split(sub_separator)
      animes[link] = name
    return animes
  except:
    pass
  return animes

# TESTING

#save('nombre', 'lambda hawking')
#save('dueño', 'zero')
#delete('historia')

#print(give('nombre'))
#print(give('historia'))