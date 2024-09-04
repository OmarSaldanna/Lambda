# https://ai.google.dev/gemini-api/docs/text-generation?lang=python
import google.generativeai as genai
import os # to load the gemini api key

# things to load the image
import io
import base64
from PIL import Image

# set the api key manually
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


# special function to load images, special case for gemini api
# receives the image encoded to base64
def load_image (b64):
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(image_b64)
    # Create a BytesIO object from the decoded bytes
    image_stream = io.BytesIO(image_bytes)
    # Open the image from the BytesIO stream using PIL
    return Image.open(image_stream)


# function to parse the current context to Gemini mode
# note: ONLY ACCEPTS THE LAST IMAGE IN CASE OF BEEING
# A NEW PROMT. PAST PROMTS IMAGES ARE SKIPPED
def parse_context (context: list):
    parsed_context = []
    prompt = ""
    image = None # by default
    # the first row must be a system one, then:
    for i, item in enumerate(context):
        # extract the info
        _type, _content = list(item.items())[0]
        # basic presets
        role = ""
        content = ""

        ######## System Message ###############################################

        # gemini has no system message
        if i == 0:
            # then just skip it
            continue

        ######## Assistant Messages ############################################
        
        # for even i, it is an assitant message
        elif i%2 == 0:
            role = "model"
            content = _content

        ######## User Messages #########################################

        # else is an user message, it can also contain images
        else:
            role = "user"
            # if its the final message:
            if i == len(context)-1:

                # if the content is a list: then IS AN IMAGE
                if isinstance(_content, list):
                    # load the image
                    image = load_image(_content[0])
                    # save the prompt
                    prompt = _content[1]
                    # and break

                # else: is just a message
                else:                
                    # so, save the prompt
                    prompt = _content
                    # and break
                    break

            # it just a normal message: images are going to be skipped
            else:

                # if the content is a list: then IS AN IMAGE
                if isinstance(_content, list):
                    # just save the text
                    content = _content[1]
                # else save the content
                else:
                    content = _content
        
        #################################################################

        parsed_context.append({
            "role": role,
            "parts": content
        })

    return parsed_context, prompt, image


# function to count tokens token counter, returns the amont of USDs
# that the prompt has taken. receives the response object and also
# the prices from the input and output tokens. Loaded on ai.py file.
# https://ai.google.dev/gemini-api/docs/tokens?lang=python#multi-turn-tokens
def discounter (response, prices: list):
    total_cost = 0;
    # calculate the price for input tokens
    total_cost += response.usage_metadata.prompt_token_count * prices [0] * 1/1e6
    # also for output tokens
    total_cost += response.usage_metadata.candidates_token_count * prices [1] * 1/1e6
    # and return the cost and the total tokens
    return total_cost, response.usage_metadata.total_token_count, response.text, (response.usage_metadata.prompt_token_count, response.usage_metadata.candidates_token_count)


# general function to use gemini
def chat (context: list, model: str, temp: int, stream: bool, max_tokens: int):
    # get the past context and the prompt, due to gemini rules
    past_context, prompt, image = parse_context(context)
    print(past_context, prompt, image)
    # load the model
    model = genai.GenerativeModel(model)
    # set the context
    chat = model.start_chat(
        # load the context
        history=past_context
    )
    # use the chat and set the case when an image comes
    return chat.send_message(prompt) if not image else chat.send_message([prompt, image])