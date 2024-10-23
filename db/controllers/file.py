# import the memory files handlers
from modules import *


def get_user_files (user_id: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id("files", user_id)
		# return the memory file data
		return mem.dic
	# the user has no file
	except:
		# then create one
		new_data = make_memory(user_id, "files")
		# once created the memory, return the new data
		return new_data.dic


def post_user_file (user_id: str, filename: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id("files", user_id)
		# create the file object
		name = filename.split('/')[-1]
		path = filename
		# add the file to the dict
		mem[name] = path
		# write changes
		mem.write()
		# return the memory file data
		return mem.dic

	# the user has no file
	except:
		# then create one
		mem = make_memory(user_id, "files")
		# create the file object
		name = filename.split('/')[-1]
		path = filename
		# add the file to the dict
		mem[name] = path
		# write changes
		mem.write()
		# once created the memory, return the new data
		return mem.dic

def delete_user_file (user_id: str, filename: str):
	# try to open the user file
	try:
		# open the memory file
		mem = get_memory_by_id("files", user_id)
		# get the name
		name = filename.split('/')[-1]
		# try to remove file from the dict
		del(mem.dic[name])
		# write changes
		mem.write()
		# return the memory file data
		return mem.dic

	# the user has no file
	except:
		# then create one
		mem = make_memory(user_id, "files")
		# just return, there are no files to remove
		# once created the memory, return the new data
		return mem.dic