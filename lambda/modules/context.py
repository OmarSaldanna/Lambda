# here are basic functions to handle the context

# function to clear context: only keep 3 messages:
# first system message, last prompt, last answer
def remake_context (context: lsit):
	# create the Lambda context structure
	new_context = []
	# append the initial message
	new_context.append(context[0])
	# also the last two messages
	new_context.append(context[-2])
	new_context.append(context[-1])
	# and return
	return new_context