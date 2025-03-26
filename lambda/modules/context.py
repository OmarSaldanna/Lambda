# here are basic functions to handle the context
# add skill: cambia de tema

import os
import tiktoken


# function to clear context: only keep 3 messages:
# first system message, last prompt, last answer
def clear_context (context: list):
	# create the Lambda context structure
	new_context = []
	# append the initial message
	new_context.append(context[0])
	# also the last two messages
	new_context.append(context[-2])
	new_context.append(context[-1])
	# and return 
	return new_context

# count tokens from string
def string_tokens (string: str):
	# instance the encoder with the set encoding
    encoding = tiktoken.get_encoding(os.environ["TOKENIZER_ENCODING"])
    # and return the num of tokens
    return len(encoding.encode(string))

# function to count tokens
def context_tokens (context: dict):
	# sum and count tokens from every message
	return sum([string_tokens(text) for t, text in context.item() if t == "text"])