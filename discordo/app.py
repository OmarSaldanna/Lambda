import json
import discord
import controllers
from discord.ext import commands


# load the token
info = json.load(open('./ram/info.json'))
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
# admin: me, for lambda backups and lambda-cli
admin = info['ADMIN']

# when the bot starts running
@bot.event
async def on_ready():
    print(f'im alive perros')

# when a message came
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Admin level
    # lambda-cli, starts with a $
    if message.content[0] == '$' and str(message.author) == admin:
        print(f'[DISCORD] -> Admin on lambda-cli -> ')
        # use the lambda_cli controller
        pieces = controllers.lambda_cli(message)
        # send the message or messages
        for p in pieces:
            await message.channel.send(p)

    # VIP Level:
    # status #
    # chat gpt #
    # some services
    # fast research
    # save stuf
    elif str(message.author) in vips:

        # status
        if message.content in ['tas', 'tas?', 'Tas?']:
          print(f'[DISCORD] -> Ping from {message.author}')
          # confirmation messgae
          await message.channel.send('of cors pa')

        # gpt3 usage
        elif message.content[:7] in ['lambda ', 'Lambda ']:
            print(f'[DISCORD] -> Admin on lambda-cli -> ')
            # use the chat_gpt controller
            pieces = controllers.chat_gpt(message, lambda_api)
            # send the message or messages
            for p in pieces:
                await message.channel.send(p)


"""  
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
"""

# run the bot
bot.run(token)
