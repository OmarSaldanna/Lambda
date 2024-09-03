# https://docs.anthropic.com/en/api/messages
import anthropic

# instance the API, the key is in the env
client = anthropic.Anthropic()


# function to parse the current context to Claude mode
def parse_context (context: list):
	parsed_context = []
	system = ""
	# iterate every block of lambda context
	for i, item in enumerate(context):
		######## System Message ###############################################

		# the first row is the system one, then:
		if i == 0:
			system = item['text']
			continue

		######## Assistant Messages ############################################
		
		# else are common messages
		_type, _content = list(item.items())[0]
		role = ""
		# by default its a text
		content = [{ "type": "text", "text": _content }]
		
		# even i messages are from assistant
		if i%2 == 0:
			# then they're answers
			role = "assistant"
		
		######## User Messages #########################################
		
		# and odds are prompts from the user
		else:
			role = "user"
			# first let's se if they're images
			if _type == "image":
				# first image block and after the text block
				content = [{
					"type": "image",
					"source": {
							"type": "base64",
							"media_type": "image/png",
							"data": _content[0]
					}},
				{ "type": "text","text": _content[1] }]
		
		#################################################################
		
		# finally append the block to the context
		parsed_context.append({
			"role": role,
			"content": content
		})
	# return the context and the system
	return parsed_context, system


# function to count tokens token counter, returns the amont of USDs
# that the prompt has taken. receives the response object and also
# the prices from the input and output tokens. Loaded on ai.py file.
# https://www.anthropic.com/pricing#anthropic-api
def discounter (response, prices: list):
	total_cost = 0;
	# calculate the price for input tokens
	total_cost += response.usage.input_tokens * prices [0] * 1/1e6
	# also for output tokens
	total_cost += response.usage.output_tokens * prices [1] * 1/1e6
	# and return the cost and the total tokens
	total_tokens = response.usage.input_tokens + response.usage.input_tokens
	return total_cost, total_tokens, response.content[0].text


# context will receive the Lambda context (general)
def chat (context: list, model: str, temp: int, stream: bool, max_tokens: int):
	# parse the context and in this case extract the system block
	claude_context, system_block = parse_context(context)
	# use the api
	return client.messages.create(
		# with the selected mode
		model=model,
		# the token limit
		max_tokens=max_tokens,
		# also the temp
		temperature=temp,
		# and the 
		system=system_block,
		messages=claude_context
	)