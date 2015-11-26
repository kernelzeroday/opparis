#Fuck ISIS
 
#We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us
#Details:It is a script for spamming hashtags
#Author: codezero
#Version: 0.01
#
#YOU NEED EMAIL VERIFIED TWITTER ACCOUNT FOR THIS TO WORK
#
#


import requests
from lxml.html import fromstring
import time
import random
import string

#hashtag to spam
hashtag = ""

#text to spam
text = ""


rand = "default"
char_set = string.ascii_uppercase + string.digits
#for debuging
#file = "testt.html"
#fhtml = open(file,'w')
i=0

with requests.Session() as c:
    url = 'https://mobile.twitter.com/session'
    response = c.get(url)

    html = fromstring(response.content)
    payload = dict(html.forms[0].fields)
    #email and password
    payload.update({
       'username': 'email',
       'password': 'password',
    })

    c.post(url, data=payload)
    r = c.get('https://mobile.twitter.com/account')
    #print r.content
    #test = c.get('https://mobile.twitter.com/')
    #print test.content

    url = 'https://mobile.twitter.com/compose/tweet'
    response = c.get(url)

    html = fromstring(response.content)
    payload = dict(html.forms[0].fields)


    while 1:
        try:
            i += 1
            rand = ''.join(random.sample(char_set*6, 6))
            payload.update({
            'tweet[text]': hashtag + " " + text + " " + rand + " " + i,
            })
            print i

            r = c.post("https://mobile.twitter.com/compose/tweet", data =payload)
            #debug
            #fhtml.write(r.content)
            #print r.content
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            #debug
            #fhtml.close()
            raise
