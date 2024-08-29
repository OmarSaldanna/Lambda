# This file provides an standarized class of a model, with
# methods: chat, research, intelligence and vision. And only
# imports simple functions from models: Gemini, GPT and claude.
# Also has a counter mechanism that calculates how many USDs
# has a prompt cost.

# in the models there are only thwo simple functions: chat and vision
# it only calls the  IA api and returns an answer. Also each api has its
# own manage functions: discounter: that returns how many dollars do
# the requests cost based on pricing, model and current costs

import os
import json
# the db handler
from modules.db import DB
from modules.cloudinary import Cloudinary
from modules.context import remake_context
# from modules.context import 


class AI:

	# this class is instanced in every skill
	def __init__ (self, user_id: str):
		# instance the db
		self.db = DB()
		# the user id
		self.user_id = user_id
		# first load the user data
		self.user_data = self.db.get('/members', {
			"id": self.user_id,
			"db": "members",
			"server": server
		})['answer']
		# also load the models info
		with open(os.environ["MODELS_FILE"], "r") as f:
			self.models_info = json.load(f)

	def __call__ (self, prompt: dict, mode="chat"):

		########################## CONTEXT RULES ##########################
		# clear context (auto and not manually): only keep 3 messages:
		# first system message, last prompt, last answer
		# 1.- if mode != db.mode then clear context. Applied before response
		# 2.- if context len (counted after each answer) > limit. Applied after response

		# first rule then

		# check the modes to apply context mode rules

		# append to context
		# import the correct model functions from models
		# parse the context
		
		# use the model
		# get the prompt cost and make the discount
		# append the answer to context and verify limits
		# return the answer

	###################################################################
	
	###################################################################

