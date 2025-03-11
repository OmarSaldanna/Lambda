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
	def __call__ (self, prompt: dict, mode="chat", max_tokens=1024):

		########################## CONTEXT RULES ############################
		# 1.- if mode != db.mode then clear context. Applied before response
		# 2.- if context len (counted after each answer) > limit. Applied
		# after response clear context (auto and not manually): only keep
		# 3 messages: first system message, last prompt, last answer

		# # first rule then
		# if mode != self.user_data['mode']:
		# 	# if so, clear the context, only if the context is longer than
		# 	# only one message
		# 	if len(self.user_data["context"]) > 1:
		# 		# clear context
		# 		self.user_data["context"] = clear_context(self.user_data["context"])

		# append prompt to context
		self.user_data["context"].append(prompt)
		# select the model
		model = self.user_data["models"][mode]
		# get the module name
		module_name = model.split('-')[0]
		
		########################## Availability Check #######################

		# if the prompt cost is higher than the remaining credits + (avg answer len price)
		# then return a message that the user has no remaining budget to chat
		# input price
		est_cost = self.user_data["context_size"] * 1/1e6 * self.models_info["models"][model][0]
		# average output price
		est_cost += int(os.environ["AVG_ANSWER_LEN"]) * 1/1e6 * self.models_info["models"][model][1]
		# then the if the estimated cost is higher than available funds
		if est_cost > self.user_data["usage"]["budget"]:
			# send an error message
			return {
				"type": "error",
				"content": os.environ["NO_FUNDS_ERROR"]
			}

		#####################################################################

		# import the correct model functions based on mode model
		llm = importlib.import_module(f"models.{module_name}")
		# use the model and pass the params
		response = llm.chat(self.user_data["context"], model, max_tokens)
		# get the prompt cost and make the discount
		promt_cost, context_size, response_text, tokens = llm.discounter(
			response, self.models_info["models"][model]
		)

		# make the discount to the user budget
		self.user_data["usage"]["budget"] -= promt_cost
		# append the answer to context
		self.user_data["context"].append({ "text": response_text })
		
		################# check context rule 2 #############################
		if context_size >= self.models_info["limits"][mode]:
			# then clear context
			self.user_data["context"] = clear_context(self.user_data["context"])
		################################## #################################
		
		# save the log of the tokens
		self.db.post("/logs", {
			"db": "tokens",
			"data": f"[{self.user_id}] {model} in: {tokens[0]} out: {tokens[1]}"
		})
		# save changes on db
		self.db.put('/members', {
			"id": self.user_id,
			"data": {
				# update the context
				"context": self.user_data["context"],
				# also context size
				"context_size": context_size,
				# the usage discount
				"usage": self.user_data["usage"],
				# and the current mode
				"mode": mode
			}
		})

		# return the answer
		return {
			"type": "text",
			"content": response_text
		}