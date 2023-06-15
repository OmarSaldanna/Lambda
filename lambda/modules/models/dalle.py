import openai

class DALLE:
  def __init__(self, token:str):
    # set the token
    openai.api_key = token
    
  # use DALL-E to generate custom images
  def __call__ (self, prompt:str, n=1):
    response = openai.Image.create(
      prompt=prompt,
      n=n,
      size="1024x1024"
    )
    if n == 1:
      # return one url
      return [response['data'][0]['url']]
    else:
      # return all urls
      urls = []
      for i in range(n):
        urls.append(response['data'][i]['url'])