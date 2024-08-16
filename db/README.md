# DataBase System

This is a DB based on `JSON` Since Lambda initially was created to be a **Discord Bot** then there were certain rules to follow in the creation of this system, some irregular rules: users aren’t going to sign up, neither create counts to interact with the Bot. That’s why new users are going to be processed as already known ones.

## Memory Files `db/data/`

These memory files are essentially `.json`s that save all the data, just like MongoDB. These are usually saved as `[id].json`. Also the distribution of these files starts in `db/data/` and:

- `errors`
- `images`
- `log`
- `members`
- `servers`
- `userlist`
- `verbs`

The details about every one of these DB collections are explained bellow.

## About Prototypes and Usages `db/presets/`

### Prototypes

As previous mentioned, the new users and the old ones are processed by the same function. This is because this DB is based in **prototypes**. This is the main case for which the DB was created:

1. An unknown user sends a message
2. Then inside the system it’s needed to `get` the user data from the db (*in most of the cases*).
3. The DB looks for the user data in `members`
    1. **If member exists**: then return the user data as a python dict.
    2. Else: create a new user data, based on the `member prototype`

As in this case, there are prototypes for `members`, `servers` and `errors`, when a new one presents, then create one based on the prototype.

### Usages

Lambda was designed to be an AI system that **provides AI services to many users**, then there must be a measure for how many resources can every user use. This is why `roles` and `usages` where created: **depending on the role, the resources that the user is allowed to use**. Some users may have more than others, or perhaps more privileges than others (*then need to implement special conditions in lambda skills*).

Every user, in his DB data has a field that is his current usage, then every time the user uses something count as a service, that will be discounted to his usage. Also the users’ usages are reloaded every week (*by default, it can be changed*). The users’ remaining days to reload are located in `userlist.json` and are daily modified by a `daily script` named `usage_updater.py`.

**Note: the default usage that `prototypes` has is `free`. Also if a new user is created by a `get` request to `/members`, the default usage will be `free`. Although if the user is created by a `post` on `/userlist` then the usage will be the one assigned on `usages.json` to the `role` specified on the request.**

## Requests, Methods and Details

### `/members`

- `GET`
    
    ```json
    {
    	"id": "user id",
    	"server": "server name"
    }
    ```
    
    This is to access the JSON file from a user given its ID, if the file does not exist, then it will create a new one (*based on prototype*). Also will append to servers the sent server if it isn’t on the list.
    
    `returns user data`
    
- `PUT`
    
    ```json
    {
    	"id": "user id",
    	"data": "{updates for the user data}"
    }
    ```
    
    This one will open the user data and then overwrite it based it on the `data` content. For example: if there was a change in the curren usage of the user, then just send **the new usage inside `data`** and then only the usage field will be updated in the user data.
    
    **Note: the data needs to be a STRING, normally generated with** `json.dumps()` function 
    
    `returns an "ok"`
    

### `/servers`

**Special Note:** Lambda started around 2019 as a discord Bot, and one of its initial functions was creating temporary whitelists to a selected voice channel. This is why this DB was created.

- `GET`
    
    ```json
    {
    	"id": "server id",
    	"name": "name of the server"
    }
    ```
    
    As users, when the server data file isn’t found, then it creates one (equally based in the prototype), also overwrites the name of the server, which is due to detection of future name updates.
    
    `returns server data`
    
- `PUT`
    
    ```json
    {
    	"id": "server id",
    	"name": "name of the server",
    	"data": "data from the channel",
    	"__example__": "{\"lockdown_channel\": \"canal-2\", \"lockdown_members\": [2,3]}"
    }
    ```
    
    It basically updates the server data. Same as before, the field `data` must be a python dict or a JSON, all in a string format.
    
    `returns an "ok"`
    

### `/images`

- `POST`
    
    ```json
    {
    	"id": "id of the image",
    	"url": "public url",
    	"prompt": "image promt"
    }
    ```
    
    This db was specially created to make a recording of every image created and its prompts, to eventually create a gallery with all the images. Basically creates a new image file with the information. Usually the `id` is a hash created on the image generation.
    
    `returns an "ok"`
    

### `/verbs`

- `GET`
    
    ```json
    {
    	"verb": "verb that it's needed the info"
    }
    ```
    
    Simply looks for the verb data, and if the verb doesn’t exist, it returns a `"404"`.
    
    `returns verb data`
    
- `POST`
    
    ```json
    {
    	"skill": "location of the .py skill file",
    	"words": ["list of words to add to verb", ...],
    	"verbs": ["list of verbs to add the words", ...],
    	*"create": "any value or not defined, it can be a yes"
    }
    ```
    
    This requests are going to append the `word: skill` to the verb data, but if any of the `word`s already exist, then it will overwrite it, be careful. On the other hand, `skill` is the **location of the skill python file starting from `skills/` but removing the last `.py`.** 
    
    `create` is something as a lock that allows to create new verb files when some of the `verbs` isn’t found. It will create the verb as a `type: multi`. To create `general` type functions, it will need to be made manually.
    
    `returns an "ok”` if the verbs were found and `create` is defined.
    
    `returns a list of verbs` if there were verbs not found and `create` is not defined.
    
