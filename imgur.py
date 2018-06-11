import os
import json
import requests

import dbase
from util import *

API_EP = "https://api.imgur.com/3"
API_HD = {"Authorization": "Client-ID "+os.environ["IMGUR_API"]}

### (data) => ({imgur, link, dhash})
def uploadImg(data):
    req = json.loads(requests.post(
        headers=API_HD,
        API_EP+"/image",
        data={ "image":data }
    ).text)

    if not req.get("success"):
        raise ImgurException

    data = req["data"]
    return {
        "imgur": data.get("id"),
        "link": data.get("link"),
        "dhash": data.get("deletehash")
    }

### (dhash) => True
def deleteImg(dhash):
    req = json.loads(request.delete(
        headers=API_HD,
        API_EP+"/image/"+dhash
    ).text)

    if not req.get("success"):
        raise ImgurException 
    return True
