import dbase
import random, string

MalformedException = Exception("Malformed request")
DatabaseException = Exception("Database function failed")

UserExistException = Exception("User already exist")
UserNotExistException = Exception("User doesnt exist")
UnauthorizedException = Exception("Unauthorized action")

ImgurException = Exception("Imgur upload failed")
RoomNotExistException = Exception("Room doesnt exist")
ImageNotExistException = Exception("Image doesnt exist")

TIMEOUT_HOUR = 1000*60*60
TIMEOUT_USER_VERIFICATION = TIMEOUT_HOUR
TIMEOUT_TOKEN_EXPIRY = TIMEOUT_HOUR*8

def getTemplate(key):
    return dbase.select("vals", "where key=?", [key])[0].get("val");

def randCode(leng=3):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(leng))
