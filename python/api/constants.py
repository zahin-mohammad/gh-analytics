LOGFILE = "log.txt"

GITHUB_BASE_URL = "https://api.github.com"
GET_EVENTS = "/events"
GET_USERS = "/users/%s" # .../:user
GET_COMMIT_COMMENTS = "/repos/%s/%s/comments" # .../:owner/:repo/...
GET_COMMENT_REACTION = "/repos/%s/%s/comments/%s/reactions" # .../:owner/:repo/.../:comment_id/...
REACTION_HEADER ={'Accept': 'application/vnd.github.squirrel-girl-preview+json'}
