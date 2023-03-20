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
bot = commands.Bot(command_prefix='λ', intents=intents)

# when the bot starts running
@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

# when a message came
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content == 'estas?':
    await message.channel.send('Estoy aquí')

  # here is where the discord app calls to lambda
  elif message.content.split(' ')[0] in ['lambda', 'Lambda', 'l', 'L']:
    # then consult to lambda
    print(f'[DISCORD] -> {message.content}')
    # send all the mesage without the l or the lambda part
    msg = message.content.split(' ')[1:]
    msg = ' '.join(msg)
    # consult to lambda
    ans = requests.get(lambda_api, headers={'msg':msg}).json()
    print(ans)
    await message.channel.send(ans['answer'])

# run the bot
bot.run(token)