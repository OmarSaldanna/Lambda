# import the memory files handlers
from modules import *

# this just imports a needed function
from controllers.userlist import get_userlist

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
		post_users("free", [user_id], new_user=True)
		# once created the memory, return the new data
		return new_data.dic


def update_user_data(user_id: str, update: dict, userlist_update=False):
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
		# also append the new user to the userslist as a free user
		# only if the update doesnt become from userlist functions
		if not userlist_update:
			post_users("free", [user_id], new_user=True)
		# once created the memory, return the new data
		return 'ok'

##########################################################################################

# post users in the userlist, also allows to create roles in
# userlist, but there must be an usage for those new roles.
# new param is to specify if the used is new, or moved to 
# other role, it's true when it is called by member controller
def post_users(role: str, users: list, new_user=False):
	# to prevent duplicated users
	users = list(set(users))
	# get the userlist
	userlist = get_userlist()
	# and the usages
	usages = Memory(os.environ["USAGES_PATH"])
	# check that the role exist in usages
	if role not in usages.dic.keys():
		# then it will be free by default
		role = "free"
	# then for each user
	for user in users:
		# first remove the user from its old role
		# only if the new_user its false
		if not new_user:
			# iterate all the userlist roles
			for r in userlist.keys():
				# see if the user is in these users
				try:
					# this souldnt throw error if the user is in this role
					_ = userlist[r][user]
					# then delete it
					del(userlist[r][user])
					# and end
					break
				except:
					continue
		# then add the user to the userlist
		try:
			# add it to the userlist in the respective role
			userlist[role][user] = int(os.environ["PERIOD"])
		# the role isnt in userlist, but it's in usages
		except:
			# create a new section for the role
			userlist[role] = {}
			# and add the user
			userlist[role][user] = int(os.environ["PERIOD"])
		# also set the user usage to the role usage 
		update_user_data(user, {"usage":usages[role], "role": role}, userlist_update=True)
	# finally write the memory
	mem = get_memory('userlist/userlist') # it sure exists
	mem.dic = userlist
	mem.write()
	# leave a log
	app_to_log('userlist', f"[POST] moved {','.join(users)} to new {role}")
	# and return a message
	return f'moved to role new "{role}"'