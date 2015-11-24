#Fuck ISIS
 
#We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us
#Title: Twitter login
#Details:It is a script to login to twitter from python
#Author: codezero

import requests
from lxml.html import fromstring

with requests.Session() as c:
    url = 'https://mobile.twitter.com/session'
    response = c.get(url)

    html = fromstring(response.content)
    payload = dict(html.forms[0].fields)

    payload.update({
      #email
       'username': '',
      #password
       'password': '',
    })

    print payload

    c.post(url, data=payload)
    r = c.get('https://mobile.twitter.com/account')
    print r.content
    test = c.get('https://mobile.twitter.com/account')
