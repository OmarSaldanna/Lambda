import requests

# function to extract ids from mentions
def extract_id(mention: str):
	return mention[2:-1]

# 0      1   2       3 4   5 6
# agrega por mencion a pro a @users
# agrega por arroba a pro a @users
# lo mismo para mueve
def main(params: tuple):
	# catch params
	message, author, server = params
	# get the user data
	user_data = requests.get("http://127.0.0.1:8081/members", json={"db": "members", "id": author}).json()['answer']
	# verify that the user has an admin role
	if user_data['role'] != 'admin':
		# if not, return a warning
		return [{
			"type": "error",
			"content": f"Lo siento <@{author}> no tienes permiso para hacer eso"
		}]
	# then the user is an admin
	# cath the params
	splited_message = message.split(' ')
	# the role
	role = splited_message[4]
	# users mentions 
	users_mentions = splited_message[6:]
	# save each user id extracted from the mentions
	users = [extract_id(user) for user in users_mentions]
	# having the list of users and the role
	# make the post of the users in the role
	try:
		# make the request
		ans = requests.post(
			"http://127.0.0.1:8081/userlist",
			json={"role": role, "users": users}
		).json()['answer']
		# return the answer if everything okey
		return [{
			"type": "error",
			"content": f"Listo, usuarios agregados, {ans}"
		}]
	except:
		return [{
				"type": "error",
				"content": f"Ups, algo salió mal"
			}]



# info about the skill
info = """ya sabes que hace wey, pero te dejo un ejemplo: agrega por [mencion, arroba] a [rol] a @users. RECUERDA QUE SI VAS A AGREGAR A UN ROL NUEVO HAY QUE MODIFICAR: **usages.json** y quizá **userlist.json**"""