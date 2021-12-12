import discord
from actions import *
from modules import database
from discord.ext import commands
import youtube_dl
import os
# brew install ffmpeg
# pip install PyNaCl


# instance the bot
client = commands.Bot(command_prefix="-")

# python discord works like js events
# for each event detected we can make sth
# and it's an asyinchronous library, then
# it works with callbacks, like js. All
# the names of the functions are defined
# in the discord library

@client.event
# when the bot is ready to be used
async def on_ready():
  # print the username
  print(f"I'm Lambda :D\tSoy un bot de Omar\tIch heiße Lambda")

# @client.event
# # if it receives a msg
# async def on_message(msg):
#   # if the msg is from the bot
#   if msg.author == client.user:
#     return
  
#   # a simple hello -hello
#   elif msg.content.startswith('-hola lambda'):
#     # it pretty much like js, wait until 
#     # this line be executed
#     await msg.channel.send(f"Holaa {msg.author} uwu")


@client.command()
async def pon(ctx, url:str):
  song_there = os.path.isfile("song.m4a")
  try:
    if song_there:
      os.remove("song.m4a")
  except PermissionError:
    await ctx("Espera a que lo que se esta repreduciendo termine")
    
  link = "https://www.youtube.com/watch?v=y2nCXaBhHfs"
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="manga")
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  
  if voice is None or not voice.is_connected():
    await voiceChannel.connect()

  # voice can only be created when the bot is already in the voice channel
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'm4a',
      'preferredquality': '192'
    }],
  }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

  for file in os.listdir("./"):
    if file.endswith('.m4a'):
      os.rename(file, "song.m4a")
  
  voice.play(discord.FFmpegPCMAudio("song.m4a"))

@client.command()
async def algo(ctx):
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="manga")
  # voice can only be created when the bot is already in the voice channel
  await voiceChannel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.play(discord.FFmpegPCMAudio("song.m4a"))

@client.command()
async def llegale(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not voice is None or voice.is_connected():
    await voice.disconnect()


@client.command()
async def pausa(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("No hay nada en el reproductor")

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

  ######################### TESTING NEW THINGS #######################

  # # reproduce sth
  # elif msg.content.startswith('-pon'):
  #   link = "https://www.youtube.com/watch?v=y2nCXaBhHfs"
  #   voiceChannel = discord.utils.get(msg.guild.voice_channels, name="manga")
  #   voice = discord.utils.get(bot.voice_clients, guild=msg.guild)
  #   if not voice.is_connected():
  #     await voiceChannel.connects()
    


  ######################### STUFF #######################

  # # save stuff -sostenme
  # elif msg.content.startswith('-sostenme'):
  #   await sostenme(msg)

  # # give back stuff -dame
  # elif msg.content.startswith('-dame'):
  #   await dame(msg)

#   ######################### ANIME #######################
#####
#   # follow an anime -sigue anime [link] como [name]
#   elif msg.content.startswith('-sigue anime'):
#     await sigue_anime(msg)
  
#   # show animes in list -animes
#   elif msg.content == '-animes':
#     await animes(msg)

#   # show anime chapters
#   elif msg.content.startswith('-capitulos'):
#     await capitulos(msg)

#   ######################### ADMIN FUNCTIONS #######################

#   ## unique functions for me, db commands $save [key] [value]
#   elif msg.content.startswith('$save') and str(msg.author) == 'OmarLarasa#8042':
#     await save(msg)

#   # $give [key]
#   elif msg.content.startswith('$give') and str(msg.author) == 'OmarLarasa#8042':
#     await give(msg)

#   # $delete [key]
#   elif msg.content.startswith('$delete') and str(msg.author) == 'OmarLarasa#8042':
#     await delete(msg)

#   # sudo shutdown
#   elif msg.content == '$die' and str(msg.author) == 'OmarLarasa#8042':
#     await die(msg)

#   ######################### VOICE CHANNEL #######################
  
#   elif msg.content == '-unete':
#     channel = msg.author.voice.channel
#     await channel.connect()
#     print(channel)
#     await msg.channel.send('Ya llegue prros, que quieren?')

#   elif msg.content.startswith('-sala segura para'):
#     # if is posible to create a sala segura
#     if db.give('salasegura') == '':
#       members = msg.content.split()[3:] # select the members
#       # convert to ids
#       ids = []
#       for m in members:
#         # <@!id>
#         ids.append(m[3:len(m)-1])
#       # append bot id
#       ids.append(db.give('id'))
#       #members.append(bot.user) # add the bot
#       db.save_list('salasegura', ids) # save the members
#       await msg.channel.send("ya estan listados en la sala segura, avisenme cuando entrar :]")
#     # if it isn't
#     else:
#       await msg.channel.send(f'{msg.author} lo siento, ya hay una sala segura activa')

#   elif msg.content.startswith('-agregar a sala'):
#     registered = db.give_list('salasegura') # read the actual
#     # if the user isn't able to do that
#     if str(msg.author.id) not in registered:
#       await msg.channel.send("Lo siento, no tienes permiso para eso")
#     # if it is in the list
#     else:
#       members = msg.content.split()[3:] # read the new
#       members = [m[3:len(m)-1] for m in members]# format
#       for member in members: # append each member
#         if member not in registered: # if member not in list
#           db.append_list('salasegura', member) # save the new member
#       await msg.channel.send(f"Listo {msg.author}, miembros agregados a la lista")

#   elif msg.content.startswith('-eliminar de sala'):
#     registered = db.give_list('salasegura') # read the actual
#     # if the user isn't able to do that
#     if str(msg.author.id) not in registered:
#       await msg.channel.send("Lo siento, no tienes permiso para eso")
#     # if it is in the list
#     else:
#       to_delete = msg.content.split()[3:] # read the new
#       to_delete = [m[3:len(m)-1] for m in to_delete] # format
#       new_members = []
#       for member in registered: # append each member and not the to_del
#         if member not in to_delete: # if member in list
#           new_members.append(member) # save the remainning members
#       db.save_list('salasegura', new_members) # save the changes
#       await msg.channel.send(f"Listo {msg.author}, miembros eliminados de la lista")

#   elif msg.content == '-sala libre':
#     # if there's no sala segura
#     if db.give('salasegura') == '':
#       await msg.channel.send(f'{msg.author} lo siento, no hay una sala segura activa')
#     # if there is
#     else:
#       members = db.give_list('salasegura')
#       # if the user is not in the member list
#       if str(msg.author.id) not in members:
#         await msg.channel.send(f'{msg.author} lo siento, no puedes desactivar la sala segura')
#       # if it is
#       else:
#         db.delete('salasegura') # clear the sala segura
#         await msg.channel.send(f'Okey {msg.author}, ya esta desactivada')

# # 
# @client.event
# # hear any change in voice channel, someone unmutes or enters the channel
# async def on_voice_state_update(member : discord.Member, before, after):
#   members = db.give_list('salasegura') # read the member list
#   member_id = member.id # select the member id
#   # the sala segura is active
#   if str(member_id) not in members and members != [''] and str(member_id) != str(client.user): # check if member is in list
#     await member.move_to(None) # diconect not in list user
#     await member.send(f"Lo siento, no puedo dejarte entrar a la *sala segura*")
    

# load the bot token
token = database.give('token')
# run the bot
client.run(token)