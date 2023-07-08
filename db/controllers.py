# db controllers are called by the app to serve the data
from modules import *

# controllers.get_user_data(author_id, database)
def get_user_data(user_id: str, database: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id(database, user_id)
		# return the memory fle data
		return mem.dic

	# the user has no file
	except:
		# then create one
		new_data = make_memory(user_id, database)
		# once created the memory, return the new data
		return new_data


# controllers.update_user_data(author_id, database, update)
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
		print('update file not found')
		# then create one
		_ = make_memory(user_id, database)
		# open the memory file
		mem = get_memory(f'{database}/{user_id}')
		# make the update changes
		mem.update(update) 
		# once created the memory, return the new data
		return 'ok'