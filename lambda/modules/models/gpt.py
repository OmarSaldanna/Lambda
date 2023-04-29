import openai

class GPT:
  def __init__(self, token):
    # set the token
    openai.api_key = token
    
  # new usage. gpt-3.5-turbo is as cheap as curie and better
  def __call__ (self, prompt):
    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return res['choices'][0]['message']['content']