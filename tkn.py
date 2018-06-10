import os
import json

import hashlib
import base64 as b64

KEY = os.environ.get("TKN_KEY")

### hash func
def getHash(stuff):
    return hashlib.sha256(stuff).hexdigest()

### return token, based roughly on JWT
def getTkn(obj):
    pload = json.dumps(obj)
    shash = getHash(pload+KEY)
    return "%s.%s"%(b64.b64encode(pload), shash)

### if not verified, return None
def extTkn(tkn):
    pload, shash = tkn.split(".")
    obj = b64.b64decode(pload)
    shash2 = getHash(obj+KEY) 
    return json.loads(obj) if shash==shash2 else None
