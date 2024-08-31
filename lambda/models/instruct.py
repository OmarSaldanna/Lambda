# THIS IS A SPECIAL MODULE CREATED TO ONLY JSON ANSWERS
# ITS THE SAME AS GPT MODULE, JUST JSON ANSWERS

# Also read: https://platform.openai.com/docs/guides/structured-outputs/introduction?context=ex2
from openai import OpenAI

# instance the API, the key is in the env
client = OpenAI()


# function to parse the current context to GPT mode
def parse_context (context: list): 
  parsed_context = []
  # the first row must be a system one, then:
  for i, item in enumerate(context):
    # extract the info
    _type, _content = list(item.items())[0]
    # basic presets
    role = ""
    content = [{
      "type": "text",
      "content": _content
    }]

    ######## System Message ###############################################

    # the first message starts with role: system
    if i == 0:
      role = "system"

    ######## Assistant Messages ############################################

    # for even i, it is an assitant message
    elif i%2 == 0:
      role = "assistant"

    ######## User Messages #########################################

    # else is an user message, it can also contain images
    else:
      role = "user"
      # in case of image
      if _type == "image":
        # then item _content is a list: image url and message
        content = [
          { "type": "image_url", "image_url": {"url": f"data:image/png;base64,{_content[0]}"} },
          { "type": "text", "content": _content[1] }
        ]
      # else it is a text, but the same content format as before the ifs
    
    #################################################################
    
    # finally append each message to the context
    parsed_context.append({
      "role": role, 
      "content": content
    })
  # and return
  return parsed_context


# function to count tokens token counter, returns the amont of USDs
# that the prompt has taken. receives the response object and also
# the prices from the input and output tokens. Loaded on ai.py file.
# https://platform.openai.com/docs/api-reference/chat/object
def discounter (response, prices: list):
  total_cost = 0;
  # calculate the price for input tokens
  total_cost += response.usage["prompt_tokens"] * prices [0]
  # also for output tokens
  total_cost += response.usage["completion_tokens"] * prices [1]
  # and return the cost and the total tokens
  return total_cost, response.usage["total_tokens"]


# function to use multimodal LLMs
def chat (context: list, model: str, temp: int, stream: bool, max_tokens: int):
  # use the API
  return client.chat.completions.create(
    # select the model
    model=model,
    # the context structure
    messages=context,
    # temperature
    temperature=1,
    # the output format
    response_format={ "type": "json_object" },
    # max tokens output
    max_tokens=max_tokens
  )