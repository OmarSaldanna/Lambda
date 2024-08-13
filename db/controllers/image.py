# import the memory files handlers
from modules import *


def post_image (image_hash: str, image_url: str, image_prompt: str):
	# open a new memory file named by the hash
	create_memory(
		f"images/{image_hash}.json",
		{
			"url": image_url,
			"prompt": image_prompt,
			"date": get_time()
		}
	)
	return 'ok'