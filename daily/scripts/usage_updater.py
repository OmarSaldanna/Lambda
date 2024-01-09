import requests

# a function that updates the users days left on db
userlist = request.put("http://127.0.0.1:8081/userlist")['answer']
# then find the users with 0 days left
for role in userlist.keys():
	for user in userlist

# firts make the put of all users, this will discount a day
# in the days left counter