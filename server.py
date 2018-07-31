"""main server script for starting the web application"""

import json
import bottle
from util import EXCEPTION_MALFORMED, EXCEPTION_UNAUTHORIZED

import tkn
import room
import users
import dbase

### bottle wrappers & util funcs
def handle_error(callback):
    """function to return cors headers"""

    def wrapper(*args, **kwargs):
        """wrapper func"""

        bottle.response.set_header("Access-Control-Allow-Origin", "*")
        bottle.response.set_header("Access-Control-Allow-Methods", "*")
        bottle.response.set_header("Server", "httpd 2.4.33")

        try:
            body = callback(*args, **kwargs)

            if body is True:
                return "ok"
            return json.dumps(body)
        except Exception as exception:
            bottle.response.status = 404
            return exception

    return wrapper
bottle.install(handle_error)

def get_req(key):
    """util function to get val from request"""

    return dict(bottle.request.query).get(key)

def verify_user():
    """util func to verify that user is authenticated"""

    jwt_tkn = dict(bottle.request.headers).get("Authorization")
    if not jwt_tkn:
        return None

    usr = tkn.extTkn(jwt_tkn)
    return usr

@bottle.route("/login", method=["OPTIONS", "GET"])
def user_log_in():
    """send login verification code to user"""

    return users.gen_code({
        "email": get_req("email")
    })

@bottle.route("/tkn", method=["OPTIONS", "GET"])
def user_verify():
    """return token to authenticated user"""

    email = get_req("email")
    code = get_req("code")
    if not email or not code:
        raise EXCEPTION_MALFORMED

    valid = users.vrf_code({
        "email": email,
        "code": code
    })

    if not valid:
        raise EXCEPTION_UNAUTHORIZED
    return tkn.genTkn(email)

@bottle.route("/user/name", method=["OPTIONS", "GET"])
def user_update_name():
    """signed in user can update their name"""

    name = get_req("name")
    if not name:
        raise EXCEPTION_MALFORMED

    usr = verify_user()
    if not usr:
        raise EXCEPTION_UNAUTHORIZED

    return users.chg_name({
        "email": usr.get("email"),
        "name": name
    })

@bottle.route("/rooms", methods=["OPTIONS", "GET"])
def room_list():
    """anyone can list rooms for viewing"""

    email = get_req("email")
    pager = get_req("pager")

    return room.get_rooms({
        "email": email,
        "pager": pager
    })

@bottle.route("/room/new", method=["OPTIONS", "GET"])
def room_new():
    """signed in user can create new room"""

    usr = verify_user()
    if not usr:
        raise EXCEPTION_UNAUTHORIZED

    name = get_req("name")
    vacy = get_req("vacancy")
    aval = get_req("weekRange")

    return room.new_room({
        "users": usr,
        "name": name,
        "vacy": vacy,
        "aval": aval
    })

@bottle.route("/room/edit", method=["OPTIONS", "GET"])
def room_edit():
    """authenticated user can edit details of room"""

    usr = verify_user()
    if not usr:
        raise EXCEPTION_UNAUTHORIZED

    r_id = get_req("rm")
    name = get_req("name")
    vacy = get_req("vacancy")
    aval = get_req("weekRange")
    if not r_id:
        raise EXCEPTION_MALFORMED

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [r_id, usr["email"]])
    if not res:
        raise EXCEPTION_UNAUTHORIZED

    return room.update_room({
        "rmId": r_id,
        "name": name,
        "vacy": vacy,
        "aval": aval
    })

@bottle.route("/room/newImg", method=["OPTIONS", "POST"])
def room_new_img():
    """authenticated user can add img to room"""

    usr = verify_user()
    if not usr:
        raise EXCEPTION_UNAUTHORIZED

    r_id = get_req("rm")
    data = dict(bottle.request.files).get("img").file.read()
    if not r_id or not data:
        raise EXCEPTION_MALFORMED

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [r_id, usr["email"]])
    if not res:
        raise EXCEPTION_UNAUTHORIZED

    res = room.add_img({
        "rmId": r_id,
        "picData": data
    })
    return "%s %s"%(res["link"], res["imgur"])

@bottle.route("/room/del_img", method=["OPTIONS", "GET"])
def room_del_img():
    """authenticated user can remove image from room"""

    usr = verify_user()
    if not usr:
        raise EXCEPTION_UNAUTHORIZED

    r_id = get_req("rm")
    img_id = get_req("imgId")
    if not r_id or not img_id:
        raise EXCEPTION_MALFORMED

    qry = "where _id=? and u_email=?"
    res = dbase.select("rooms", qry, [r_id, usr["email"]])
    if not res:
        raise EXCEPTION_UNAUTHORIZED

    return room.del_img({
        "rmId": r_id,
        "imgurId": img_id
    })

@bottle.route("/admin/new_user", method=["OPTIONS", "GET"])
def admin_new_user():
    """admin function to add new users"""

    usr = verify_user()
    if not usr or not users.is_admin(usr["email"]):
        raise EXCEPTION_UNAUTHORIZED

    name = get_req("name")
    email = get_req("email")

    return users.new_user({"email":email, "name":name})

@bottle.route("/admin/listUsers", method=["OPTIONS", "GET"])
def admin_list_users():
    """admin function to list users"""

    usr = verify_user()
    if not usr or not users.is_admin(usr["email"]):
        raise EXCEPTION_UNAUTHORIZED

    return [{
        "name": usr["name"],
        "email": usr["email"]
    } for usr in users.get_users()]

bottle.run(host="0.0.0.0", port=8000)
