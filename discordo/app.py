import discord
from modules import controllers
from discord.ext import commands
from modules.memory import *


# load the token
info = get_memory('info')
# requirements to run discord app
token = info['DISCORDO']
# vip list: close friends that are allowed to use Lambda
# admin: me, for lambda-cli, members and other functions
admin = info['ADMIN']
vips = info['VIPS']

# define the intents
intents = discord.Intents.all()
intents.members = True
# instance the discord app
bot = commands.Bot(command_prefix='-', intents=intents)



# when the bot starts running
@bot.event
async def on_ready():
    print('[DISCORDO] -> Lambda -> im alive')
    # send a message to the channel that lambda is alive


# when a message came
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Admin level
    # lambda cli #
    # add members: add, see, del #
    # lambdrive files: ls, rm, mv #
    if str(message.author) == admin:
        # amdmin try: this is an attempt to stop errors caused by syntax
        try:
############# lambda cli
            if message.content[0] == '$':
                # this is for the log
                app_to_log(f'[DISCORD] -> Admin on lambda-cli -> {message.content[2:]}\n')
                pieces = controllers.lambda_cli(message) # use the lambda_cli controller
                for p in pieces: # send the message or messages
                    await message.channel.send(p)

############# the admin manual
            elif message.content == 'aman':
                app_to_log(f'[DISCORD] -> {message.author} admin manual\n')
                # get the message by pieces
                pieces = controllers.get_admin_manual()
                # send the pieces
                for p in pieces:
                    await message.channel.send(p)

############# member admin
            elif message.content[:7] == 'member ':

                # add user
                if message.content[7:10] == 'add':
                    # use the controller
                    msg, log = controllers.add_member(message, vips, info)
                    # make the log
                    app_to_log(log)
                    # and send the message
                    await message.channel.send(msg)

                # see users
                elif message.content[7:] == 'see':
                    # make the log
                    app_to_log(f'[DISCORD] -> Admin on members -> seen members\n')
                    # and send the result
                    await message.channel.send("**Lista de VIPs**")
                    # show all the vip users
                    for user in vips:
                        await message.channel.send(f"> {user}")
                
                # delete user
                elif message.content[7:10] == 'del':
                    # use the controller
                    msg, log = controllers.delete_member(message, vips, info)
                    # make the log
                    app_to_log(log)
                    # and send the message
                    await message.channel.send(msg)

                # command not understood                
                else:
                    app_to_log(f'[DISCORD] -> Admin on members -> bad command\n')
                    await message.channel.send("> Escribe bien wey [add|see|del]")
            
############# echo funcion
            elif message.content[:5] == 'echo ':
                await message.channel.send(f"```{message.content[5:]}```")


############# lambdrive files
            elif message.content[:10] == 'lambdrive ':
                # get the command
                command = message.content[10:12]
                # excecute the command
                pieces = controllers.lambdrive_cli(message, command)
                # app to log
                app_to_log(f'[DISCORD] -> Admin on lambdrive -> {message.content[10:]}\n')
                # send the message
                for p in pieces:
                    await message.channel.send(p)


############# End of Admin functions
        except:
            app_to_log(f'[DISCORD] -> Admin command -> error\n')
            await message.channel.send("> Error comando no válido\n> Puedes consultar el manual con _aman_")



    # VIP Level:
    # status #
    # chat gpt #
    # save stuff #
    # give stuff #
    # generate qr codes #
    # DALL-E images #
    if str(message.author) in vips:
        # vips try: this is an attempt to stop errors caused by syntax
        try:

############# status
            if message.content in ['tas', 'tas?', 'Tas?']:
                app_to_log(f'[DISCORD] -> {message.author} ping\n')
                # confirmation messgae
                await message.channel.send('> of cors')

############# to see the manual of available functions
            elif message.content in ['man', 'manual', 'Manual']:
                app_to_log(f'[DISCORD] -> {message.author} manual\n')
                # get the message by pieces
                pieces = controllers.get_manual()
                # send the pieces
                for p in pieces:
                    await message.channel.send(p)

############# gpt3 usage
            elif message.content[:7] in ['lambda ', 'Lambda ']:
                app_to_log(f'\n[DISCORD] -> {message.author} on chat gpt: {message.content}\n')
                # use the chat_gpt controller
                pieces = controllers.chat_gpt(message)
                # add to log the answer
                app_to_log(f"{''.join(pieces)}\n")
                # send the message or messages
                for p in pieces:
                    await message.channel.send(p)

############# save stuff
            elif message.content[:9] in ['sostenme ', 'Sostenme ']:
                app_to_log(f'\n[DISCORD] -> {message.author} saved stuff: {message.content[9:]}\n')
                # save the stuff
                controllers.save_stuff(message)
                # send the confirmation
                await message.channel.send(f"> Listo @{str(message.author)}")

############# return stuff
            elif message.content[:5] in ['dame', 'Dame']:
                app_to_log(f'\n[DISCORD] -> {message.author} read stuff\n')
                # read the stuff
                stuff = controllers.get_stuff(message)
                # send the confirmation
                await message.channel.send(f"> {stuff}")

############# QR generator
            elif message.content[:2] in ['QR', 'qr']:
                app_to_log(f'\n[DISCORD] -> {message.author} QR Generated with: "{message.content[3:]}"\n')
                # get the link of the image
                image_path = controllers.generate_qr(message)
                # send the image
                await message.channel.send(file=discord.File(image_path))

############# DALL-E images
            elif message.content[:5] in ['Dalle', 'dalle']:
                app_to_log(f'\n[DISCORD] -> {message.author} image generated with: "{message.content[3:]}"\n')
                # get the link of the image
                image_url = controllers.dalle(message)
                # send the image
                await message.channel.send(image_url)

        except:
            app_to_log(f'[DISCORD] -> Vip command -> error\n')
            await message.channel.send("> Error comando no válido\n> Puedes consultar el manual con _man_")


    # not registered users
    elif message.content[:6] in ['lambda', 'Lambda']:
        await message.channel.send(f"> Lo siento @{str(message.author)} no tienes acceso a mi")
        await message.channel.send(f"> Si lo deseas pídele a @{admin} que te de acceso")


# run the bot
bot.run(token)
