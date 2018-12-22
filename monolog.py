# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 21:29:57 2018

@author: fukui
"""

import urllib.request
import socket


def monogetLogInsert(userid, prgname, count):
    ip_adress = socket.gethostbyname(socket.gethostname())
    
    
    #url = "https://13gwgepmkk.execute-api.ap-northeast-1.amazonaws.com/prod"
    url = "https://13gwgepmkk.execute-api.ap-northeast-1.amazonaws.com/prod"
    
    params = {
        'user_id': userid,
        'count' : count,
        'program_name' : prgname,
        'ip_adress' : ip_adress
    }
    
    ## Get Request
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = res.read()
    
