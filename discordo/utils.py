# split a text in pieces of n length
def split_text(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]


# this was implemented cause of there's messages with len
# greater than 2K characters that discord don't acept. So
# send multiple messages if the msg is too large
# msg is the text, and message is the discord instance
async def send_message(msg, message):
	if len(msg) > 2000:
		# split the text in pieces
		pieces = split_text(msg, 2000)
		# send piece by piece
		for p in pieces:
			await message.channel.send(p)
	else:
		await message.channel.send(msg)

