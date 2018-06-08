import time
import dbase
from util import *

### (email) => ({email, code})
def getUser(email):
    res = dbase.select("users", "where email=?", [email])
    return res[0] if res else None

### (email) => True/False
def isUserExist(email):
    return getUser(email) is not None

### ({email, name}) => True
def newUser(usr): 
    # TODO: check valid email
    email = usr.get("email")
    if not email:
        raise MalformedException
    if isUserExist(email): 
        raise UserExistException
    
    name = usr.get("name", email)
    return dbase.insert("users", {
        "email": email,
        "name": name
    }) 

### ({email, name}) => True
def cngName(usr):
    email = usr.get("email")
    if not isUserExist(email): raise UserNotExistException
    
    name = usr.get("name", email)
    return dbase.update("users", "where email=?", [email], {
        "name": name
    }) 

### ({email}) => code1
def genCode(usr):
    email = usr.get("email")
    if not isUserExist(email): raise UserNotExistException

    part1, part2 = randCode(), randCode()
    res = dbase.update("users", "where email=?", [email], {
        "code": part1+"-"+part2,
        "tstamp": int(time.time()) 
    })

    if not res: raise DatabaseException

    # TODO: send mail
    return part1

### ({email, code}) => True
def vrfCode(usr): 
    email = usr.get("email")
    user = getUser(email)
    if user is None: raise UserNotExistException

    code = usr.get("code")
    check = user.get("code")
    if not code or not check: 
        raise MalformedException

    if not dbase.update("users", "where email=?", 
            [email], { "code": "" }):
        raise DatabaseException
    
    return code==check
