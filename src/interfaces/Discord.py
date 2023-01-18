import discord

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as', self.user)

  async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
      return

    if message.content == 'lambda':
      await message.channel.send('Estoy aquí')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run('MTAyNDA1NjUwNTc4OTU4NzQ4Ng.GzYtmQ.l7Hbwpnk6Fuvx3dlA777fGlVjMWbZJLGilsf70')

"""
######################## HELPER COMMAND #######################

@client.command()
async def test(ctx):
  msg, msg_channel = ctx.message.content, ctx.message.channel 
  author, author_id = ctx.message.author, ctx.message.author.id
  try:
    voice_channel = ctx.author.voice.channel
  except:
    voice_channel = None
  
  print(msg)
  print(msg_channel)
  print(author)
  print(author_id)
  print(voice_channel)


######################### SMART COMMANDS #######################
# these are general purpose, depending on the sentences (spanish) given with -Lambda,
# for example: 

# -Lambda falta comprar shampoo
# -Lambda no hay pasta de dientes
# -Lambda necesitamos spaguetti

@client.command() # working on the next commit
async def Lambda(ctx):
  await ctx.send(f'Hola :3')


def launch(token):
  # run the bot with its token
  client.run(token)

"""






"""

######################### VOICE CHANNEL COMMANDS #######################

@client.command()
async def descarga(ctx):
  # obtain the message
  msg = ctx.message.content.split(' ')
  # verify the format -descarga [link] como [name]
  if len(msg) >= 4 and msg[2] == 'como': # correct format
    # then download the requested song
    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192'
      }],
    }
    url, name = msg[1], " ".join(msg[3:])
    print(f"\n==> descargando {name} de {url}...\n")
    # download the audio
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

    # once downloaded, rename the file, to know the file name
    for file in os.listdir("./"):
      if file.endswith('.m4a'):
        os.rename(file, "song.m4a")
    
    file_name = name.replace(' ', '_') # for save the file
    # then targeted the file, rename with the given name
    os.system(f"mv song.m4a {file_name}.m4a")
    # move it to music folder
    os.system(f"mv {file_name}.m4a ../music")
    # register the new song on the database
    database.append_list('musica', file_name)
    await ctx.send(f'exitosamente pirateado ;), guardado como {name}')


@client.command()
async def pon(ctx):
  msg = ctx.message.content
  song = " ".join(msg.split(' ')[1:])
  song = song.replace(' ', '_')

  # look for the name on the saved songs
  if song in database.give('musica'):
    print(f"\n==> reproduciendo {song.replace('_', ' ')}...\n")
    # select a voice channel
    try:
      channel_name = str(ctx.author.voice.channel)
    except:
      channel_name = "Animesito" # a voice channel of my server
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
    # instance a voice object, voice can only be created when the bot is already in the voice channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # most of the time voice will be none, always before connect()
    if voice is None or not voice.is_connected():
      # as the bot is disconnected, connect it
      await voiceChannel.connect()
    # instance again the voice, once connected the bot, it won't be none
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # the route of the song
    route = f"./../music/{song}.m4a"
    # finally put it in the voice
    voice.play(discord.FFmpegPCMAudio(route))
  # the song wasn't in list
  else:
    await ctx.send("Lo siento, {song} no ha sido pirateada aún")

@client.command()
async def llegale(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  # if the bot is connected, then it leaves
  if not voice is None or voice.is_connected():
    await voice.disconnect()

@client.command()
async def pausa(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  #else:
    # await ctx.send("No hay nada en el reproductor")

@client.command()
async def play(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  #else:
    #await ctx.send("No hay nada en el reproductor")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()

######################### STUFF COMMANDS #######################

# save stuff -sostenme
@client.command()
async def sostenme(ctx):
  await actions.sostenme(ctx.message)

# give back stuff -dame
@client.command()
async def dame(ctx):
  await actions.dame(ctx.message)

######################### ANIME ############################

# follow an anime -sigue anime [link] como [name]
@client.command()
async def sigueanime(ctx):
  await actions.sigue_anime(ctx.message)
  
# show animes in list -animes
@client.command()
async def animes(ctx):
  await actions.animes(ctx.message)

# show anime chapters -capitulos [name]
@client.command()
async def capitulos(ctx):
  await actions.capitulos(ctx.message)

######################### ADMIN FUNCTIONS #######################
# unique functions for me, db commands

# -save [key] [value]
@client.command()
async def save(ctx):
  if str(ctx.message.author) == 'OmarLarasa#8042':
    await actions.save(ctx.message)

# -give [key]
@client.command()
async def give(ctx):
  if str(ctx.message.author) == 'OmarLarasa#8042':
    await actions.give(ctx.message)

# -delete [key]
@client.command()
async def delete(ctx):
  if str(ctx.message.author) == 'OmarLarasa#8042':
    await actions.delete(ctx.message)

# -die
@client.command()
async def die(ctx):
  if str(ctx.message.author) == 'OmarLarasa#8042':
    await actions.die(ctx.message)

######################### WHITE LIST #######################

# # -salasegura para [@member1] [@member2] ...
# @client.command()
# async def salasegura(ctx):
#   # there's no white list active
#   if database.give('salasegura') == '':
#     msg = ctx.message.content
#     members = msg.split(' ')[2:] # ids mentions are like <@!id>
#     # extract the ids without symbols
#     member_ids = [m[3:len(m)-1] for m in members]
#     # add the bot id
#     member_ids.append(database.give('id'))
#     # save the members in the db

#     database.save_list('salasegura', member_ids)
#     # then join the bot to the channel voice if it isn't
#     # select a voice channel
#     try:
#       channel_name = str(ctx.author.voice.channel)
#     except:
#       channel_name = "Animesito"
#     voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
#     # instance a voice object, voice can only be created when the bot is already in the voice channel
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     # most of the time voice will be none, always before connect()
#     if voice is None or not voice.is_connected():
#       # as the bot is disconnected, connect it
#       await voiceChannel.connect()
#     # send a confirmation
#     await ctx.send(f"ya esta lista la sala segura para {' '.join(members)}")

#   # there's a white list active
#   else:
#     await ctx.send('no puedo hacer eso, ya hay una sala segura activa')

# # -agregarasala [@member1] [@member2] ...
# @client.command()
# async def agregarasala(ctx):
#   actual_members = database.give_list('salasegura') # read the actual members
#   # see if this person is in the members
#   person_id = str(ctx.message.author.id)
#   if person_id in actual_members:
#     # detect the new members
#     msg = ctx.message.content
#     new_members = msg.split(' ')[1:] # ids mentions are like <@!id>
#     # extract the ids without symbols
#     new_member_ids = [m[3:len(m)-1] for m in new_members]
#     # add the new members
#     for i in new_member_ids:
#       database.append_list('salasegura', i)
#     # send a message
#     await ctx.send('Nuevos miembros agregados')
#   else:
#     await ctx.send("lo siento, no tienes permiso para eso")

# -kickeardesala [@member1] [@member2] ...
# @client.command()
# async def eliminardesala(ctx):
#   actual_members = database.give_list('salasegura') # read the actual members
#   # see if this person is in the members
#   person_id = str(ctx.message.author.id)
#   remaining_members = []
#   if person_id in actual_members:
#     # detect the members to delete
#     msg = ctx.message.content
#     kick_members = msg.split(' ')[1:] # ids mentions are like <@!id>
#     # extract the ids without symbols
#     kick_member_ids = [m[3:len(m)-1] for m in kick_members]
#     # add the new members
#     for i in actual_members:
#       # add only the not kicked members
#       if i not in kick_member_ids:
#         remaining_members.append(i)
#     # save the new members
#     database.save_list('salasegura', remaining_members)
#     # send a confirmation
#     await ctx.send('Miembros eliminados')
#   else:
#     await ctx.send("lo siento, no tienes permiso para eso")

# # -salalibre
# @client.command()
# async def salalibre(ctx):
#   members = database.give_list('salasegura') # read the actual members
#   # see if this person is in the members
#   person_id = str(ctx.message.author.id)
#   if person_id in members:
#     # delete the white list
#     database.delete('salasegura')
#     # send a confirmation
#     await ctx.send('Listo, todos son libres de entrar')
#   else:
#     await ctx.send("lo siento, no tienes permiso para eso")

# # kick members that aren't in white list when they join the channel
# @client.event
# # hear any change in voice channel, someone unmutes or enters the channel
# async def on_voice_state_update(member:discord.Member, before, after):
#   members = database.give_list('salasegura') # read the member list
#   # detect if there's a white list active
#   if members != ['']:
#     # the sala segura is active
#     if str(member.id) not in members: # check if member is in list
#       await member.move_to(None) # diconect not in list user
    

"""