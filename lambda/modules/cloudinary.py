import os
# cloduinary utils
import cloudinary
import cloudinary.uploader
# and the db handler
from modules.db import DB


# cloudinary module
class Cloudinary:
	"""
	This is a module that uses cloudinary to upload
	files into cloudinary
	"""
	def __init__ (self, user_id):
		# get the cloudinary credentials
		# returns "https" URLs by setting secure=True  
		config = cloudinary.config(
			secure=True,
			cloud_name=os.environ["cloud_name"],
			api_key=os.environ["api_key"],
			api_secret=os.environ["api_secret"]
		)
		# instance a db to use it
		self.db = DB()
		# and the user id
		self.user_id = user_id

	# upload files
	def upload (self, img_path: str):
		# upload the image
		ans = cloudinary.uploader.upload(img_path)
		# if it worked, regist on log
		self.db.post("/logs", {
			"db": "clodinary",
			"data": f"[{self.user_id}] uploaded file {img_path} to {ans['secure_url']}"
		})
		return ans['secure_url']
