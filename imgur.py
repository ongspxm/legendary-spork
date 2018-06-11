import os
import json
import requests

import dbase
from util import *

API_EP = "https://api.imgur.com/3"
API_ID = os.environ["IMGUR_API"]

### (data) => ({imgur, link, dhash})
def uploadImg(data):
    req = json.loads(requests.post(
        API_EP+"/image", 
        headers={ "Authorization": "Client-ID "+API_ID },
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
