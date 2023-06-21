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
		# number of images generated
		if n == 1:
			# return one url
			return [response['data'][0]['url']]
		else:
			# return all urls
			urls = []
			for i in range(n):
				urls.append(response['data'][i]['url'])
			return urls