# https://docs.anthropic.com/en/api/messages

import anthropic

client = anthropic.Anthropic()



def parse_context (context: dict):
	parsed_context = []
	# the first row must be a system one, then:
	for i, item in enumerate(context):
		# 

def discounter (response, prices: list)

def chat (context: list, model: str, response_format="text", temp=1, stream=False, max_tokens=1024):
	o
	# use the api
	return client.messages.create(
		model=model,
		max_tokens=max_tokens,
		temperature=temp,
		system=context[0],
		messages=[]
	)