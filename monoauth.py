import urllib.request
import socket

count_nm = 100
ip_adress = socket.gethostbyname(socket.gethostname())


#url = "https://13gwgepmkk.execute-api.ap-northeast-1.amazonaws.com/prod"
url = "https://13gwgepmkk.execute-api.ap-northeast-1.amazonaws.com/prod"

params = {
    'user_id': "myuser",
    'count' : count_nm,
    'program_name' : "monoget",
    'ip_adress' : ip_adress
}

## Get Request
req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
with urllib.request.urlopen(req) as res:
    body = res.read()


