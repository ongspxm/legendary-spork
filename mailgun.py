import os
import requests

MAILGUN_API = os.environ.get("MG_API")
MAILGUN_DOM = os.environ.get("MG_DOM")
MAILGUN_EML = os.environ.get("MG_EML")
MAILGUN_URL = "https://api.mailgun.net/v3/%s/messages"%(MAILGUN_DOM)

### ({text, subj, from, to})
def sendmail(msg):
    return requests.post(
        MAILGUN_URL, auth=("api", MAILGUN_API),
        data = {
            "to": [msg["to"]],
            "text": msg["text"],
            "from": MAILGUN_EML,
            "subject": msg["subj"]
        }
    )
