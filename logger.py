import requests
import datetime
import json

def post_log(action):
    url = 'https://tfn85zvwe5.execute-api.us-west-1.amazonaws.com/default/logging'
    current_time = datetime.datetime.now()
    log = {
        'log': {
            'source': 'Bitebody.xyz API',
            'time': str(current_time),
            'action': action
        }
    }

    print(json.dumps(log))

    try:
        r = requests.get(url, data=json.dumps(log))
        print(r.text, r.status_code, r.reason)
    except Exception as e:
        print(e)
