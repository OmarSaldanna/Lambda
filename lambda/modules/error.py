# very special module implemented to throw errors inside skills
# may be used for more in the future
# based on brain error

# import the DB handler
from modules.db import DB

# instance db
db = DB()
 
def error (content: str, params: tuple)
	# get the params
	message, member, server = params
    # save it in the error db
    db.post("/errors", {
      "data": {
        "call": message,
        "code": error_str,
        "member": member,
        "server": server
      }
    })
    # and in logs
    db.post("/logs", {
      "db" : "errors",
      "data": f"[{member}] {message}"
    })