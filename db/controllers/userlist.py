# import the memory files handlers
from modules import *

# import the update user data function from member controller
# from controllers.member import update_user_data
# this gave an error "most likely due to a circular import"

# return the user list 
def get_userlist():
	try:
		# get the userlist
		mem = get_memory('userlist/userlist')
		# return the data
		return mem.dic
	except:
		# if there isnt a file, then just create it
		create_memory("userlist/userlist.json", {})
		# and return an empty dict
		return {}

# discounts -1 to the users' days left
# returns an userlist of the users to restore
def put_userlist():
	# get the userlist
	mem = get_userlist()
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
				mem[role][user] = os.environ["PERIOD"]
				# and add the user to the restore userlist
				userlist[role].append(user)
			# else, there are still days left
			else:
				# then discount
				mem[role][user] -= 1
	# finally write the memory
	mem.write()
	# and leave a log
	app_to_log('userlist', '[PUT] days left discounted')
	# and return
	return userlist


# post users was move to member

# function to restore the user's usage once their days left have ended
def patch_users(userlist: dict):
	# load the usages
	usages = Memory(os.environ["USAGES_PATH"])
	# for each role in the userlist
	for role in userlist.keys():
		# for each user in the role
		for user in userlist[role]:
			# set that usage into the usage of the user
			update_user_data(user, {"usage":usages[role], "role": role})
	# finally save a log
	app_to_log('userlist', f"[PATCH] restored users usage")
	# and return
	return 'ok'


# SPECIAL NOTE: put counts the days and returns the users to be recharged
# and their roles, patch updates the usages from those users to be recharged