"""util funcs"""
import random
import string

import dbase

EXCEPTION_MALFORMED = Exception("Malformed request")
EXCEPTION_DATABASE = Exception("Database function failed")

EXCEPTION_USER_EXIST = Exception("User already exist")
EXCEPTION_USER_NOT_EXIST = Exception("User doesnt exist")
EXCEPTION_UNAUTHORIZED = Exception("Unauthorized action")

EXCEPTION_IMGUR = Exception("Imgur upload failed")
EXCEPTION_ROOM_NOT_EXIST = Exception("Room doesnt exist")
EXCEPTION_IMAGE_NOT_EXIST = Exception("Image doesnt exist")

TIMEOUT_HOUR = 1000*60*60
TIMEOUT_USER_VERIFICATION = TIMEOUT_HOUR
TIMEOUT_TOKEN_EXPIRY = TIMEOUT_HOUR*8

def get_template(key):
    """get text template from dbase"""
    return dbase.select("vals", "where key=?", [key])[0].get("val")

def rand_code(leng=3):
    """generate random string"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(leng))
