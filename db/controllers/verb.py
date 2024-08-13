# import the memory files handlers
from modules import *


def get_verb_data(verb: str):
	# try to get the verb
	try:
		# get the verb data
		mem = get_memory(f'verbs/{verb}')
		# and return
		return mem.dic
	# the verb wasn't found
	except:
		return '404'


# writes or overwrites verb data based on the create or elimination
# elimination of lambda skills
def post_verb_data(skill: str, words: list, verbs: list, newverb_lock=False):
	# missing verbs
	missing = []
	# create the update dic
	update = {}
	for word in words:
		update[word] = skill
	# try open each verb memory
	for verb in verbs:
		try:
			mem = get_memory(f'verbs/{verb}')
			# then run the update
			mem.update(update)
		# if the verb isnt found, then append it to missing
		except:
			missing.append(verb)
			# if the new verb lock isn't active
			if newverb_lock:
				# first add the function type to the update
				update['type'] = "multi"
				# now create the memory
				create_memory(f"verbs/{verb}.json", update)
	# finally return the missing
	return missing


# removes all the information related to a lambda skill
def delete_verb_data(skill: str):
	# list of altered verbs
	altered = []
	# list all the verbs
	for verb in list_file_names(memory_path + "verbs"):
		# open the memory file
		mem = get_memory(f'verbs/{verb}')
		# check if the skill is in the verb
		if skill in mem.dic.values():
			# rows to remove
			to_remove = []
			# then iterate the dic items
			print(verb)
			for key, val in mem.dic.items():
				# when appears the skill
				if val == skill:
					# append the key to then remove
					to_remove.append(key)
			# remove all saved the rows
			for key in to_remove:
				del(mem.dic[key])
			# finally write the memory, once removed the words
			mem.write()
			# also append the verb to altered
			altered.append(verb)
	# and finally return the altered verbs
	return altered


def patch_verb_data(search: str, value: str):
	# list
	result = [] if search != "skill" else {}
	# list all the verbs
	for verb in list_file_names(memory_path + "verbs"):
		# open the memory file
		mem = get_memory(f'verbs/{verb}')
		################# search: word #######################
		if search == "word":
			if value in mem.dic.keys():
				result.append(verb)
		################# search: function #######################
		if search == "function":
			if value in mem.dic.values():
				result.append(verb)
		################# search: skill #######################
		if search == "skill":
			# then create a dict like a tree
			if value in mem.dic.values():
				# start creating a list
				result[verb] = []
				# iter the dic
				for key, val in mem.dic.items():
					# when appears the skill
					if val == value:
						# append the key to the created list
						result[verb].append(key)
	# finaly return
	return result