- `DELETE`
    
    ```json
    {
    	"skill": "iot.test"
    }
    ```
    
    Special function made to remove skills easily from every verb their’e in. Use carefully. Mainly made for administrative and maintenance purposes.
    
    `return a list of verbs` from where was removed the skill.
    
- `PATCH`
    
    ```json
    {
    	"search": "[word | function | skill]",
    	"value": "explained bellow"
    }
    ```
    
    Also an special function that was made for searching info about the verbs and skills. Mainly made for administrative and maintenance purposes. This function has 3 different uses depending on the `search` value:
    
    - `word` looks for in what verbs appears the word, `value` is that word. `returns a list os verbs`.
    - `function` search in what verbs appears the skill, `value` is that skill. `returns a list os verbs`.
    - `skill` this one was specially designed to see in what verbs and what words are associated to a given `skill`. `value` must be that skill. `returns a disct of verbs that contain a list of words`.

### `/logs`

- `POST`
    
    ```json
    {
    	"db": "log to locate the message",
    	"data": "message"
    }
    ```
    
    The log system was designed to be pretty simple to use and is currently being used for most parts of the whole Lambda system, also for the extra apps.
    
    This DB part basically handles all the files with an `append` mode. Receives two params, `db` is the **name of the file to append the message** and `data` is the message to append to the log file.
    
    The text appended to the file isn’t just the `data` message, furthermore the date from the system is added. Here are a few examples of lines from logs:
    
    - `from bchat-recepipts`
        
        > [*random user id*]-lambda-La humedad es de 0.0%- [2024-03-24 - 22:09:49]
        > 
    - `from userlist`
        
        > [POST] moved [*random user id*] to pro [2024-08-15 - 13:59:12]
        > 
    - `from tokens`
        
        > [*random user id*] in: 321 out: 157 adjusted: 204 total: 525 [2023-09-20 - 16:54:50]
        > 
    - `from bin`
        
        > Rupdating Lambda at [2024-03-24 - 22:44:59]
        > 
    
    **Note: logs are normally cleaned after a Lambda backup, usually ran weekly.**
    

### `/errors`

- `POST`
    
    ```json
    {
    	"data": "{content dict as a string}"
    }
    ```
    
    Lambda has a special system to report errors that most usually pass on bad prompts or other internal system exceptions. This system saves info about the errors occurred. The way the request works is **sending a dict with the error info, but parsed as a string**, the content follows the next structure:
    
    ```json
    "data": {
    		"call": "lambda prompt that generated the error",
     		"code": "error code",
     		"member": "user id",
     		"server": "server id"
    }
    ```
    
    It also send a message to a Telegram chat every when an error occurs. The errors’ code is hashed and that hash is the way that Lambda recognizes errors and save the files as `[error id].json` and also counts **how many times this same error have happened**.
    

### `/userlist`

- `GET`
    
    ```json
    {}
    ```
    
    This function will return the whole `userlist` data, it doesn’t receives noting
    
    `returns the userlist`
    
- `POST`
    
    ```json
    {
    	"role": "role to append the users",
    	"users": ["user ids to append to the role"]
    }
    ```
    
    These function appends a **list of users** to a given `role` in the `userlist`. This function has several freedoms over the DB:
    
    - If the `role` is not defined `usages.json` then it will be set as `free`.
    - If the `role` isn’t already defined in `userlist`, then it will be created.
    - If one or more of the given `users` isn’t already found in `members`, then the user data **will be created, setting its usage as the one from the given** `role`.
    - Also the list of `users` can contain **new users and existing users in the same query**.
    
    `returns an ok`
    
- `PUT`
    
    ```json
    {}
    ```
    
    **Note: the returning of these function is passed to `PATCH`.** 
    
    - **`PUT` is the query that discounts days to users in `userlist`.**
    - **`PATCH` is the responsable of recharge the users `usages`, based on the result of the `PUT`.**
    
    Both of these request are daily executed by the daily script `usage_updater.py`.
    
    `returns a cuasi userlist that has only users needed to recharge them usage`, something like this (example):
    
    ```json
    {
        "free": ["user-1", "user-2", "user-3",]
        "pro": ["user-4"]
        "admin": []
    }
    ```
    
- `PATCH`
    
    **This request receives the result shown before, but parsed as a string.**
    
    This is responsible to restore the users `usages`, for those users that has reach the day count `0` and need them usage to be restored. **That list is provided as a result of a `PUT` request. See above documentation for `userlist` `PUT`.**
    
    `returns an "ok"`
    

### **Dev Notes**

- All the answers come in the next format `{ "answer": ... }`
- The way the DB reads the field `data` in ALL REQUESTS must be a JSON or a python dict, both in a STRING FORMAT. Except for `logs`.
- All the `data` fields need to be STRINGS and their’e loaded with `data = eval(data_string)` or `json.loads(data_string)`
- If one of the fields of the query contains a list, it’s going to be a **list and not a string**.

