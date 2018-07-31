"""application logic for rooms"""

import dbase
import imgur
from util import EXCEPTION_ROOM_NOT_EXIST, EXCEPTION_MALFORMED, EXCEPTION_IMAGE_NOT_EXIST

### (rm_id) => {_id, u_id, name, ..}
def get_room(rm_id):
    """get room by the id"""

    res = dbase.select("rooms", "where _id=?", [rm_id])
    if not res:
        raise EXCEPTION_ROOM_NOT_EXIST

    return res[0]

### ({email, pager}) => [{rid, email, name, range, avail, imgs}]
def get_rooms(obj):
    """get list of all rooms"""

    email = obj.get("email")
    pager = obj.get("pager")
    if not pager:
        pager = 0

    qry = "where _id>?"
    val = [pager]

    if email:
        qry += " and u_email=?"
        val.append(email)

    res = [{
        "rid": rm["_id"],
        "name": rm["name"],
        "email": rm["u_email"],
        "range": rm["weekRange"],
        "avail": rm["numAvailable"],
        "imgs": [
            img["link"] for img in
            dbase.select("images", "where r_id=?", [rm["_id"]])
        ]
    } for rm in dbase.select("rooms", qry, val)]

    return res

### ({user, name, vacy, aval}) => True
def new_room(obj):
    """create new room owned by user"""

    user = obj.get("user")
    name = obj.get("name", "<hosting name>")
    vacy = obj.get("vacy", 0)
    aval = obj.get("aval", 52)
    if not user:
        raise EXCEPTION_MALFORMED

    return dbase.insert("rooms", {
        "u_email":user["email"],
        "name":name,
        "numAvailable":vacy,
        "weekRange":aval
    })

### ({rm_id, name, vacancy, available}) => True
def update_room(obj):
    """update room details"""

    rm_id = obj.get("rm_id")
    name = obj.get("name")
    vacy = obj.get("vacy")
    aval = obj.get("aval")
    if not rm_id:
        raise EXCEPTION_MALFORMED

    res = {}
    if name:
        res["name"] = name

    if vacy:
        res["numAvailable"] = vacy

    if aval:
        res["weekRange"] = aval

    return dbase.update(
        "rooms", "where _id=?",
        [rm_id], res)

### ({user, rm_id}) => True
def del_room(obj):
    """delete room owned by user"""

    user = obj.get("user")
    rm_id = obj.get("rm_id")
    if not user or not rm_id:
        raise EXCEPTION_MALFORMED

    return dbase.delete(
        "rooms", "where u_email=? and _id=?",
        [user["email"], rm_id])


### ({rm_id, picData}) => {imgur, link, r_id, dhash}
def add_img(obj):
    """add image to room"""

    rm_id = obj.get("rm_id")
    data = obj.get("picData")
    if not rm_id or not get_room(rm_id) or not data:
        raise EXCEPTION_MALFORMED

    img = imgur.upload_img(data)
    img["r_id"] = rm_id

    dbase.insert("images", img)
    return img

### ({rm_id, imgurId}) => True
def del_img(obj):
    """remove image from room"""

    rm_id = obj.get("rm_id")
    img_id = obj.get("imgurId")
    if not rm_id or not get_room(rm_id) or not imgur:
        raise EXCEPTION_MALFORMED

    img = dbase.select("images", "where imgur=? and r_id=?", [img_id, rm_id])
    if not img:
        raise EXCEPTION_IMAGE_NOT_EXIST
    img = img[0]

    return imgur.delete_img(img["dhash"])
