import openai

class DALLE:
  def __init__(self, token):
    # set the token
    openai.api_key = token
    
  # use DALL-E to generate custom images
  def __call__ (self, prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="1024x1024"
    )
    # get the image url
    image_url = response['data'][0]['url']
    # return the link
    return image_url
