import requests
import time
from requests.auth import HTTPDigestAuth

# TODO: Make a wrapper class
GITHUB_BASE_URL = "https://api.github.com"
GET_EVENTS = "/events"
GET_USERS = "/users/%s" # .../:user
GET_COMMIT_COMMENTS = "/repos/%s/%s/comments" # .../:owner/:repo/...
GET_COMMENT_REACTION = "/repos/%s/%s/comments/%s/reactions" # .../:owner/:repo/.../:comment_id/...
REACTION_HEADER ={'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

class GitHubAPI:
    def __init__(self, user, access_token):
        self.USER = user
        self.TOKEN = access_token
        self.RATE_LIMIT = 5000
        self.updateRateLimitInfo()

    def rateLimitInfo(self):
        url = GITHUB_BASE_URL + (GET_USERS % (self.USER))
        return requests.get(url, auth=(self.USER, self.TOKEN))
    
    def updateRateLimitInfo(self):
        try:
            rateLimitInfo = dict(self.rateLimitInfo().headers)
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
                if retryCount > 0:
                    return self.requestWithRetry(retryCount-1, method, url, params=None, **kwargs) 
        raise Exception(f'Retry failed for {method} {url} {params}')


    def get(self, url, params=None, **kwargs):
        return requests.get(url, params, **kwargs)
