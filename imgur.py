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
        API_EP+"/image",
        headers=API_HD,
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
    req = json.loads(requests.delete(
        API_EP+"/image/"+dhash,
        headers=API_HD
    ).text)

    if not req.get("success"):
        raise ImgurException

    return dbase.delete("images", "where dhash=?", [dhash])
