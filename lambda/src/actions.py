import modules.database as db

async def not_found(msg):
  await msg.channel.send(f'*Error 404:* Dile a mi huevón dueño que me repare')

######################### STUFF #######################

async def sostenme(msg):
  stuff = msg.content.split()[1:] # split only by spaces
  db.save_list(f'stuff_{msg.author}', stuff) # save the stuff as list
  # alerts
  print(msg.author, 'guarda en stuff')
  await msg.channel.send(f'Okey {msg.author}, ahí me avisas')

async def dame(msg):
  key = f'stuff_{msg.author}'
  res = db.give_list(key)
  if res == '':
    await msg.channel.send(f"{msg.author} pero no has dado nada")
  else:
    await msg.channel.send(f'Aquí tienes {msg.author} {db.format_answer(res)}')

######################### ANIME #######################

# follow an anime -sigue anime [link] como [name]
async def sigue_anime(msg):
  lst = msg.content.split() 
  # select the data so save
  link, name = lst[2], lst[4]
  val = f'{link}::{name}'
  # verify if the anime is already registered
  animes = db.get_animes()
  if link not in animes.keys():
    try:
      # if already there are animes
      db.append_list('animes', val)
    # if it dont works
    except:
      db.save('animes', val)
    print(f'saved {name} in animes')
    await msg.channel.send(f'Perfecto {msg.author}, ya agregue {name} a la lista :D')
  # if it already exists
  else:
    await msg.channel.send(f'{name} ya está en la lista {msg.author}')

# show animes in list -animes
async def animes(msg):
  animes = db.get_animes()
  text = [f'{name} - {link}' for link,name in zip(animes.keys(), animes.values())]
  text = '\n\t> '.join(text)
  await msg.channel.send(f'Estos son los animes en lista: \n\t > {text}')

# show anime chapters -capitulos de [anime]
async def capitulos(msg):
  # show anime chapters
  await not_found(msg)

######################### ADMIN FUNCTIONS #######################

# $save [key] [value]
async def save(msg):
  msg_list = msg.content.split()
  key, val = msg_list[1], msg_list[2]
  db.save(key, val)
  await msg.channel.send('-> saved')

# $give [key]
async def give(msg):
  msg_list = msg.content.split()
  key = msg_list[1]
  val = db.give(key)
  val = val.replace(' ', '\n\t> ')
  await msg.channel.send(f'-> giving: {val}')

# $delete [key]
async def delete(msg):
  msg_list = msg.content.split()
  key = msg_list[1]
  db.delete(key)
  await msg.channel.send(f'-> deleting: {key}')

# sudo shutdown
async def die(msg):
  await msg.channel.send(f'que buen momento para shutdaunearse\nse me cuidan')
  # empty the salasegura
  db.delete('salasegura')
  # stop the program
  exit()