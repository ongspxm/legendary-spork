import json
import bottle
from util import *

import tkn
import user
import room

### bottle wrappers & util funcs
def handleError(callback):
    def wrapper(*args, **kwargs):
        bottle.response.set_header("Access-Control-Allow-Origin", "*")
        bottle.response.set_header("Access-Control-Allow-Methods", "*")
        bottle.response.set_header("Server", "httpd 2.4.33")

        try:
            body = callback(*args, **kwargs)

            if body is True:
                return "ok"
            return json.dumps(body)
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
    jwtTkn = bottle.request.headers.get("Authorization")
    if not jwtTkn: return None

    usr = tkn.extTkn(jwtTkn)
    return usr

@bottle.route("/login", method=["OPTIONS", "GET"])
def user_logIn():
    return user.genCode({
        "email": getReq("email")
    })

@bottle.route("/tkn", method=["OPTIONS", "GET"])
def user_verify():
    email = getReq("email")
    code = getReq("code")
    if not email or not code: raise MalformedException

    valid = user.vrfCode({
        "email": email,
        "code": code
    })

    if not valid: raise UnauthorizedException
    return tkn.genTkn(email)

@bottle.route("/user/name", method=["OPTIONS", "GET"])
def user_updateName():
    name = getReq("name")
    if not name: raise MalformedException

    usr = verifyUser()
    if not usr: raise UnauthorizedException

    return user.chgName({
        "email": usr.get("email"),
        "name": name
    })

@bottle.route("/rooms", methods=["OPTIONS", "GET"])
def room_list():
    email = getReq("email")
    pager = getReq("pager")

    return room.getRooms({
        "email": email,
        "pager": pager
    })

@bottle.route("/room/new", method=["OPTIONS", "GET"])
def room_new():
    usr = verifyUser()
    if not usr: raise UnauthorizedException

    name = getReq("name")
    vacy = getReq("vacancy")
    aval = getReq("weekRange")

    return room.newRoom({
        "user": usr,
        "name": name,
        "vacy": vacy,
        "aval": aval
    })

@bottle.route("/room/edit", method=["OPTIONS", "GET"])
def room_edit():
    usr = verifyUser()
    if not usr: raise UnauthorizedException

    rmId = getReq("rm")
    name = getReq("name")
    vacy = getReq("vacancy")
    aval = getReq("weekRange")
    if not rmId: raise MalformedException

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [rmId, usr["email"]])
    if len(res)==0: raise UnauthorizedException

    return room.updateRoom({
        "rmId": rmId,
        "name": name,
        "vacy": vacy,
        "aval": aval
    })

@bottle.route("/room/newImg", method=["OPTIONS", "POST"])
def room_newImg():
    usr = verifyUser()
    if not usr: raise UnauthorizedException

    rmId = getReq("rm")
    data = bottle.request.files.get("img").file.read()
    if not rmId or not data:
        raise MalformedException

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [rmId, usr["email"]])
    if len(res)==0: raise UnauthorizedException

    res = room.addImg({
        "rmId": rmId,
        "picData": data
    })
    return "%s %s"%(res["link"], res["imgur"])

@bottle.route("/room/delImg", method=["OPTIONS", "GET"])
def room_delImg():
    usr = verifyUser()
    if not usr: raise UnauthorizedException

    rmId = getReq("rm")
    imgId = getReq("imgId")
    if not rmId or not imgId:
        raise MalformedException

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [rmId, usr["email"]])
    if len(res)==0: raise UnauthorizedException

    return room.delImg({
        "rmId": rmId,
        "imgurId": imgId
    })

@bottle.route("/admin/newUser", method=["OPTIONS", "GET"])
def admin_newUser():
    usr = verifyUser()
    if not usr or not user.isAdmin(usr["email"]):
        raise UnauthorizedException

    name = getReq("name")
    email = getReq("email")

    return user.newUser({"email":email, "name":name})

@bottle.route("/admin/listUsers", method=["OPTIONS", "GET"])
def admin_listUsers():
    usr = verifyUser()
    if not usr or not user.isAdmin(usr["email"]):
        raise UnauthorizedException

    return map(lambda usr: {
        "name": usr["name"],
        "email": usr["email"]
    }, user.getUsers())

bottle.run(host="0.0.0.0", port=8000)
