import os
import time
import json
import hashlib
import base64 as b64

from util import *

KEY = os.environ.get("TKN_KEY")

### hash func
def getHash(stuff):
    return hashlib.sha256(stuff).hexdigest()

### return token, based roughly on JWT
def genTkn(email):
    pload = json.dumps({
        "email": email,
        "expiry": int(time.time())+TIMEOUT_TOKEN_EXPIRY
    })
    shash = getHash(pload+KEY)
    return "%s.%s"%(b64.b64encode(pload), shash)

### if not verified, return None
def extTkn(tkn):
    pload, shash = tkn.split(".")
    jstr = b64.b64decode(pload)

    obj = json.loads(jstr)
    if not obj.get("expiry"):
        return None

    shash2 = getHash(jstr+KEY)
    diff = int(time.time()) - obj["expiry"]

    if not shash==shash2 or diff>0:
        return None
    return obj
