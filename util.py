import random
import base64 as b64

MalformedException = Exception("Malformed request")
DatabaseException = Exception("Database function failed")

UserExistException = Exception("User already exist")
UserNotExistException = Exception("User doesnt exist")

def randCode(leng=3):
    return b64.b64encode(str(random.random()))[:leng] 
