import requests
from requests.auth import HTTPDigestAuth
import traceback
from githubapi import GitHubAPI


import json
from key import *  

USER = "zahin-mohammad"
TOKEN = GITHUB_PERSONAL_ACCESS_TOKEN

gitHubAPI = GitHubAPI(USER, TOKEN)
print(gitHubAPI.rateLimitRemaining)


# print(json.dumps(rateLimitInfo.json(), indent=2))

GITHUB_BASE_URL = "https://api.github.com"
# GET_EVENTS = "/events"
# # GET /repos/:owner/:repo/comments
GET_COMMIT_COMMENTS = "/repos/%s/%s/comments"

# # GET /repos/:owner/:repo/comments/:comment_id/reactions
# GET_COMMENT_REACTION = "/repos/%s/%s/comments/%s/reactions"
# REACTION_HEADER ={'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

# # Proof Of Concept Test
OWNER = "defunkt"
REPO = "facebox"
failCounter = 0
for i in range (0, 100, 1):
    try:
        url = GITHUB_BASE_URL + (GET_COMMIT_COMMENTS % (OWNER, REPO))
        gitHubAPI.makeRequest("get", url, auth=(USER, TOKEN))
    except:
        failCounter+=1
print(failCounter)
print(gitHubAPI.rateLimitRemaining)

# resp = requests.get(GITHUB_BASE_URL + (GET_COMMIT_COMMENTS % (OWNER, REPO)), auth=(USER, PASS))
# # print (resp.json())
# # if resp.status_code != 200:
#     # This means something went wrong.
#     # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# # print(json.dumps(resp.json(), indent=2))
# commentIdList  = [comment['id'] for comment in resp.json()]

# for commmentID in commentIdList:
#     try:
#         url = GITHUB_BASE_URL + (GET_COMMENT_REACTION % (OWNER, REPO, commmentID))
#         resp = requests.get(url, headers = REACTION_HEADER, auth=(USER, PASS))
#         print(json.dumps(resp.json(), indent=2))
#     except:
#         traceback.print_exc()
#         # print(":((((")
# print(commentIdList)