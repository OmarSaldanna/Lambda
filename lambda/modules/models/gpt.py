import openai

class GPT:
  def __init__(self, token:str):
    # set the token
    openai.api_key = token
    
  # new usage. gpt-3.5-turbo is as cheap as curie and better
  def __call__ (self, messages: list, temp=0.5, model="gpt-3.5-turbo"):
    res = openai.ChatCompletion.create(
      model=model,
      messages=messages,
            #[{"role": "system", "content": system},
            #{"role": "user", "content": prompt}]
      temperature=temp
    )
    return res['choices'][0]['message']['content']