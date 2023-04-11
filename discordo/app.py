import os
import json
import discord
import requests
from discord.ext import commands
os.system('clear')

# load the token
info = json.load(open('./info.json'))
token = info['DISCORDO']
lambda_ip = info['HOST']['lambda_ip']
lambda_port = info['HOST']['lambda_port']
# the lambda api url
lambda_api = f'http://{lambda_ip}:{lambda_port}/lambda/discordo'


# define the intents
intents = discord.Intents.all()
intents.members = True
# instance the discord app
bot = commands.Bot(command_prefix='-', intents=intents)


# vip list: close friends that are allowed to use GPT
vips = info['VIPS']


# when the bot starts running
@bot.event
async def on_ready():
  print(f'im alive perros')

# when a message came
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  # to verify that lambda is alive
  if message.content in ['tas', 'estas']:
    #print(message.author)
    #print(str(message.author) in vips)
    await message.channel.send('of cors pa')

  # to use gpt3, restricted use to my close friends
  if message.content.split(' ')[0] in ['lambda', 'Lambda'] and str(message.author) in vips:
    # then consult to lambda
    print(f'[DISCORD] -> Using GPT3 -> {message.content}')
    # select the message content after the "lambda"
    msg = message.content.split(' ')[1:]
    msg = ' '.join(msg)
    # consult to lambda
    ans = requests.get(lambda_api + '/gpt', headers={'msg':msg}).json()
    print(ans['answer'])
    # send the answer to discord
    await message.channel.send(ans['answer'])

  # to use an specific command that requires memory or sth
  elif message.content.split(' ')[0] in ['l', 'L']:
    # then consult to lambda
    print(f'[DISCORD] -> Using Command -> {message.content}')
    # send all the mesage without the l or the lambda part
    msg = message.content.split(' ')[1:]
    msg = ' '.join(msg)
    # consult to lambda
    ans = requests.get(lambda_api + '/commands', headers={'msg':msg}).json()
    print(ans['answer'])
    await message.channel.send(ans['answer'])

# run the bot
bot.run(token)
