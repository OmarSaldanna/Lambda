# db controllers are called by the app to serve the data
from modules import *

#############################################################################################
################################### Member Functions ########################################
#############################################################################################

def get_user_data(user_id: str, server: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id("members", user_id)
		# check the servers
		if server not in mem['servers']:
			# add the server
			mem['servers'] += [server]
			# and write
			mem.write()
		# return the memory fle data
		return mem.dic
	# the user has no file
	except:
		# then create one
		new_data = make_memory(user_id, "members")
		# check the servers
		if server not in new_data['servers']:
			# add the server
			new_data['servers'] += [server]
			# and write
			new_data.write()
		# also append the new user to the userslist as a free user
		post_users("free", [user_id])
		# once created the memory, return the new data
		return new_data.dic


def update_user_data(user_id: str, update: dict):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory(f'members/{user_id}')
		# make the update changes
		mem.update(update)
		# return a message
		return 'ok'
	# the user has no file
	except:
		# then create one and get the mem instance
		mem = make_memory(user_id, "members")
		# make the update changes
		mem.update(update) 
		# once created the memory, return the new data
		return 'ok'

#############################################################################################
################################### Server Functions ########################################
#############################################################################################

def get_server_data(server_id: str, server_name: str):
	# try to open the server file
	try:
		# open the memory file
		mem = get_memory_by_id('servers', server_id)
		# return the memory fle data
		return mem.dic
	# the server has no file
	except:
		# then create one
		new_data = make_memory(server_id, 'servers')
		# set the name, as an update
		new_data.update({"name": server_name})
		# once created the memory, return the new data
		return new_data.dic


def update_server_data(server_id: str, update: dict):
	# try to open the server file
	try:
		# open the memory file
		mem = get_memory(f'servers/{server_id}')
		# make the update changes
		mem.update(update)
		# return a message
		return 'ok'
	# the user has no file
	except:
		# then create one
		mem = make_memory(server_id, 'servers')
		# make the update changes
		mem.update(update)
		# once created the memory, return the new data
		return 'ok'

#############################################################################################
################################### Server Functions ########################################
#############################################################################################

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

#############################################################################################
#################################### Verbs Functions ########################################
#############################################################################################

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
	for verb in list_file_names("db/data/verbs"):
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
	for verb in list_file_names("db/data/verbs"):
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

#############################################################################################
#################################### Errors Functions #######################################
#############################################################################################

def add_to_log(database: str, data: str):
	# app to log
	app_to_log(database, data)
	# send a message
	return 'ok'


# function to generate hashes, it must not be used to security operations
def generate_hash(data: str):
	# generate a numerical hash with python
    # convert it to hexadecimal
    return hex(hash(data) & 0xFFFFFFFFFFFFFFFF)[2:].zfill(16)

#	"data": {
#		"call": lambda call that generated the error
# 		"code": error code
# 		"member": user id
# 		"server": server id
# 	}
#controllers.add_to_errors(database, data)
def add_to_errors(data: dict):
	# hash the error code
	error_hash = generate_hash(data['code'])
	# try to open the error file
	try:
		# open the memory file
		mem = get_memory(f'errors/{error_hash}')
		# in this case, append the data
		for key in ['call', 'member', 'server']:
			if data[key] not in mem[key + 's']:
				mem[key + 's'].append(data[key])
		#mem['servers'].append(data['server'])
		#mem['members'].append(data['member'])
		# sum to the counter
		mem['count'] += 1
		# and write the memory
		mem.write()
		# return a message
		return 'ok', error_hash
	# the user has no file
	except:
		# then create one based on the prototype
		mem = make_memory(error_hash, 'errors')
		# assign the data
		mem['calls'] = [data['call']]
		mem['servers'] = [data['server']]
		mem['members'] = [data['member']]
		mem['code'] = data['code']
		# and write changes
		mem.write()
		# once created the memory, return the new data
		return 'ok', error_hash

#############################################################################################
#################################### Userlist Functions #####################################
#############################################################################################

# return the user list 
def get_userlist():
	try:
		# get the userlist
		mem = get_memory('userlist/userlist')
		# return the data
		return mem.dic
	except:
		raise MemoryError("userlist/userlist.json file not found or error")

# discounts -1 to the users' days left
# returns an userlist of the users to restore
def put_userlist():
	# get the userlist
	mem = get_memory('userlist/userlist')
	# start the userlist dic
	userlist = {}
	# then for each role
	for role in mem.dic.keys():
		# instance the role
		userlist[role] = []
		# for each user
		for user in mem[role].keys():
			# if user has a counter of -1
			if mem[role][user] <= 0:
				# then restore to 30
				mem[role][user] = 30
				# and add the user to the restore userlist
				userlist[role].append(user)
			# else, there are still days left
			else:
				# then discount
				mem[role][user] -= 1
	# finally write the memory
	mem.write()
	# and leave a log
	add_to_log('userlist', '[PUT] days left discounted')
	# and return
	return userlist

# post users in the userlist, also allows to create roles in
# userlist, but there must be an usage for those new roles
def post_users(role: str, users: list):
	# to prevent duplicated users
	users = list(set(users))
	# get the roles
	mem = get_memory('userlist/userlist')
	# and the usages
	usages = get_memory("../usages")
	# if the role does not exist, then cerate it
	if role not in mem.dic.keys():
		# verify that there is an usage for the role
		if role not in usages.dic.keys():
			return f"Error: no usage for role '{role}'"
		# then there is an usage for the new role
		# cerate the new role in userlist with the users
		mem[role] = {}
		# now add each user to the role
		for user in users:
			# append the user with its 30 days left
			mem[role][user] = 30
			# also set the user usage to the role usage 
			update_user_data(user, "members", {"usage":usages[role]})
			# remove the user from the past role
			# check in each role
			for i_role in mem.dic.keys():
				# skip the destination role
				if role == i_role:
					continue
				# then check if the user in the role
				try:
					# if the user exists, this shouldn't throw error
					_ = mem[i_role][user]
					# then remove the user from that role
					del(mem[i_role][user])
					# break and add the user to the new role
					break
				except:
					continue
		# finally write the memory
		mem.write()
		# and leave a log
		add_to_log('userlist', f"[POST] moved {','.join(users)} to new {role}")
		# and return
		return f'moved to role new "{role}"'
	#######################################################################
	# in case that the role exist in userlist
	# for each user
	for user in users:
		# first check if the user is not in the selected role
		try:
			# if the user exists, this shouldn't throw error
			_ = mem[role][user]
			# in that case skip, it was a typo
			continue
		except:
			pass
		# then, the user is in another role
		# check in each role
		for i_role in mem.dic.keys():
			# skip the destination role
			if role == i_role:
				continue
			# then check if the user in the role
			try:
				# if the user exists, this shouldn't throw error
				_ = mem[i_role][user]
				# then remove the user from that role
				del(mem[i_role][user])
				# break and add the user to the new role
				break
			except:
				continue
		# then add the user to the role
		# equals 30, of 30 days left
		mem[role][user] = 30
		# get the role usage
		role_usage = usages[role]
		# set that usage into the usage of the user
		update_user_data(user, "members", {"usage":role_usage})
	# finally write the memory
	mem.write()
	# and leave a log
	add_to_log('userlist', f"[POST] moved {','.join(users)} to {role}")
	# and return
	return f'moved to role "{role}"'


# function to restore the user's usage once their days left have ended
def patch_users(userlist: dict):
	# load the usages
	usages = get_memory("../usages")
	# for each role in the userlist
	for role in userlist.keys():
		# for each user in the role
		for user in userlist[role]:
			# set that usage into the usage of the user
			update_user_data(user, "members", {"usage":usages[role]})
	# finally save a log
	add_to_log('userlist', f"[PATCH] restored users usage")
	# and return
	return 'ok'

#############################################################################################
#################################### Extra Functions ########################################
#############################################################################################

# controller to send alerts to telegram
def telegram_alert(content: str):
	# send the alert
	telegram_message(content)
	# save a log
	add_to_log('errors', f"[DB] {content}")
	# and return
	return 'ok'

# controller to list files in directories
# used mainly for json files
def list_file_names (folder: str, removed_letters=5):
	return [f[:-5] for f in os.listdir(folder)]