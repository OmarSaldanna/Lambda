# Lambda AI



incoming messages:


data* , prompt: { content parsed as lambda db }


read of large documents will be implemented after SDB is ready


###################################################################
	########################## CONTEXT RULES ##########################
	###################################################################

	# if mode != db.mode then clear context and only keep last 3 messages:
	# system, user, and last answer.
	# if context len (counted after each answer) > limit then clear and
	# keep last 3 messages 