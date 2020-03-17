import requests
import datetime

def post_log(action):
    url = 'https://tfn85zvwe5.execute-api.us-west-1.amazonaws.com/default/logging'
    current_time = datetime.datetime.now()
    log = {
        "log": {
            "source": "Bitebody.xyz API",
            "time": str(current_time),
            "action": action
            }
        }

    requests.post(url, log)
