import requests

class Logger:
    url = ''

    def __init__(self):
        self.url = 'https://tfn85zvwe5.execute-api.us-west-1.amazonaws.com/default/logging'

    def post_log(self, log):
        requests.post(self.url, log)