## DB Schemes `prototypes` and `usages`

```json
{	
	"__comment__": "usages are still going to be adjusted",

	"members": {
		"servers": [],
		"role": "free",
		"usage": {
			"talk": 300000,
			"text": 150000,
			"intelligence": 150000,
			"research": 150000,
			"vision": 150000,
			"voice": 100000,
			"images": 20,
			"ear": 300
		},
		"file": "",
		"memory": "",
		"credentials": {
			"hint": "",
			"hash": ""
		},
		"devices": {},
		"personality": "Eres una IA asistente",
		"context_len": 0,
		"context": [
			{
				"role": "system", "content": "Eres alguien inteligente"
			}
		]
	},

	"servers": {
		"name": "",
		"lockdown_channel": "",
  	"lockdown_members": []
	},

	"errors": {
		"count": 1,
		"code": "",
		"servers": [],
		"members": [],
		"calls": []
	}
}
```

### `members`

- `servers` contains the servers from where a user has made prompts. These are added automatically with the usage.
- `role` shows the current user `role` associated to its available usage, it’s changed through `userlist` actions.
- `usage` contains a dict that show the available resources for the user. It is recharged once the user days come to `0` in the `userlist`. It can only be recharged through `userlist` actions.
- `file` contains the `hash` of the current file uploaded by the user without the extension. **The folder, extension and other details to load the file are given by the skill that uses the file**.
- `memory` saves things that the user wants.
- `credentials` saves Lambda System credentials that are given by the users:
    - `hint` has a special hint to remember the password in case of being forgotten.
    - `hash` is the hash associated to the user’s given password.
- `devices` this is a dict that contains the info about the devices connected to Lambda IoT client. **This field is only changed when the `IoT Client` establish connection, this process uploads the list of devices connected to the system.**
- `personality` this is the content of the first message that inits the context, usually used to set the style of the answers. **Normally when changed the current context is deleted.**
- `context_len` simply contains the current size of the context. It’s updated after every answer.
- `context` contains the context structure for conversation. **It is automatically deleted every once its len reaches a certain limit, defined on Lambda `config`**.

### `servers`

- `name` contains the name of the server.
- `lockdown_channel` name of the channel that currently locates the lockdown.
- `lockdown_members` list of allowed members to enter the channel.

### `errors`

- `count` shows the frequency of appearance of the error. How many times has it happened.
- `code` displays the error code.
- `servers` list of servers where the error has appeared.
- `members` users’ ids that cause the error.
- `calls` prompts that cause the error.

## Special Rules `members` and `userlist`

- Create a new `member` will also **append that member as a free** user to `userlist`
- Post an **unexisting member** in `userlist` will create a `member`, but with the usage assigned to the specified role.

## Errors

Once a while, errors occur in the whole system, due to wrong inputs or prompts, or any other reasons. The need of tracking and report all these errors was the reason behind the creation of this collection. The process is simple, an error request comes on `/errors` and has the next format:

```json
"data": {
		"call": "lambda prompt that generated the error",
 		"code": "error code",
 		"member": "user id",
 		"server": "server id"
}
```

1. The data is receipt.
2. The error code is hashed.
3. Look for that hash and look for the error
    1. If it exists then
        1. count one more to the error frequency
        2. and add extra info
    2. Else
        1. create a new error based on prototype

Finally once the error is registered finally send a message to telegram selected chat (*through a bot*) to report the error.

## Logs

Since this system is basically a collection of server programs running in parallel, using many different types of process, then a flexible log system was implemented, as simple that only receives a message and a file name. Then as the whole Lambda system grows, the logs are going to be recording every important process operations.

The log files are easily read since they are .txt (*but the extension can be changed*). There are several log files for different purposes:

- `audios` contains info and about all the audios generated by the users.
- `bchat-errors` contains all the unknown messages incoming to the `bchat` server, which is used to communicate with the IoT Lambda Network.
- `bchat-receipts` contains the well receipt messages from `bchat` server. These messages are read by `iot skills` to deliver answers on chat.
- `bchat` this is a main log that contains what users and IPs have establish connection with the `bchat` server, also the users’ `devices` are passed through that initial connection.
- `bin` contains all the operations ran by the Lambda script located in `bin/lambda`, these operations include: starting or stopping Lambda main systems, running or killing Lambda extra apps, update the code, new requirements installed, and backups.
- `cloudinary` contains what users have upload and image to `cloudnary`, normally used to pass the public url to LLMs that has image input, or image generation.
- `errors` other log oriented to save errors, it saves the user and the prompt that generate the error.
- `images` contains info about image generation, and also previously variation and edition.
- `tokens` contains how many token usage generates each prompt from the users. It saves token input, output, total and adjusted (*something calculated to standardize operation costs*).
- `userlist` contains info abut all the movements made inside the `userlist`, moving users to roles, user restore and the `userlist` routines.

*Last update 16/8/2024*