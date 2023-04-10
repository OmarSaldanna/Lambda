import openai

class GPT3:
  def __init__(self, token):
    # set the token
    openai.api_key = token
  
  def __call__(self, text):
    # use gpt-3
    response = openai.Completion.create(
      model="text-curie-001",
      prompt=text,
      temperature=0.5,
      max_tokens=2000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
    )
    return response['choices'][0]['text'].strip()
