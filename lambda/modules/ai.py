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
import importlib

# the db handler
from modules.db import DB
# and the context handling functions
from modules.context import clear_context


class AI:

	# this class is instanced in every skill
	def __init__ (self, user_id: str, server: str):
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


	# Main function, receibes a block of message in form of Lambda context
	def __call__ (self, prompt: dict, mode="chat", temp=1, stream=False, max_tokens=1024):

		########################## CONTEXT RULES ############################
		# 1.- if mode != db.mode then clear context. Applied before response
		# 2.- if context len (counted after each answer) > limit. Applied
		# after response clear context (auto and not manually): only keep
		# 3 messages: first system message, last prompt, last answer
		
		# logs
		# self.db.post("/logs", {
			# "db": "tokens",
			# "data": f"[{self.user_id}] {model} in: {tokens_in} out: {tokens_out} adjusted: {adjusted} total: {total_tokens}"
		# })

		# first rule then
		if mode != self.user_data['mode']:
			# if so, clear the context
			self.user_data["context"] = clear_context(self.user_data["context"])

		# append prompt to context
		self.user_data["context"].append(prompt)
		# import the correct model functions based on mode model
		model = self.user_data["models"][mode] # select the model
		module_name = model.split('-')[0] # get the module name
		llm = importlib.import_module(f"models.{module_name}")
		
		# use the model and pass the params
		response = llm.chat(self.user_data["context"], model, temp, stream, max_tokens)
		# get the prompt cost and make the discount
		promt_cost, context_size, response_text = llm.discounter(
			response, self.models_info["prices"][model]
		)

		# make the discount to the user budget
		self.user_data["usage"]["budget"] -= promt_cost
		# append the answer to context
		self.user_data["context"].append({ "text": response_text })
		# check context rule 2
		if context_size >= self.models_info["limits"][mode]:
			# then clear context
			self.user_data["context"] = clear_context(self.user_data["context"])
		
		# save changes on db
		self.db.put('/members', {
			"id": self.user_id,
			"data": {
				# update the context
				"context": self.user_data["context"],
				# the usage discount
				"usage": self.user_data["usage"],
				# and the current mode
				"mode": mode
			}
		})

		# return the answer
		return response_text