import requests
import time
import os
from requests.auth import HTTPDigestAuth
from . import constants

# TODO: Make a wrapper class
class GitHubAPI:
    def __init__(self, user, access_token):
        self.USER = user
        self.TOKEN = access_token
        self.RATE_LIMIT = 5000
        self.updateRateLimitInfo()
    
    def updateRateLimitInfo(self):
        try:
            url = constants.GITHUB_BASE_URL + (constants.GET_USERS % (self.USER))
            response = requests.get(url, auth=(self.USER, self.TOKEN))
            rateLimitInfo = dict(response.headers)
            self.rateLimitRemaining = int(rateLimitInfo["X-RateLimit-Remaining"])
            self.rateLimitReset = int(rateLimitInfo["X-RateLimit-Reset"])
        except:
            self.rateLimitRemaining = 0
            self.rateLimitReset = time.time() + 60*60



    def checkRateLimit(self):
        now = time.time()
        if self.rateLimitReset < now:
            self.updateRateLimitInfo()
        if self.rateLimitRemaining <=0:
            time.sleep(self.rateLimitReset+5 - now)
            self.updateRateLimitInfo()
        self.rateLimitRemaining -=1

    def makeRequest(self, method, url, params=None, **kwargs):
        self.requestWithRetry(3, method, url, params=None, **kwargs)

    def requestWithRetry(self, retryCount, method, url, params=None, **kwargs):
        self.checkRateLimit()
        if method == "get":
            try:
                response = self.get(url, params, **kwargs)
                if response.status_code != 200 and retryCount > 0:
                    return self.requestWithRetry(retryCount-1, method, url, params=None, **kwargs)
                return response
            except requests.exceptions.RequestException as e:
                self.log(e)
                if retryCount > 0:
                    return self.requestWithRetry(retryCount-1, method, url, params=None, **kwargs)
        e = Exception(f'Retry failed for {method} {url} {params}')
        self.log(e)
        raise e


    def get(self, url, params=None, **kwargs):
        return requests.get(url, params, **kwargs)

    def log(self, logMessage):
        if os.path.exists(constants.LOGFILE):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        with open(constants.LOGFILE, append_write) as f:
            f.write(logMessage)

