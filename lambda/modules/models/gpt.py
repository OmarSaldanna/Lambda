import openai

class GPT:
  def __init__(self, token):
    # set the token
    openai.api_key = token
  
  """
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
  """

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
