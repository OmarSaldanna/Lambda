import requests
import json

# a function that updates the users days left on db
userlist = requests.put("http://127.0.0.1:8081/userlist").json()['answer']
# the userlist contains the users that need to be restored, organized
# in a dict of lists, where the keys are the roles and values the users.
# Then use the PATCH request and send the userlist to restore the users' usages
try:
	# try to restore the usages
	_ = requests.patch("http://127.0.0.1:8081/userlist", json={"userlist": json.dumps(userlist)})
except:
	# send a telegram alert throgh the db
	requests.post("http://127.0.0.1:8081/alerts", json={"content": "[DB] Error: Couldn't restore the users usages"})