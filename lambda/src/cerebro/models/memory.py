# same as database but class and with other spesific functions
class Memory:
  def __init__ (self, route):
    # save the database route
    self.route = route
    
    # database "rules"
    self.key_separator = ':>:'
    self.val_separator = ':<:'
    self.sub_separator = '::'

  def __read_lines(self): # returns a list
    file = open(self.route, 'r') # open the memory file
    lines = file.read().split('\n') # read the file by lines
    file.close()
    return lines
  
  def __write_lines(self, lines): # recieves a list
    file = open(self.route, 'w') # open for write
    file.write('\n'.join(lines)) # write the new data
    file.close()

  def __find(self, key_to_find, lines, space, value=0):
    counter = -1
    for line in lines:
      key = line.split(space)[value]
      counter += 1
      if key == key_to_find:
        return counter
    return -1

  def __getitem__(self, key):
    lines = self.__read_lines() # read the file
    idx = self.__find(key, lines, self.key_separator) # look for the key
    if idx >= 0:
      res = lines[idx].split(self.key_separator)[1] # select the value
      if self.val_separator in res:
        res = res.split(self.val_separator)
    else:
      res = ''
    return res
  
  def __setitem__(self, key, value): # accepts lists and strs
    lines = self.__read_lines() # read the file by lines
    idx = self.__find(key, lines, self.key_separator) # look for the key to see if it exists
    # if it exists
    if idx >= 0:
      # update
      if type(value) == list: # if it's a list
        lines[idx] = f"{key}{self.key_separator}{self.val_separator.join(value)}" # write the list
      else:
        lines[idx] = f"{key}{self.key_separator}{value}" # write the str
    else:
      if type(value) == list: # if it's a list
        lines.append(f"{key}{self.key_separator}{self.val_separator.join(value)}") # add the new line
      else:
        lines.append(f"{key}{self.key_separator}{value}") # add the new line

    # write the changes
    self.__write_lines(lines)

  def append(self, key, new_value):
    # read the actual value
    actual_value = self.__getitem__(key)
    if type(actual_value) == list:
      # add the new value
      actual_value.append(new_value)
    else:
      # the values are a list
      actual_value = [actual_value, new_value]
    # and save the changes
    self.__setitem__(key, actual_value)

  def pop(self, key, i:int):
    # read the actual value
    actual_value = self.__getitem__(key)
    # delete the i value
    print(actual_value)
    try:
      actual_value.pop(i)
    except:
      print('>>Error en funcion pop en memory')
    # and save the changes
    self.__setitem__(key, actual_value)

  def remove(self, key, item:str):
    # read the actual value
    actual_value = self.__getitem__(key)
    # try to find the value and delete it
    try:
      actual_value.pop(actual_value.index(item))
    except:
      pass
    # and save the changes
    self.__setitem__(key, actual_value)