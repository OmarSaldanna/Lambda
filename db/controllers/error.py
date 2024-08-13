# import the memory files handlers
from modules import *

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