import time
import bottle
from util import *

import tkn
import user
import imgur

### bottle wrappers & util funcs
def handleError(callback):
    def wrapper(*args, **kwargs):
        try:
            body = callback(*args, **kwargs)
            return "ok" if body is True else body
        except Exception as e:
            bottle.response.status = 404
            return e 
            
    return wrapper
bottle.install(handleError)

def getReq(key):
    return bottle.request.query.get(key)

def verifyUser():
    # expired in 3 hours
    expired = 1000*60*60*3

    usr = tkn.extTkn(bottle.request.headers.get("Authorization"))
    if not usr: return False
    
    issat = usr.get("issat")
    if issat and int(time.time())-issat>expired: return False

    return usr

@bottle.get("/login")
def user_logIn():
    return user.genCode({
        "email": getReq("email")
    })

@bottle.get("/tkn")
def user_verify():
    email = getReq("email")
    code = getReq("code")
    if not email or not code: raise MalformedException

    valid = user.vrfCode({
        "email": email,
        "code": code 
    })
    
    if not valid: raise UnauthorizedException  
    return tkn.genTkn({
        "email": email,
        "issat": int(time.time())
    })

@bottle.get("/user/name")
def user_updateName():
    name = getReq("name")
    if not name: raise MalformedException

    usr = verifyUser()
    if not usr: raise UnauthorizedException
    
    return user.chgName({
        "email": usr.get("email"),
        "name": name 
    })

@bottle.get("/admin/newUser")
def admin_newUser():
    # TODO: jwt checking
    name = getReq("name")
    email = getReq("email")

    return user.newUser({"email":email, "name":name})

bottle.run(host="0.0.0.0", port=8000)
