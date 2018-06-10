import dbase
from util import *

### ({user, name, vacancy, availability}) => True/False
def newRoom(obj):
    user = obj.get("user")
    name = obj.get("name", "<hosting name>")
    vacy = obj.get("vacancy", 0)
    aval = obj.get("availablity", 52)
    if not user: raise MalformedException

    return dbase.insert("rooms", {
        "u_email":user["email"],
        "name":name,
        "numAvailable":vacy,
        "weekRange":aval
    })

### ({rmId, name, vacancy, available}) => True/False
def updateRoom(obj):
    rmId = obj.get("rmId")
    name = obj.get("name")
    vacy = obj.get("vacancy")
    aval = obj.get("availablity")
    if not rmId: raise MalformedException

    res = {}
    if name: res["name"] = name
    if vacy: res["numAvailable"] = vacy
    if aval: res["weekRange"] = aval

    return dbase.update(
            "rooms", "where _id=?",
            [rmId], res)

### ({user, rmId}) => True/False
def delRoom(obj):
    user = obj.get("user")
    rmId = obj.get("rmId")
    if not user or not rmId:
        raise MalformedException

    return dbase.delete(
            "rooms", "where u_email=? and _id=?", 
            [user["email"], rmId])


### ({rmId, picData})
def addImg(): pass

### ({rmId, imgurId})
def delImg(): pass
