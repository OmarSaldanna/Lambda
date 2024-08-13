# import the memory files handlers
from modules import *


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