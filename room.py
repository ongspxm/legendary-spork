import dbase
import imgur
from util import *

### (rmId) => {_id, u_id, name, ..}
def getRoom(rmId):
    res = dbase.select("rooms", "where _id=?", [rmId])
    if not len(res): raise RoomNotExistException
    return res[0]

### ({email, pager}) => [{rid, email, name, range, avail, imgs}]
def getRooms(obj):
    email = obj.get("email")
    pager = obj.get("pager")
    if not pager: pager = 0

    qry = "where _id>?"
    val = [pager]

    if email:
        qry += " and u_email=?"
        val.append(email)

    res = map(lambda rm: {
        "rid": rm["_id"],
        "name": rm["name"],
        "email": rm["u_email"],
        "range": rm["weekRange"],
        "avail": rm["numAvailable"],
        "imgs": map(
            lambda img: img["link"],
            dbase.select("images", "where r_id=?", [rm["_id"]])
        )
    }, dbase.select("rooms", qry, val))

    return res

### ({user, name, vacy, aval}) => True
def newRoom(obj):
    user = obj.get("user")
    name = obj.get("name", "<hosting name>")
    vacy = obj.get("vacy", 0)
    aval = obj.get("aval", 52)
    if not user: raise MalformedException

    return dbase.insert("rooms", {
        "u_email":user["email"],
        "name":name,
        "numAvailable":vacy,
        "weekRange":aval
    })

### ({rmId, name, vacancy, available}) => True
def updateRoom(obj):
    rmId = obj.get("rmId")
    name = obj.get("name")
    vacy = obj.get("vacy")
    aval = obj.get("aval")
    if not rmId: raise MalformedException

    res = {}
    if name: res["name"] = name
    if vacy: res["numAvailable"] = vacy
    if aval: res["weekRange"] = aval

    return dbase.update(
            "rooms", "where _id=?",
            [rmId], res)

### ({user, rmId}) => True
def delRoom(obj):
    user = obj.get("user")
    rmId = obj.get("rmId")
    if not user or not rmId:
        raise MalformedException

    return dbase.delete(
            "rooms", "where u_email=? and _id=?",
            [user["email"], rmId])


### ({rmId, picData}) => {imgur, link, r_id, dhash}
def addImg(obj):
    rmId = obj.get("rmId")
    data = obj.get("picData")
    if not rmId or not getRoom(rmId) or not data:
        raise MalformedException

    img = imgur.uploadImg(data)
    img["r_id"] = rmId

    dbase.insert("images", img)
    return img

### ({rmId, imgurId}) => True
def delImg(obj):
    rmId = obj.get("rmId")
    imgId = obj.get("imgurId")
    if not rmId or not getRoom(rmId) or not imgur:
        raise MalformedException

    img = dbase.select("images", "where imgur=? and r_id=?", [imgId, rmId])
    if not len(img): raise ImageNotExistException
    img = img[0]

    return imgur.deleteImg(img["dhash"])
