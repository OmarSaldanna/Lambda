# db controllers are called by the app to serve the data
from modules import *

#controllers.get_user_data(author_id, database)
def get_user_data(user_id: str, database: str, server: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id(database, user_id)
		# check the servers in case of db=members
		if database == "members":
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
		new_data = make_memory(user_id, database)
		# check the servers in case of db=members
		if database == "members":
			if server not in new_data['servers']:
				# add the server
				new_data['servers'] += [server]
				# and write
				new_data.write()
		# also append the new user to the userslist as a free user
		post_users("free", [user_id])
		# once created the memory, return the new data
		return new_data.dic


#controllers.update_user_data(author_id, database, update)
def update_user_data(user_id: str, database: str, update: dict):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory(f'{database}/{user_id}')
		# make the update changes
		mem.update(update)
		# return a message
		return 'ok'
	# the user has no file
	except:
		# then create one and get the mem instance
		mem = make_memory(user_id, database)
		# make the update changes
		mem.update(update) 
		# once created the memory, return the new data
		return 'ok'


#controllers.get_server_data(server_id)
def get_server_data(server_id: str):
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
		# once created the memory, return the new data
		return new_data.dic


#controllers.update_server_data(server_id, update)
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


#controllers.get_verb_data(verb)
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


#controllers.add_verb_data(verb, data)
def add_verb_data(verb: str, data: dict):
	# try to open the verb file, to check if
	# it already extsis
	try:
		# get the verb data, this line should
		# raise an error if the verb does not exist
		mem = get_memory(f'verbs/{verb}')
		# then return the verb
		return mem.dic
	# the verb does not exist, then create the file
	except:
		# create the json file with the str
		create_memory(f'verbs/{verb}.json', data)
		return 'ok'


#controllers.update_verb_data(verb, data)
def update_verb_data(verb: str, update: dict):
	# try to get the verb
	try:
		# get the verb data
		mem = get_memory(f'verbs/{verb}')
		# make the update
		mem.update(update)
		# and return
		return 'ok'
	# the verb wasn't found
	except:
		return '404'


#controllers.add_to_log(database, data)
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


# return the user list 
def get_userlist():
	try:
		# get the userlist
		mem = get_memory('[PUT] userlist/userlist')
		# return the data
		return mem.dic
	except:
		raise MemoryError("userlist/userlist.json file not found or error")

# discounts -1 to the users' days left
def put_userlist():
	# get the userlist
	mem = get_memory('userlist/userlist')
	# then for each role
	for role in mem.dic.keys():
		# for each user
		for user in mem[role].keys():
			# discount
			mem[role][user] -= 1
	# finally write the memory
	mem.write()
	# and leave a log
	add_to_log('userlist', 'days left discounted')
	# and return
	return mem.dic

# post users in the userlist
def post_users(role: str, users: list):
	users = list(set(users))
	# get the roles
	mem = get_memory('userlist/userlist')
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
		role_usage = get_memory("../usages")[role]
		# set that usage into the usage of the user
		update_user_data(user, "members", {"usage":role_usage})
	# finally write the memory
	mem.write()
	# and leave a log
	add_to_log('userlist', f"[POST] moved {','.join(users)} to {role}")
	# and return
	return 'ok'