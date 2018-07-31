"""application logic for users"""

import re
import time

from util import get_template, rand_code
from util import TIMEOUT_USER_VERIFICATION
from util import EXCEPTION_USER_EXIST, EXCEPTION_USER_NOT_EXIST
from util import EXCEPTION_DATABASE, EXCEPTION_UNAUTHORIZED, EXCEPTION_MALFORMED

import dbase
from mailgun import sendmail

### (email) => True/False
def is_valid_email(email):
    """validate that email is in right format"""

    if email and len(email) > 7:
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
    return False

### (email) => ({email, code})
def get_user(email):
    """get user object from db"""

    res = dbase.select("users", "where email=?", [email])
    return res[0] if res else None

### () => [{email, name}]
def get_users():
    """return list of users"""
    return dbase.select("users")

### (email) => True/False
def is_admin(email):
    """check if an email has admin rights"""

    res = dbase.select("admins", "where email=?", [email])
    return len(res) == 1

### (email) => True/False
def is_user_exist(email):
    """verify that an user exist"""
    return get_user(email) is not None

### ({email, name}) => True/False
def new_user(usr):
    """create new user with name and email"""

    email = usr.get("email")
    if not is_valid_email(email):
        raise EXCEPTION_MALFORMED
    if is_user_exist(email):
        raise EXCEPTION_USER_EXIST

    name = usr.get("name", email)
    return dbase.insert("users", {
        "email": email,
        "name": name
    })

### ({email, name}) => True
def chg_name(usr):
    """change the name of the user"""

    email = usr.get("email")
    if not is_user_exist(email):
        raise EXCEPTION_USER_NOT_EXIST

    name = usr.get("name", email)
    return dbase.update("users", "where email=?", [email], {
        "name": name
    })

### ({email}) => code1
def gen_code(usr):
    """generate code to be emailed to user"""

    email = usr.get("email")
    if not is_user_exist(email):
        raise EXCEPTION_USER_NOT_EXIST

    part1, part2 = rand_code(), rand_code()
    res = dbase.update("users", "where email=?", [email], {
        "code": part1+"-"+part2,
        "tstamp": int(time.time())
    })

    if not res:
        raise EXCEPTION_DATABASE

    sendmail({
        "to": email,
        "subj": "logging in",
        "text": get_template("email_verification")%(part1+"-"+part2)
    })
    return part1

### ({email, code}) => True
def vrf_code(usr):
    """verify that the code received is same as server
    will clear the password on one wrong try
    """
    email = usr.get("email")
    user = get_user(email)
    if user is None:
        raise EXCEPTION_USER_NOT_EXIST

    diff = int(time.time()) - user.get("tstamp", 0)
    if diff > TIMEOUT_USER_VERIFICATION:
        raise EXCEPTION_UNAUTHORIZED

    code = usr.get("code")
    check = user.get("code")
    if not code or not check:
        raise EXCEPTION_MALFORMED

    if not dbase.update("users", "where email=?",
                        [email], {"code": "", "tstamp":0}):
        raise EXCEPTION_DATABASE

    return code == check
